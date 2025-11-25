from .user import MututorUser, UserRole, MuSession
from .course import Course, CourseStatus, CourseFormat, Subject, Level, CourseSession, CourseResource
from .enrollment import Enrollment, EnrollmentStatus
from .feedback import Feedback, SessionEvaluation
from .notification import Notification, NotificationType
from .record import MeetingRecord, MeetingRecordStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .base import Base

DATABASE_URL = "sqlite:///./app/models/mututor.db"

engine = create_engine(DATABASE_URL, echo=False)
mututor_session = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)

__all__ = [
    "MututorUser",
    "UserRole",
    "Course",
    "CourseStatus",
    "CourseFormat",
    "Subject",
    "Level",
    "CourseSession",
    "CourseResource",
    "Enrollment",
    "EnrollmentStatus",
    "Feedback",
    "SessionEvaluation",
    "Notification",
    "NotificationType",
    "MeetingRecord",
    "MeetingRecordStatus",
    "MuSession",
    "mututor_session",
    "Base"
]


def clear_all_sessions():
    """
    Clear all rows from the MuSession table.
    This is useful for cleanup operations or resetting session data.
    
    Returns:
        int: Number of sessions deleted
    """
    with mututor_session() as session:
        deleted_count = session.query(MuSession).delete()
        session.commit()
        return deleted_count
