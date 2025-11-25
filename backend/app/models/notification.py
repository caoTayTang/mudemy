from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime, time, date, timezone
import enum
from .base import Base

class NotificationType(str, enum.Enum):
    SESSION_REMINDER = "session_reminder"
    SCHEDULE_CHANGE = "schedule_change"
    ENROLLMENT_SUCCESS = "enrollment_success"
    ENROLLMENT_CANCELLED = "enrollment_cancelled"
    FEEDBACK_REQUEST = "feedback_request"
    SYSTEM_ANNOUNCEMENT = "system_announcement"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, nullable=False, index=True)  #target user
    
    type = Column(Enum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    related_id = Column(Integer, nullable=True) #related course id
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    #user = relationship("MututorUser", back_populates="notifications") 

    def __repr__(self):
        return f"<Notification(id={self.id}, type={self.type}, is_read={self.is_read})>"