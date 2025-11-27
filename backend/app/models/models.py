from sqlalchemy import create_engine, Column, String, Integer, DateTime, Date, DECIMAL, Text as TextType, CheckConstraint, ForeignKey, Table, Boolean, NVARCHAR
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = 'USER'
    
    UserID = Column(String(10), primary_key=True)
    User_name = Column(NVARCHAR(100), nullable=False, unique=True)
    Email = Column(String(100), nullable=False, unique=True)
    Password = Column(String(255), nullable=False)
    Full_name = Column(String(100))
    City = Column(String(100))
    Country = Column(String(100))
    Phone = Column(String(10))
    Date_of_birth = Column(Date)
    Last_login = Column(DateTime)
    IFlag = Column(Boolean)  # Instructor flag
    Bio_text = Column(TextType)
    Year_of_experience = Column(Integer)
    SFlag = Column(Boolean)  # Student flag
    Total_enrollments = Column(Integer, default=0)
    


class Course(Base):
    __tablename__ = 'COURSE'
    
    CourseID = Column(String(10), primary_key=True)
    Difficulty = Column(String(20))
    Language = Column(String(50), nullable=False)
    Title = Column(String(200), nullable=False)
    Description = Column(TextType)
    


class Enrollment(Base):
    __tablename__ = 'ENROLLMENT'
    
    EnrollmentID = Column(String(10), primary_key=True)
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    PaymentID = Column(String(10), ForeignKey('PAYMENT.PaymentID'), primary_key=True)
    StudentID = Column(String(10), ForeignKey('USER.UserID'), primary_key=True)
    Status = Column(String(20), default='Active')
    Enroll_date = Column(DateTime, default=datetime.utcnow)
    


class Payment(Base):
    __tablename__ = 'PAYMENT'
    
    PaymentID = Column(String(10), primary_key=True)
    Amount = Column(Integer, nullable=False)
    Payment_date = Column(DateTime, default=datetime.utcnow)
    Payment_method = Column(String(50))
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'))
    


class Certificate(Base):
    __tablename__ = 'CERTIFICATE'
    
    CertificateID = Column(String(10), primary_key=True)
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID'), primary_key=True)
    StudentID = Column(String(10), ForeignKey('USER.UserID'), primary_key=True)
    Expiry_date = Column(Date)
    Issue_date = Column(Date, default=datetime.utcnow)
    Certificate_number = Column(String(50), nullable=False)



class Module(Base):
    __tablename__ = 'MODULE'
    
    ModuleID = Column(String(10), primary_key=True)
    Title = Column(String(200), nullable=False)
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID', ondelete='CASCADE', onupdate='CASCADE'))
    


class LessonRef(Base):
    __tablename__ = 'LESSON_REF'
    
    LessonID = Column(String(10), primary_key=True)



class Content(Base):
    __tablename__ = 'CONTENT'
    
    ContentID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Slides = Column(String(100))
    Title = Column(String(200))
    ModuleID = Column(String(10), ForeignKey('MODULE.ModuleID'))
    


class Text(Base):
    __tablename__ = 'TEXT'
    
    ContentID = Column(String(10), ForeignKey('CONTENT.ContentID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    TextID = Column(String(10), unique=True, primary_key=True)
    Text = Column(String(200))



class Video(Base):
    __tablename__ = 'VIDEO'
    
    ContentID = Column(String(10), ForeignKey('CONTENT.ContentID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    VideoID = Column(String(10), unique=True, primary_key=True)
    Video = Column(String(200))
    


class Image(Base):
    __tablename__ = 'IMAGE'
    
    ContentID = Column(String(10), ForeignKey('CONTENT.ContentID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    ImageID = Column(String(10), unique=True, primary_key=True)
    Image = Column(String(200))



class Resource(Base):
    __tablename__ = 'RESOURCE'
    
    ResourceID = Column(String(10), primary_key=True)
    File_Name = Column(String(255), nullable=False)
    File_link = Column(String(500), nullable=False)
    External_link = Column(String(200))



class Assignment(Base):
    __tablename__ = 'ASSIGNMENT'
    
    AssID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Deadline = Column(DateTime, default=datetime.utcnow)
    Description = Column(TextType)
    Title = Column(String(200), nullable=False)
    ModuleID = Column(String(10), ForeignKey('MODULE.ModuleID'))


class Quiz(Base):
    __tablename__ = 'QUIZ'
    
    QuizID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Time_limit = Column(Integer)
    Num_attempt = Column(Integer, default=1)
    Title = Column(String(200), nullable=False)
    ModuleID = Column(String(10), ForeignKey('MODULE.ModuleID'))


class Question(Base):
    __tablename__ = 'QUESTION'
    
    QuestionID = Column(String(10), unique=True, primary_key=True)
    QuizID = Column(String(10), ForeignKey('QUIZ.QuizID', ondelete='CASCADE', onupdate='CASCADE'))
    Correct_answer = Column(TextType, nullable=False)
    Content = Column(TextType, nullable=False)



class Answer(Base):
    __tablename__ = 'ANSWER'
    
    QuestionID = Column(String(10), ForeignKey('QUESTION.QuestionID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    QuizID = Column(String(10), ForeignKey('QUIZ.QuizID'), primary_key=True)
    AnswerID = Column(String(10), unique=True, primary_key=True)
    Answer = Column(TextType, nullable=False)



class Submission(Base):
    __tablename__ = 'SUBMISSION'
    
    SubID = Column(String(10), unique=True, primary_key=True)
    QuizID = Column(String(10), ForeignKey('QUIZ.QuizID'))
    AssignID = Column(String(10), ForeignKey('ASSIGNMENT.AssID'))
    Sub_content = Column(TextType)
    Grade = Column(DECIMAL(5, 2))
    Sub_date = Column(DateTime, default=datetime.utcnow)



class Take(Base):
    __tablename__ = 'TAKE'
    
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    LessonID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    is_finished = Column(Boolean, default=False)
