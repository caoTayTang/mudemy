from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from .base import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, nullable=False, index=True)
    topic = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Feedback(id={self.id}, topic={self.topic}, status={self.status})>"


class SessionEvaluation(Base):
    __tablename__ = "session_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    
    session_id = Column(Integer, ForeignKey("course_sessions.id"), nullable=False)  
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 scale
    comment = Column(Text, nullable=True)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    session = relationship("CourseSession", back_populates="evaluations")
    enrollment = relationship("Enrollment", back_populates="evaluations")

    def __repr__(self):
        return f"<SessionEvaluation(id={self.id}, session_id={self.session_id}, rating={self.rating})>"