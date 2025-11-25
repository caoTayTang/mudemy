from sqlalchemy.orm import Session, sessionmaker
from .user_service import UserService
from .course_service import CourseService, CourseSessionService, SubjectService, CourseResourceService
from .enrollment_service import EnrollmentService
from .feedback_service import FeedbackService, SessionEvaluationService
from .notification_service import NotificationService, ReminderService
from .record_service import MeetingRecordService


class ServiceRegistry:
    def __init__(self, db_session: sessionmaker):
        self.db = db_session
        self.user = UserService(db_session)
        self.subject = SubjectService(db_session)
        self.course = CourseService(db_session)
        self.course_session = CourseSessionService(db_session)
        self.enrollment = EnrollmentService(db_session)
        self.feedback = FeedbackService(db_session)
        self.session_evaluation = SessionEvaluationService(db_session)
        self.notification = NotificationService(db_session)
        self.meeting_record = MeetingRecordService(db_session)


def get_services(db_session: sessionmaker) -> ServiceRegistry:
    return ServiceRegistry(db_session)


__all__ = [
    "UserService",
    "SubjectService",
    "CourseService",
    "CourseSessionService",
    "EnrollmentService",
    "FeedbackService",
    "SessionEvaluationService",
    "NotificationService",
    "ReminderService",
    "MeetingRecordService",
    "ServiceRegistry",
    "CourseResourceService",
    "get_services"
]