from sqlalchemy import Column, String, Integer, DateTime, Date, DECIMAL, Text as TextType, ForeignKey, Boolean, NVARCHAR, FetchedValue, CheckConstraint
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = 'USER'
    __table_args__ = {
        'extend_existing': True, 
   }
    
    UserID = Column(String(10), primary_key=True, server_default=FetchedValue())
    User_name = Column(NVARCHAR(100), nullable=False, unique=True)
    Email = Column(NVARCHAR(100), nullable=False, unique=True)
    Password = Column(NVARCHAR(255), nullable=False)
    Full_name = Column(NVARCHAR(100))
    City = Column(NVARCHAR(100))
    Country = Column(NVARCHAR(100))
    Phone = Column(String(10))
    Date_of_birth = Column(Date)
    Last_login = Column(DateTime)
    IFlag = Column(Boolean)  # Instructor flag
    Bio_text = Column(NVARCHAR(None))  # NVARCHAR(MAX)
    Year_of_experience = Column(Integer)
    Average_rating = Column(DECIMAL(3, 1),nullable=True,default=None)
    SFlag = Column(Boolean)  # Student flag
    Total_enrollments = Column(Integer, default=0)


class Qualification(Base):
    __tablename__ = 'QUALIFICATION'
    __table_args__ = {'extend_existing': True}
    
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Qualification = Column(NVARCHAR(200), primary_key=True)


class Interests(Base):
    __tablename__ = 'INTERESTS'
    __table_args__ = {'extend_existing': True}
    
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Interest = Column(NVARCHAR(100), primary_key=True)


class Category(Base):
    __tablename__ = 'CATEGORY'
    __table_args__ = {'extend_existing': True}
    
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID'), primary_key=True)
    Category = Column(NVARCHAR(100), primary_key=True)


class Course(Base):
    __tablename__ = 'COURSE'
    __table_args__ = {'extend_existing': True}
    
    CourseID = Column(String(10), primary_key=True)
    Difficulty = Column(NVARCHAR(20))
    Language = Column(NVARCHAR(50), nullable=False)
    Title = Column(NVARCHAR(200), nullable=False)
    Description = Column(NVARCHAR(None))  # NVARCHAR(MAX)


class Requires(Base):
    __tablename__ = 'REQUIRES'
    __table_args__ = {'extend_existing': True}
    
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID'), primary_key=True)
    Required_courseID = Column(String(10), ForeignKey('COURSE.CourseID'), primary_key=True)


class Instruct(Base):
    __tablename__ = 'INSTRUCT'
    __table_args__ = {'extend_existing': True}
    
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)


class Enrollment(Base):
    __tablename__ = 'ENROLLMENT'
    __table_args__ = {'extend_existing': True}
    
    EnrollmentID = Column(String(10), unique=True, nullable=False)
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    PaymentID = Column(String(10), ForeignKey('PAYMENT.PaymentID'), primary_key=True)
    StudentID = Column(String(10), ForeignKey('USER.UserID'), primary_key=True)
    Status = Column(NVARCHAR(20), default='Active')
    Enroll_date = Column(DateTime, default=datetime.utcnow)


class Payment(Base):
    __tablename__ = 'PAYMENT'
    __table_args__ = {'extend_existing': True}
    
    PaymentID = Column(String(10), primary_key=True)
    Amount = Column(Integer, nullable=False)
    Payment_date = Column(DateTime, default=datetime.utcnow)
    Payment_method = Column(NVARCHAR(50))
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'))


class Certificate(Base):
    __tablename__ = 'CERTIFICATE'
    __table_args__ = {'extend_existing': True}
    
    CertificateID = Column(String(10), unique=True, nullable=False)
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID'), primary_key=True)
    StudentID = Column(String(10), ForeignKey('USER.UserID'), primary_key=True)
    Expiry_date = Column(Date)
    Issue_date = Column(Date, default=datetime.utcnow)
    Certificate_number = Column(String(50), nullable=False)


class Module(Base):
    __tablename__ = 'MODULE'
    __table_args__ = {'extend_existing': True}
    
    ModuleID = Column(String(10), primary_key=True)
    Title = Column(NVARCHAR(200), nullable=False)
    CourseID = Column(String(10), ForeignKey('COURSE.CourseID', ondelete='CASCADE', onupdate='CASCADE'))


class LessonRef(Base):
    __tablename__ = 'LESSON_REF'
    __table_args__ = {'extend_existing': True}
    
    LessonID = Column(String(10), primary_key=True)


class Content(Base):
    __tablename__ = 'CONTENT'
    __table_args__ = {'extend_existing': True}
    
    ContentID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Slides = Column(NVARCHAR(100))
    Title = Column(NVARCHAR(200))
    ModuleID = Column(String(10), ForeignKey('MODULE.ModuleID'))


