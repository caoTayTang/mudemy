from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, String, ForeignKey
from typing import List, Optional
from datetime import datetime, date
from ..models.models import User
from ..models.base import Base

qualification_table = Table('QUALIFICATION', Base.metadata,
    Column('UserID', String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    Column('Qualification', String(200), primary_key=True)
)

interests_table = Table('INTERESTS', Base.metadata,
    Column('UserID', String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    Column('Interest', String(100), primary_key=True)
)

instruct_table = Table('INSTRUCT', Base.metadata,
    Column('UserID', String(10), ForeignKey('USER.UserID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    Column('CourseID', String(10), ForeignKey('COURSE.CourseID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
)

class UserService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, user_id: str, username: str, email: str, password: str,
               full_name: Optional[str] = None, city: Optional[str] = None,
               country: Optional[str] = None, phone: Optional[str] = None,
               date_of_birth: Optional[date] = None, is_instructor: bool = False,
               is_student: bool = False) -> User:
        user = User(
            UserID=user_id,
            User_name=username,
            Email=email,
            Password=password,
            Full_name=full_name,
            City=city,
            Country=country,
            Phone=phone,
            Date_of_birth=date_of_birth,
            IFlag=is_instructor,
            SFlag=is_student,
            Total_enrollments=0,
            Last_login=datetime.utcnow()
        )
        db = self.db_session()
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        db = self.db_session()
        result = db.query(User).filter(User.UserID == user_id).first()
        db.close()
        return result

    def get_by_username(self, username: str) -> Optional[User]:
        db = self.db_session()
        result = db.query(User).filter(User.User_name == username).first()
        db.close()
        return result

    def get_by_email(self, email: str) -> Optional[User]:
        db = self.db_session()
        result = db.query(User).filter(User.Email == email).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        db = self.db_session()
        result = db.query(User).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_instructors(self, skip: int = 0, limit: int = 100) -> List[User]:
        db = self.db_session()
        result = db.query(User).filter(User.IFlag == True).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_students(self, skip: int = 0, limit: int = 100) -> List[User]:
        db = self.db_session()
        result = db.query(User).filter(User.SFlag == True).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_city(self, city: str) -> List[User]:
        db = self.db_session()
        result = db.query(User).filter(User.City == city).all()
        db.close()
        return result

    def get_by_country(self, country: str) -> List[User]:
        db = self.db_session()
        result = db.query(User).filter(User.Country == country).all()
        db.close()
        return result

    def update(self, user_id: str, username: Optional[str] = None,
               email: Optional[str] = None, password: Optional[str] = None,
               full_name: Optional[str] = None, city: Optional[str] = None,
               country: Optional[str] = None, phone: Optional[str] = None,
               date_of_birth: Optional[date] = None, bio_text: Optional[str] = None,
               year_of_experience: Optional[int] = None) -> Optional[User]:
        db = self.db_session()
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            db.close()
            return None
        
        if username is not None:
            user.User_name = username
        if email is not None:
            user.Email = email
        if password is not None:
            user.Password = password
        if full_name is not None:
            user.Full_name = full_name
        if city is not None:
            user.City = city
        if country is not None:
            user.Country = country
        if phone is not None:
            user.Phone = phone
        if date_of_birth is not None:
            user.Date_of_birth = date_of_birth
        if bio_text is not None:
            user.Bio_text = bio_text
        if year_of_experience is not None:
            user.Year_of_experience = year_of_experience
        
        db.commit()
        db.refresh(user)
        db.close()
        return user

    def update_last_login(self, user_id: str) -> Optional[User]:
        db = self.db_session()
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            db.close()
            return None
        
        user.Last_login = datetime.utcnow()
        db.commit()
        db.refresh(user)
        db.close()
        return user

    def set_instructor_flag(self, user_id: str, is_instructor: bool) -> Optional[User]:
        db = self.db_session()
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            db.close()
            return None
        
        user.IFlag = is_instructor
        db.commit()
        db.refresh(user)
        db.close()
        return user

    def set_student_flag(self, user_id: str, is_student: bool) -> Optional[User]:
        db = self.db_session()
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            db.close()
            return None
        
        user.SFlag = is_student
        db.commit()
        db.refresh(user)
        db.close()
        return user

    def increment_enrollments(self, user_id: str) -> Optional[User]:
        db = self.db_session()
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            db.close()
            return None
        
        user.Total_enrollments = (user.Total_enrollments or 0) + 1
        db.commit()
        db.refresh(user)
        db.close()
        return user

    def delete(self, user_id: str) -> bool:
        db = self.db_session()
        user = db.query(User).filter(User.UserID == user_id).first()
        if not user:
            db.close()
            return False
        
        db.delete(user)
        db.commit()
        db.close()
        return True

    def add_qualification(self, user_id: str, qualification: str) -> bool:
        db = self.db_session()
        try:
            db.execute(qualification_table.insert().values(UserID=user_id, Qualification=qualification))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def remove_qualification(self, user_id: str, qualification: str) -> bool:
        db = self.db_session()
        result = db.execute(
            qualification_table.delete().where(
                (qualification_table.c.UserID == user_id) & 
                (qualification_table.c.Qualification == qualification)
            )
        )
        db.commit()
        db.close()
        return result.rowcount > 0

    def get_qualifications(self, user_id: str) -> List[str]:
        db = self.db_session()
        result = db.execute(
            qualification_table.select().where(qualification_table.c.UserID == user_id)
        ).fetchall()
        db.close()
        return [row.Qualification for row in result]

    def add_interest(self, user_id: str, interest: str) -> bool:
        db = self.db_session()
        try:
            db.execute(interests_table.insert().values(UserID=user_id, Interest=interest))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def remove_interest(self, user_id: str, interest: str) -> bool:
        db = self.db_session()
        result = db.execute(
            interests_table.delete().where(
                (interests_table.c.UserID == user_id) & 
                (interests_table.c.Interest == interest)
            )
        )
        db.commit()
        db.close()
        return result.rowcount > 0

    def get_interests(self, user_id: str) -> List[str]:
        db = self.db_session()
        result = db.execute(
            interests_table.select().where(interests_table.c.UserID == user_id)
        ).fetchall()
        db.close()
        return [row.Interest for row in result]


class InstructorService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def assign_to_course(self, user_id: str, course_id: str) -> bool:
        db = self.db_session()
        try:
            db.execute(instruct_table.insert().values(UserID=user_id, CourseID=course_id))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def remove_from_course(self, user_id: str, course_id: str) -> bool:
        db = self.db_session()
        result = db.execute(
            instruct_table.delete().where(
                (instruct_table.c.UserID == user_id) & 
                (instruct_table.c.CourseID == course_id)
            )
        )
        db.commit()
        db.close()
        return result.rowcount > 0

    def get_courses_by_instructor(self, user_id: str) -> List[str]:
        db = self.db_session()
        result = db.execute(
            instruct_table.select().where(instruct_table.c.UserID == user_id)
        ).fetchall()
        db.close()
        return [row.CourseID for row in result]

    def get_instructors_by_course(self, course_id: str) -> List[str]:
        db = self.db_session()
        result = db.execute(
            instruct_table.select().where(instruct_table.c.CourseID == course_id)
        ).fetchall()
        db.close()
        return [row.UserID for row in result]

    def get_instructor_stats(self, user_id: str) -> dict:
        db = self.db_session()
        instructor = db.query(User).filter(User.UserID == user_id).first()
        if not instructor:
            db.close()
            return {}
        
        courses = db.execute(
            instruct_table.select().where(instruct_table.c.UserID == user_id)
        ).fetchall()
        
        stats = {
            'user_id': user_id,
            'full_name': instructor.Full_name,
            'bio': instructor.Bio_text,
            'experience_years': instructor.Year_of_experience,
            'total_courses': len(courses),
            'qualifications': self.get_qualifications(user_id),
            'course_ids': [row.CourseID for row in courses]
        }
        
        db.close()
        return stats

    def get_qualifications(self, user_id: str) -> List[str]:
        db = self.db_session()
        result = db.execute(
            qualification_table.select().where(qualification_table.c.UserID == user_id)
        ).fetchall()
        db.close()
        return [row.Qualification for row in result]


class StudentService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def get_student_stats(self, user_id: str) -> dict:
        db = self.db_session()
        student = db.query(User).filter(User.UserID == user_id).first()
        if not student:
            db.close()
            return {}
        
        from ..models.models import Enrollment, Certificate
        
        enrollments = db.query(Enrollment).filter(Enrollment.StudentID == user_id).all()
        certificates = db.query(Certificate).filter(Certificate.StudentID == user_id).all()
        
        stats = {
            'user_id': user_id,
            'full_name': student.Full_name,
            'total_enrollments': student.Total_enrollments,
            'active_courses': len([e for e in enrollments if e.Status == 'Active']),
            'completed_courses': len(certificates),
            'interests': self.get_interests(user_id)
        }
        
        db.close()
        return stats

    def get_interests(self, user_id: str) -> List[str]:
        db = self.db_session()
        result = db.execute(
            interests_table.select().where(interests_table.c.UserID == user_id)
        ).fetchall()
        db.close()
        return [row.Interest for row in result]