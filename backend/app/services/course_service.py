from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional, Dict
from datetime import datetime, date, time, timezone
from ..models.course import Course, CourseStatus, Level, CourseSession, Subject, CourseFormat, CourseResource
from sqlalchemy import and_, or_

class CourseService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, title: str, tutor_id: str, subject_id: int, max_students: int,
               description: Optional[str] = None, cover_image_url: Optional[str] = None,
               level: Level = Level.BEGINNER, status: CourseStatus = CourseStatus.PENDING) -> Course:
        course = Course(
            title=title,
            description=description,
            cover_image_url=cover_image_url,
            tutor_id=tutor_id,
            subject_id=subject_id,
            level=level,
            max_students=max_students,
            status=status
        )
        db = self.db_session()
        db.add(course)
        db.commit()
        db.refresh(course)
        db.close()
        return course

    def get_by_id(self, course_id: int) -> Optional[Course]:
        db = self.db_session()
        result = db.query(Course).filter(Course.id == int(course_id)).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Course]:
        db = self.db_session()
        result = db.query(Course).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_tutor(self, tutor_id: str) -> List[Course]:
        db = self.db_session()
        result = db.query(Course).filter(Course.tutor_id == tutor_id).all()
        db.close()
        return result

    def get_by_subject(self, subject_id: int) -> List[Course]:
        db = self.db_session()
        result = db.query(Course).filter(Course.subject_id == subject_id).all()
        db.close()
        return result

    def get_by_status(self, status: CourseStatus) -> List[Course]:
        db = self.db_session()
        result = db.query(Course).filter(Course.status == status).all()
        db.close()
        return result

    def get_by_level(self, level: Level) -> List[Course]:
        db = self.db_session()
        result = db.query(Course).filter(Course.level == level).all()
        db.close()
        return result

    def update(self, course_id: int, title: Optional[str] = None, description: Optional[str] = None,
               cover_image_url: Optional[str] = None, level: Optional[Level] = None,
               max_students: Optional[int] = None, status: Optional[CourseStatus] = None) -> Optional[Course]:
        db = self.db_session()
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            db.close()
            return None
        
        if title is not None:
            course.title = title
        if description is not None:
            course.description = description
        if cover_image_url is not None:
            course.cover_image_url = cover_image_url
        if level is not None:
            course.level = level
        if max_students is not None:
            course.max_students = max_students
        if status is not None:
            course.status = status
        
        course.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(course)
        db.close()
        return course

    def delete(self, course_id: int) -> bool:
        db = self.db_session()
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            db.close()
            return False
        
        db.delete(course)
        db.commit()
        db.close()
        return True
    