class Text(Base):
    __tablename__ = 'TEXT'
    __table_args__ = {'extend_existing': True}
    
    ContentID = Column(String(10), ForeignKey('CONTENT.ContentID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    TextID = Column(String(10), unique=True, nullable=False, primary_key=True)
    Text = Column(NVARCHAR(200))


class Video(Base):
    __tablename__ = 'VIDEO'
    __table_args__ = {'extend_existing': True}
    
    ContentID = Column(String(10), ForeignKey('CONTENT.ContentID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    VideoID = Column(String(10), unique=True, nullable=False, primary_key=True)
    Video = Column(NVARCHAR(200))


class Image(Base):
    __tablename__ = 'IMAGE'
    __table_args__ = {'extend_existing': True}
    
    ContentID = Column(String(10), ForeignKey('CONTENT.ContentID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    ImageID = Column(String(10), unique=True, nullable=False, primary_key=True)
    Image = Column(NVARCHAR(200))


class Resource(Base):
    __tablename__ = 'RESOURCE'
    __table_args__ = {'extend_existing': True}
    
    ResourceID = Column(String(10), primary_key=True)
    File_Name = Column(NVARCHAR(255), nullable=False)
    File_link = Column(NVARCHAR(500), nullable=False)
    External_link = Column(NVARCHAR(200))


class ProvideResource(Base):
    __tablename__ = 'PROVIDE_RESOURCE'
    __table_args__ = {'extend_existing': True}
    
    ResourceID = Column(String(10), ForeignKey('RESOURCE.ResourceID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    LessonID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)


class Assignment(Base):
    __tablename__ = 'ASSIGNMENT'
    __table_args__ = {'extend_existing': True}
    
    AssID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Deadline = Column(DateTime, nullable=False, default=datetime.utcnow)
    Description = Column(NVARCHAR(None))  # NVARCHAR(MAX)
    Title = Column(NVARCHAR(200), nullable=False)
    ModuleID = Column(String(10), ForeignKey('MODULE.ModuleID'))


class Quiz(Base):
    __tablename__ = 'QUIZ'
    __table_args__ = {'extend_existing': True}
    
    QuizID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    Time_limit = Column(Integer)
    Num_attempt = Column(Integer, default=1)
    Deadline = Column(DateTime, nullable=False, default=datetime.utcnow)
    Title = Column(NVARCHAR(200), nullable=False)
    ModuleID = Column(String(10), ForeignKey('MODULE.ModuleID'))


class Question(Base):
    __tablename__ = 'QUESTION'
    __table_args__ = {'extend_existing': True}
    
    QuestionID = Column(String(10), primary_key=True)
    QuizID = Column(String(10), ForeignKey('QUIZ.QuizID', ondelete='CASCADE', onupdate='CASCADE'))
    Correct_answer = Column(NVARCHAR(None), nullable=False)  # NVARCHAR(MAX)
    Content = Column(NVARCHAR(None), nullable=False)  # NVARCHAR(MAX)


class Answer(Base):
    __tablename__ = 'ANSWER'
    __table_args__ = {'extend_existing': True}
    
    QuestionID = Column(String(10), ForeignKey('QUESTION.QuestionID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    QuizID = Column(String(10), ForeignKey('QUIZ.QuizID'), primary_key=True)
    AnswerID = Column(String(10), unique=True, nullable=False, primary_key=True)
    Answer = Column(NVARCHAR(None), nullable=False)  # NVARCHAR(MAX)


class AssignSubmission(Base):
    __tablename__ = 'ASSIGN_SUBMISSION'
    __table_args__ = {'extend_existing': True}
    
    SubID = Column(String(10), primary_key=True)
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'))
    AssID = Column(String(10), ForeignKey('ASSIGNMENT.AssID', ondelete='CASCADE', onupdate='CASCADE'))
    Sub_content = Column(NVARCHAR(None))  # NVARCHAR(MAX)
    Grade = Column(DECIMAL(5, 2))
    Sub_date = Column(DateTime, nullable=False, default=datetime.utcnow)


class QuizSubmission(Base):
    __tablename__ = 'QUIZ_SUBMISSION'
    __table_args__ = {'extend_existing': True}
    
    SubID = Column(String(10), primary_key=True)
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'))
    QuizID = Column(String(10), ForeignKey('QUIZ.QuizID', ondelete='CASCADE', onupdate='CASCADE'))
    Sub_content = Column(NVARCHAR(None))  # NVARCHAR(MAX)
    Grade = Column(DECIMAL(5, 2))
    Sub_date = Column(DateTime, nullable=False, default=datetime.utcnow)


class Take(Base):
    __tablename__ = 'TAKE'
    __table_args__ = {'extend_existing': True}
    
    UserID = Column(String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    LessonID = Column(String(10), ForeignKey('LESSON_REF.LessonID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    is_finished = Column(Boolean, default=False)