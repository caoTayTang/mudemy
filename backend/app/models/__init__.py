from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from .base import Base
from .models import *


# SERVER_NAME = 'DESKTOP-IM92AEE\\SQLEXPRESS' 
SERVER_NAME = r'localhost\SQLEXPRESS'
DATABASE_NAME = 'MUDemy'
CONNECTION_STRING = f'mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
# USERNAME = "student123"
# PASSWORD = "Pass123!"
# CONNECTION_STRING = (
#     f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER_NAME}/{DATABASE_NAME}"
#     "?driver=ODBC+Driver+17+for+SQL+Server"
# )

engine = create_engine(CONNECTION_STRING, echo=False) 
mudemy_session = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


__all__ = [
    "User",
    "Qualification",
    "Interests",
    "Category",
    "Course",
    "Requires",
    "Instruct",
    "Enrollment",
    "Payment",
    "Certificate",
    "Module",
    "LessonRef",
    "Content",
    "Text",
    "Video",
    "Image",
    "Resource",
    "ProvideResource",
    "Assignment",
    "Quiz",
    "Question",
    "Answer",
    "AssignSubmission",
    "QuizSubmission",
    "Take",
    "engine",
    "mudemy_session",
    "Base",
    "generate_id"
]

prefix_map = {"User.UserID":["USR",5],
          "Course.CourseID":["CRS",5],
          "Module.ModuleID":["MOD",3],
          "Payment.PaymentID":["PAY",3],
          "Enrollment.EnrollmentID":["ENR",3],
          "Content.ContentID":["CON",3],
          "Video.VideoID":["VID",3],
          "Text.TextID":["TXT",3],
          "Image.ImageID":["IMG",3],
          "Resource.ResourceID":["RES",3],
          "Assignment.AssID":["ASS",3],
          "Quiz.QuizID":["QUI",3],
          "Question.QuestionID":["Q",3],
          "Answer.AnswerID":["ANS",1],
          "AssignSubmission.SubID":["SUB",3],
          "QuizSubmission.SubID":["SUB",3],
          "Certificate.CertificateID":["CER",3]
          }

def generate_id(session, id_column):
    prefix, pad_len = prefix_map.get(str(id_column))
    with session() as s:
        last_id = s.query(func.max(id_column)).scalar()
        
        if last_id:
            try:
                number_part = int(last_id[len(prefix):]) 
                new_number = number_part + 1
            except ValueError:
                new_number = 1 
        else:
            new_number = 1
            
        return f"{prefix}{new_number:0{pad_len}d}"