class CourseSessionService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, course_id: int, session_number: int, session_date: date,
               start_time: time, end_time: time, format: CourseFormat = CourseFormat.OFFLINE,
               location: Optional[str] = None) -> CourseSession:
        session = CourseSession(
            course_id=course_id,
            session_number=session_number,
            session_date=session_date,
            start_time=start_time,
            end_time=end_time,
            format=format,
            location=location
        )
        db = self.db_session()
        db.add(session)
        db.commit()
        db.refresh(session)
        db.close()
        return session

    def get_by_course_session(self, course_id, session_id) -> Optional[CourseSession]:
        db = self.db_session()
        result = db.query(CourseSession).filter(
            CourseSession.course_id == course_id,
            CourseSession.session_number == session_id).first()
        db.close()
        return result

    def get_by_id(self, session_id: int) -> Optional[CourseSession]:
        db = self.db_session()
        result = db.query(CourseSession).filter(CourseSession.id == session_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CourseSession]:
        db = self.db_session()
        result = db.query(CourseSession).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_course(self, course_id: int) -> List[CourseSession]:
        db = self.db_session()
        result = db.query(CourseSession).filter(CourseSession.course_id == course_id).order_by(CourseSession.session_number).all()
        db.close()
        return result

    def get_by_course_snum(self, course_id:int, session_number: int)-> Optional[CourseSession]:
        db = self.db_session()
        result = db.query(CourseSession).filter(CourseSession.course_id == course_id, CourseSession.session_number == session_number).first()
        db.close()
        return result

    def get_by_date(self, session_date: date) -> List[CourseSession]:
        db = self.db_session()
        result = db.query(CourseSession).filter(CourseSession.session_date == session_date).all()
        db.close()
        return result

    def get_by_format(self, format: CourseFormat) -> List[CourseSession]:
        db = self.db_session()
        result = db.query(CourseSession).filter(CourseSession.format == format).all()
        db.close()
        return result

    def update(self, session_id: int, session_number: Optional[int] = None,
               session_date: Optional[date] = None, start_time: Optional[time] = None,
               end_time: Optional[time] = None, format: Optional[CourseFormat] = None,
               location: Optional[str] = None) -> Optional[CourseSession]:
        db = self.db_session()
        session = db.query(CourseSession).filter(CourseSession.id == session_id).first()
        if not session:
            db.close()
            return None
        
        if session_number is not None:
            session.session_number = session_number
        if session_date is not None:
            session.session_date = session_date
        if start_time is not None:
            session.start_time = start_time
        if end_time is not None:
            session.end_time = end_time
        if format is not None:
            session.format = format
        if location is not None:
            session.location = location

        db.commit()
        db.refresh(session)
        db.close()
        return session

    def delete(self, session_id: int) -> bool:
        db = self.db_session()
        session = db.query(CourseSession).filter(CourseSession.id == session_id).first()
        if not session:
            db.close()
            return False
        
        db.delete(session)
        db.commit()
        db.close()
        return True
    
    def delete_all_by_course(self, course_id: int) -> bool:
        db = self.db_session()
        count = db.query(CourseSession).filter(
            CourseSession.course_id == course_id
        ).delete()
        db.commit()
        db.close()
        return count
    
    def check_time_confict(
        self, 
        tutor_id: str, 
        sessions: Dict,
        exclude_session_id: Optional[int] = None
    ) -> Dict:
        errors = []
        
        with self.db_session() as session:
            session_date = datetime.strptime(sessions.get('session_date'), '%Y-%m-%d').date()
            start_time = datetime.strptime(sessions.get('start_time'), '%H:%M').time()
            end_time = datetime.strptime(sessions.get('end_time'), '%H:%M').time()
            session_format = sessions.get('format')

            if isinstance(session_format, str):
                session_format = CourseFormat(session_format.lower())

            tutor_courses_query = session.query(Course).filter(
                Course.tutor_id == tutor_id
            )
            
            tutor_courses = tutor_courses_query.all()
            
            for course in tutor_courses:
                conflicting_sessions = session.query(CourseSession).filter(
                    and_(
                        CourseSession.course_id == course.id,
                        CourseSession.session_date == session_date,
                        or_(
                            and_(
                                CourseSession.start_time <= start_time,
                                CourseSession.end_time > start_time
                            ),
                            and_(
                                CourseSession.start_time < end_time,
                                CourseSession.end_time >= end_time
                            ),
                            and_(
                                CourseSession.start_time >= start_time,
                                CourseSession.end_time <= end_time
                            )
                        )
                    )
                )
                
                if exclude_session_id:
                    conflicting_sessions = conflicting_sessions.filter(CourseSession.id != exclude_session_id)
                conflicting_sessions = conflicting_sessions.first()

                if conflicting_sessions:
                    errors.append(
                        f"Session {session_date} ({start_time}-{end_time}): "
                        f"Tutor has a conflicting session in course '{course.title}' "
                        f"({conflicting_sessions.start_time}-{conflicting_sessions.end_time})"
                    )
        return {
        "valid": len(errors) == 0,
        "errors": errors
    }
    
