from sqlalchemy import create_engine
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
    "Base"
]