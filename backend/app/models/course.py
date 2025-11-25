from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey, Text, Time, Date
from sqlalchemy.orm import relationship, declarative_base, Session
from datetime import datetime, time, date, timedelta, timezone
import enum
from .base import Base


class CourseStatus(str, enum.Enum):
    PENDING = "pending"   
    OPEN = "open"      
    ONGOING = "ongoing"  
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    INACTIVE = "inactive" 

class CourseFormat(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"



class Subject(Base):
    """
    Model for course subjects (e.g., 'Toán cao cấp', 'Lập trình').
    Corresponds to mockSubjects.
    """
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    courses = relationship("Course", back_populates="subject")

    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name})>"

class Level(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    cover_image_url = Column(String, nullable=True)
   

    tutor_id = Column(String, ForeignKey("users.id"), nullable=False, index=True) 
    
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    level = Column(Enum(Level), nullable=False, default=Level.BEGINNER)

    max_students = Column(Integer, nullable=False)
    status = Column(Enum(CourseStatus), default=CourseStatus.PENDING, index=True)
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    
    subject = relationship("Subject", back_populates="courses")
    
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    
    sessions = relationship("CourseSession", back_populates="course", cascade="all, delete-orphan")
    
    meeting_records = relationship("MeetingRecord", back_populates="course", cascade="all, delete-orphan")

    resource = relationship("CourseResource", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(id={self.id}, title={self.title}, status={self.status})>"



class CourseSession(Base):
    """
    Model for individual recurring sessions of a course.
    Corresponds to the 'schedule' array in the mock data.
    """
    __tablename__ = "course_sessions"

    id = Column(Integer, primary_key=True, index=True) 
    
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    
    session_number = Column(Integer, nullable=False)
    
    session_date = Column(Date, nullable=False) 
    
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    format = Column(Enum(CourseFormat), default=CourseFormat.OFFLINE)
    location = Column(String, nullable=True)  #  class room for offline courses or link for online courses


    course = relationship("Course", back_populates="sessions")
    evaluations = relationship("SessionEvaluation", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CourseSession(course_id={self.course_id}, session_id={self.id}, date={self.session_date})>"

class CourseResource(Base):
    __tablename__ = "course_resource"

    id = Column(Integer, primary_key=True, index=True) 
    
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    resource_id = Column(Integer, nullable=False, index=True)

    course = relationship("Course", back_populates="resource")
    
    def __repr__(self):
        return f"<CourseResource(course_id={self.course_id}, resource_id={self.resource_id})>"
    