class CourseResourceService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, course_id: int, resource_id: int) -> CourseResource:
        """Create a new course resource link"""
        course_resource = CourseResource(
            course_id=course_id,
            resource_id=resource_id
        )
        db = self.db_session()
        db.add(course_resource)
        db.commit()
        db.refresh(course_resource)
        db.close()
        return course_resource

    def get_by_id(self, id: int) -> Optional[CourseResource]:
        """Get a course resource by its ID"""
        db = self.db_session()
        result = db.query(CourseResource).filter(CourseResource.id == id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CourseResource]:
        """Get all course resources with pagination"""
        db = self.db_session()
        result = db.query(CourseResource).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_course(self, course_id: int) -> List[CourseResource]:
        """Get all resources for a specific course"""
        db = self.db_session()
        result = db.query(CourseResource).filter(CourseResource.course_id == course_id).all()
        db.close()
        return result

    def get_by_resource(self, resource_id: int) -> List[CourseResource]:
        """Get all courses using a specific resource"""
        db = self.db_session()
        result = db.query(CourseResource).filter(CourseResource.resource_id == resource_id).all()
        db.close()
        return result

    def get_by_course_and_resource(self, course_id: int, resource_id: int) -> Optional[CourseResource]:
        """Get a specific course-resource link"""
        db = self.db_session()
        result = db.query(CourseResource).filter(
            CourseResource.course_id == course_id,
            CourseResource.resource_id == resource_id
        ).first()
        db.close()
        return result

    def update(self, id: int, course_id: Optional[int] = None, 
               resource_id: Optional[int] = None) -> Optional[CourseResource]:
        """Update a course resource link"""
        db = self.db_session()
        course_resource = db.query(CourseResource).filter(CourseResource.id == id).first()
        if not course_resource:
            db.close()
            return None
        
        if course_id is not None:
            course_resource.course_id = course_id
        if resource_id is not None:
            course_resource.resource_id = resource_id
        
        db.commit()
        db.refresh(course_resource)
        db.close()
        return course_resource

    def delete(self, id: int) -> bool:
        """Delete a course resource link by ID"""
        db = self.db_session()
        course_resource = db.query(CourseResource).filter(CourseResource.id == id).first()
        if not course_resource:
            db.close()
            return False
        
        db.delete(course_resource)
        db.commit()
        db.close()
        return True

    def delete_by_course_and_resource(self, course_id: int, resource_id: int) -> bool:
        """Delete a specific course-resource link"""
        db = self.db_session()
        course_resource = db.query(CourseResource).filter(
            CourseResource.course_id == course_id,
            CourseResource.resource_id == resource_id
        ).first()
        if not course_resource:
            db.close()
            return False
        
        db.delete(course_resource)
        db.commit()
        db.close()
        return True

    def delete_all_by_course(self, course_id: int) -> int:
        """Delete all resources for a specific course. Returns count of deleted records."""
        db = self.db_session()
        count = db.query(CourseResource).filter(
            CourseResource.course_id == course_id
        ).delete()
        db.commit()
        db.close()
        return count
    
class SubjectService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, id: int, name: str) -> Subject:
        subject = Subject(id=id, name=name)
        db = self.db_session()
        db.add(subject)
        db.commit()
        db.refresh(subject)
        db.close()
        return subject

    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        db = self.db_session()
        result = db.query(Subject).filter(Subject.id == subject_id).first()
        db.close()
        return result

    def get_by_name(self, name: str) -> Optional[Subject]:
        db = self.db_session()
        result = db.query(Subject).filter(Subject.name == name).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Subject]:
        db = self.db_session()
        result = db.query(Subject).offset(skip).limit(limit).all()
        db.close()
        return result

    def update(self, subject_id: int, name: Optional[str] = None) -> Optional[Subject]:
        db = self.db_session()
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            db.close()
            return None
        
        if name is not None:
            subject.name = name
        
        db.commit()
        db.refresh(subject)
        db.close()
        return subject

    def delete(self, subject_id: int) -> bool:
        db = self.db_session()
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            db.close()
            return False
        
        db.delete(subject)
        db.commit()
        db.close()
        return True