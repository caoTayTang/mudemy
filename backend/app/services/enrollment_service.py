from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional
from datetime import datetime, timezone
from ..models.enrollment import Enrollment, EnrollmentStatus
from ..models.course import Course, CourseSession
from sqlalchemy import and_, or_

class EnrollmentService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, tutee_id: str, course_id: int, 
               status: EnrollmentStatus = EnrollmentStatus.ENROLLED) -> Enrollment:
        enrollment = Enrollment(
            tutee_id=tutee_id,
            course_id=course_id,
            status=status
        )
        db = self.db_session()
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        db.close()
        return enrollment

    def get_by_id(self, enrollment_id: int) -> Optional[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_tutee(self, tutee_id: str) -> List[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(Enrollment.tutee_id == tutee_id).all()
        db.close()
        return result

    def get_by_course(self, course_id: int) -> List[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
        db.close()
        return result

    def get_by_status(self, status: EnrollmentStatus) -> List[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(Enrollment.status == status).all()
        db.close()
        return result

    def get_by_tutee_and_course(self, tutee_id: str, course_id: int) -> Optional[Enrollment]:
        db = self.db_session()
        result = db.query(Enrollment).filter(
            Enrollment.tutee_id == tutee_id,
            Enrollment.course_id == course_id
        ).first()
        db.close()
        return result

    def update(self, enrollment_id: int, status: Optional[EnrollmentStatus] = None,
               drop_reason: Optional[str] = None) -> Optional[Enrollment]:
        db = self.db_session()
        enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            db.close()
            return None
        
        if status is not None:
            enrollment.status = status
        enrollment.drop_reason = drop_reason
        
        enrollment.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(enrollment)
        db.close()
        return enrollment

    def delete(self, enrollment_id: int) -> bool:
        db = self.db_session()
        enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            db.close()
            return False
        
        db.delete(enrollment)
        db.commit()
        db.close()
        return True
    
    def check_time_conflict(self, tutee_id: str, course_id: int) -> dict:
        """
        Check if enrolling in a course would create time conflicts with 
        the tutee's existing enrolled courses.
        
        Returns:
            dict: {
                'valid': bool,
                'errors': List[str]
            }
        """
        
        errors = []
        
        db = self.db_session()
        
        try:
            enrolled_courses = db.query(Enrollment).filter(
                Enrollment.tutee_id == tutee_id,
                Enrollment.status == EnrollmentStatus.ENROLLED
            ).all()

            new_course_sessions = db.query(CourseSession).filter(
                CourseSession.course_id == course_id
            ).all()
            
            for new_session in new_course_sessions:
                for enrollment in enrolled_courses:
                    existing_sessions = db.query(CourseSession).filter(
                        CourseSession.course_id == enrollment.course_id
                    ).all()
                    
                    for existing_session in existing_sessions:
                        if new_session.session_date == existing_session.session_date:
                            if (
                                (new_session.start_time >= existing_session.start_time and 
                                new_session.start_time < existing_session.end_time) or

                                (new_session.end_time > existing_session.start_time and 
                                new_session.end_time <= existing_session.end_time) or

                                (new_session.start_time <= existing_session.start_time and 
                                new_session.end_time >= existing_session.end_time)
                            ):
                                enrolled_course = db.query(Course).filter(
                                    Course.id == enrollment.course_id
                                ).first()
                                
                                errors.append(
                                    f"Session on {new_session.session_date} "
                                    f"({new_session.start_time}-{new_session.end_time}) "
                                    f"conflicts with enrolled course '{enrolled_course.title}' "
                                    f"session ({existing_session.start_time}-{existing_session.end_time})"
                                )
            
            return {
                'valid': len(errors) == 0,
                'errors': errors
            }
        
        finally:
            db.close()