from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from .base import Base

class EnrollmentStatus(str, enum.Enum):
    ENROLLED = "enrolled"
    COMPLETED = "completed"
    DROPPED = "dropped"

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)

    tutee_id = Column(String, nullable=False, index=True)
    
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ENROLLED)

    enrollment_date = Column(DateTime, default=datetime.now(timezone.utc))
    
    drop_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    course = relationship("Course", back_populates="enrollments")
    evaluations = relationship("SessionEvaluation", back_populates="enrollment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Enrollment(id={self.id}, tutee_id={self.tutee_id}, course_id={self.course_id})>"