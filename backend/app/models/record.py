from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, timezone
import enum
from .base import Base


class MeetingRecordStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class MeetingRecord(Base):
    __tablename__ = "meeting_records"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    tutor_id = Column(String, ForeignKey("users.id"), nullable=False) 
    attendees = Column(Text, nullable=True)  
    discussion_points = Column(Text, nullable=True)
    status = Column(Enum(MeetingRecordStatus), default=MeetingRecordStatus.PENDING)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    course = relationship("Course", back_populates="meeting_records")
    #tutor = relationship("User", back_populates="meeting_records") 

    def __repr__(self):
        return f"<MeetingRecord(id={self.id}, course_id={self.course_id}, status={self.status})>"
    
   