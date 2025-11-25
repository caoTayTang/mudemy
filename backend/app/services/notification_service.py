from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional
from datetime import datetime, timedelta, timezone, date
from ..models import CourseSession, Enrollment, Notification, NotificationType, EnrollmentStatus, Course
import asyncio
from ..core import*

logger = get_logger("Notice/Remind")
class ReminderService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    async def check_upcoming_sessions(self):
        """
        Runs continuously in the background.
        Checks for sessions starting in 15 minutes and sends notifications.
        """
        while True:
            try:
                await self._process_reminders()
            except Exception as e:
                print(f"Error in reminder scheduler: {e}")
            
            # Wait for 5 mins before next check
            logger.info("Sleeping now...")
            await asyncio.sleep(300)

    async def _process_reminders(self):
            db = self.db_session()
            try:
                now = datetime.now()
                limit_time = now + timedelta(days=2)

                candidates:List[CourseSession] = db.query(CourseSession).filter(
                    CourseSession.session_date >= now.date(),
                    CourseSession.session_date <= limit_time.date()
                ).all()  

                for session in candidates:           
                    session_start_dt = datetime.combine(session.session_date, session.start_time)

                    if now < session_start_dt <= limit_time:
                        
                        course:Course = db.query(Course).filter(Course.id == session.course_id).first()

                        enrollments:List[Enrollment] = db.query(Enrollment).filter(
                            Enrollment.course_id == session.course_id,
                            Enrollment.status == EnrollmentStatus.ENROLLED
                        ).all() 

                        #Notify Tutees
                        for enrollment in enrollments:
                            await self._create_and_send_reminder(
                                db, 
                                user_id=enrollment.tutee_id, 
                                course_title=course.title, 
                                session=session
                            )

                        #Notify Tutor
                        await self._create_and_send_reminder(
                            db, 
                            user_id=course.tutor_id, 
                            course_title=course.title, 
                            session=session,
                            is_tutor=True
                        )

            finally:
                db.close()

    async def _create_and_send_reminder(self, db, user_id, course_title, session:CourseSession, is_tutor=False):
        exists = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.related_id == session.id,
            Notification.type == NotificationType.SESSION_REMINDER
        ).first() #

        if exists:
            return 

        content = f"Your session for '{course_title}' starts at {session.start_time} on {session.session_date}."
        content += f"Format: {session.format}, location: {session.location}"

        new_notif = Notification(
            user_id=user_id,
            type=NotificationType.SESSION_REMINDER,
            title="Upcoming Session Reminder",
            content=content,
            related_id=session.id,
            is_read=False
        )
        db.add(new_notif)
        db.commit()
        db.refresh(new_notif)

        await manager.send_personal_message({
            "type": "NEW_NOTIFICATION",
            "data": {
                "id": new_notif.id,
                "title": new_notif.title,
                "content": new_notif.content,
                "type": new_notif.type.value,
                "created_at": new_notif.created_at.isoformat()
            }
        }, user_id)

    async def test(self):
        while True:
            try:
                print("calling sth")
            except Exception as e:
                print(f"Error in reminder scheduler: {e}")

            print("waiting 10s for next call")
            await asyncio.sleep(10)

class NotificationService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, user_id: str, type: NotificationType, title: str, content: str,
               related_id: Optional[int] = None, is_read: bool = False) -> Notification:
        notification = Notification(
            user_id=user_id,
            type=type,
            title=title,
            content=content,
            related_id=related_id,
            is_read=is_read
        )
        db = self.db_session()
        db.add(notification)
        db.commit()
        db.refresh(notification)
        db.close()
        return notification

    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        db = self.db_session()
        result = db.query(Notification).filter(Notification.id == notification_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Notification]:
        db = self.db_session()
        result = db.query(Notification).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_user(self, user_id: str) -> List[Notification]:
        db = self.db_session()
        result = db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()
        db.close()
        return result

    def get_unread_by_user(self, user_id: str) -> List[Notification]:
        db = self.db_session()
        result = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).order_by(Notification.created_at.desc()).all()
        db.close()
        return result

    def get_by_type(self, type: NotificationType) -> List[Notification]:
        db = self.db_session()
        result = db.query(Notification).filter(Notification.type == type).all()
        db.close()
        return result

    def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        db = self.db_session()
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            db.close()
            return None
        
        notification.is_read = True
        db.commit()
        db.refresh(notification)
        db.close()
        return notification

    def mark_all_as_read(self, user_id: str) -> int:
        db = self.db_session()
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})
        db.commit()
        db.close()
        return count

    def update(self, notification_id: int, title: Optional[str] = None,
               content: Optional[str] = None, is_read: Optional[bool] = None) -> Optional[Notification]:
        db = self.db_session()
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            db.close()
            return None
        
        if title is not None:
            notification.title = title
        if content is not None:
            notification.content = content
        if is_read is not None:
            notification.is_read = is_read
        
        db.commit()
        db.refresh(notification)
        db.close()
        return notification

    def delete(self, notification_id: int) -> bool:
        db = self.db_session()
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            db.close()
            return False
        
        db.delete(notification)
        db.commit()
        db.close()
        return True