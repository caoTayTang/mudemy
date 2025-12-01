from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models.models import User, Take, Interests, Instruct, Qualification


class UserService:
    """Service for User CRUD operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create a new user"""
        with self.db_session() as session:
            try:
                user = User(**user_data)
                session.add(user)
                session.commit()
                session.refresh(user)
                return user
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating user: {str(e)}")
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        with self.db_session() as session:
            return session.query(User).filter(User.UserID == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        with self.db_session() as session:
            return session.query(User).filter(User.User_name == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        with self.db_session() as session:
            return session.query(User).filter(User.Email == email).first()
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        with self.db_session() as session:
            return session.query(User).offset(skip).limit(limit).all()
    
    def get_instructors(self) -> List[User]:
        """Get all instructors"""
        with self.db_session() as session:
            return session.query(User).filter(User.IFlag == True).all()
    
    def get_students(self) -> List[User]:
        """Get all students"""
        with self.db_session() as session:
            return session.query(User).filter(User.SFlag == True).all()
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[User]:
        """Update user information"""
        with self.db_session() as session:
            user = session.query(User).filter(User.UserID == user_id).first()
            if not user:
                return None
            
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            session.commit()
            session.refresh(user)
            return user
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        with self.db_session() as session:
            user = session.query(User).filter(User.UserID == user_id).first()
            if not user:
                return False
            
            session.delete(user)
            session.commit()
            return True
    
    def update_last_login(self, user_id: str) -> Optional[User]:
        """Update user's last login timestamp"""
        with self.db_session() as session:
            user = session.query(User).filter(User.UserID == user_id).first()
            if not user:
                return None
            
            user.Last_login = datetime.utcnow()
            session.commit()
            session.refresh(user)
            return user
    
    def increment_enrollments(self, user_id: str) -> Optional[User]:
        """Increment total enrollments for a student"""
        with self.db_session() as session:
            user = session.query(User).filter(User.UserID == user_id).first()
            if not user:
                return None
            
            if user.Total_enrollments is None:
                user.Total_enrollments = 1
            else:
                user.Total_enrollments += 1
            
            session.commit()
            session.refresh(user)
            return user
    
    def search_users_by_name(self, name: str) -> List[User]:
        """Search users by full name"""
        with self.db_session() as session:
            return session.query(User).filter(User.Full_name.like(f'%{name}%')).all()


class TakeService:
    """Service for Take (lesson progress) operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_take(self, user_id: str, lesson_id: str, is_finished: bool = False) -> Take:
        """Record that a user is taking/has taken a lesson"""
        with self.db_session() as session:
            try:
                take = Take(UserID=user_id, LessonID=lesson_id, is_finished=is_finished)
                session.add(take)
                session.commit()
                session.refresh(take)
                return take
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating take record: {str(e)}")
    
    def get_take(self, user_id: str, lesson_id: str) -> Optional[Take]:
        """Get a specific take record"""
        with self.db_session() as session:
            return session.query(Take).filter(
                Take.UserID == user_id,
                Take.LessonID == lesson_id
            ).first()
    
    def get_user_lessons(self, user_id: str) -> List[Take]:
        """Get all lessons taken by a user"""
        with self.db_session() as session:
            return session.query(Take).filter(Take.UserID == user_id).all()
    
    def get_completed_lessons(self, user_id: str) -> List[Take]:
        """Get completed lessons by a user"""
        with self.db_session() as session:
            return session.query(Take).filter(
                Take.UserID == user_id,
                Take.is_finished == True
            ).all()
    
    def get_incomplete_lessons(self, user_id: str) -> List[Take]:
        """Get incomplete lessons by a user"""
        with self.db_session() as session:
            return session.query(Take).filter(
                Take.UserID == user_id,
                Take.is_finished == False
            ).all()
    
    def mark_lesson_finished(self, user_id: str, lesson_id: str) -> Optional[Take]:
        """Mark a lesson as finished"""
        with self.db_session() as session:
            take = session.query(Take).filter(
                Take.UserID == user_id,
                Take.LessonID == lesson_id
            ).first()
            
            if not take:
                return None
            
            take.is_finished = True
            session.commit()
            session.refresh(take)
            return take
    
    def mark_lesson_unfinished(self, user_id: str, lesson_id: str) -> Optional[Take]:
        """Mark a lesson as unfinished"""
        with self.db_session() as session:
            take = session.query(Take).filter(
                Take.UserID == user_id,
                Take.LessonID == lesson_id
            ).first()
            
            if not take:
                return None
            
            take.is_finished = False
            session.commit()
            session.refresh(take)
            return take
    
    def delete_take(self, user_id: str, lesson_id: str) -> bool:
        """Delete a take record"""
        with self.db_session() as session:
            take = session.query(Take).filter(
                Take.UserID == user_id,
                Take.LessonID == lesson_id
            ).first()
            
            if not take:
                return False
            
            session.delete(take)
            session.commit()
            return True
    
    def get_lesson_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's lesson progress statistics"""
        with self.db_session() as session:
            all_lessons = session.query(Take).filter(Take.UserID == user_id).all()
            completed = session.query(Take).filter(
                Take.UserID == user_id,
                Take.is_finished == True
            ).count()
            total = len(all_lessons)
            
            return {
                'total_lessons': total,
                'completed_lessons': completed,
                'incomplete_lessons': total - completed,
                'completion_rate': (completed / total * 100) if total > 0 else 0
            }


class InterestsService:
    """Service for Student Interests operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def add_interest(self, user_id: str, interest: str) -> Interests:
        """Add an interest for a student"""
        with self.db_session() as session:
            try:
                interest_obj = Interests(UserID=user_id, Interest=interest)
                session.add(interest_obj)
                session.commit()
                session.refresh(interest_obj)
                return interest_obj
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error adding interest: {str(e)}")
    
    def get_user_interests(self, user_id: str) -> List[Interests]:
        """Get all interests for a user"""
        with self.db_session() as session:
            return session.query(Interests).filter(Interests.UserID == user_id).all()
    
    def get_users_by_interest(self, interest: str) -> List[Interests]:
        """Get all users with a specific interest"""
        with self.db_session() as session:
            return session.query(Interests).filter(Interests.Interest == interest).all()
    
    def remove_interest(self, user_id: str, interest: str) -> bool:
        """Remove an interest from a user"""
        with self.db_session() as session:
            interest_obj = session.query(Interests).filter(
                Interests.UserID == user_id,
                Interests.Interest == interest
            ).first()
            
            if not interest_obj:
                return False
            
            session.delete(interest_obj)
            session.commit()
            return True
    
    def clear_user_interests(self, user_id: str) -> bool:
        """Remove all interests for a user"""
        with self.db_session() as session:
            interests = session.query(Interests).filter(Interests.UserID == user_id).all()
            
            if not interests:
                return False
            
            for interest in interests:
                session.delete(interest)
            
            session.commit()
            return True


class InstructService:
    """Service for Instructor-Course relationship operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def assign_instructor(self, user_id: str, course_id: str) -> Instruct:
        """Assign an instructor to a course"""
        with self.db_session() as session:
            try:
                instruct = Instruct(UserID=user_id, CourseID=course_id)
                session.add(instruct)
                session.commit()
                session.refresh(instruct)
                return instruct
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error assigning instructor: {str(e)}")
    
    def get_instructor_courses(self, user_id: str) -> List[Instruct]:
        """Get all courses taught by an instructor"""
        with self.db_session() as session:
            return session.query(Instruct).filter(Instruct.UserID == user_id).all()
    
    def get_course_instructors(self, course_id: str) -> List[Instruct]:
        """Get all instructors for a course"""
        with self.db_session() as session:
            return session.query(Instruct).filter(Instruct.CourseID == course_id).all()
    
    def remove_instructor(self, user_id: str, course_id: str) -> bool:
        """Remove an instructor from a course"""
        with self.db_session() as session:
            instruct = session.query(Instruct).filter(
                Instruct.UserID == user_id,
                Instruct.CourseID == course_id
            ).first()
            
            if not instruct:
                return False
            
            session.delete(instruct)
            session.commit()
            return True
    
    def is_instructor_of_course(self, user_id: str, course_id: str) -> bool:
        """Check if a user is an instructor of a specific course"""
        with self.db_session() as session:
            instruct = session.query(Instruct).filter(
                Instruct.UserID == user_id,
                Instruct.CourseID == course_id
            ).first()
            
            return instruct is not None


class QualificationService:
    """Service for Instructor Qualifications operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def add_qualification(self, user_id: str, qualification: str) -> Qualification:
        """Add a qualification for an instructor"""
        with self.db_session() as session:
            try:
                qual = Qualification(UserID=user_id, Qualification=qualification)
                session.add(qual)
                session.commit()
                session.refresh(qual)
                return qual
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error adding qualification: {str(e)}")
    
    def get_user_qualifications(self, user_id: str) -> List[Qualification]:
        """Get all qualifications for a user"""
        with self.db_session() as session:
            return session.query(Qualification).filter(Qualification.UserID == user_id).all()
    
    def remove_qualification(self, user_id: str, qualification: str) -> bool:
        """Remove a qualification from a user"""
        with self.db_session() as session:
            qual = session.query(Qualification).filter(
                Qualification.UserID == user_id,
                Qualification.Qualification == qualification
            ).first()
            
            if not qual:
                return False
            
            session.delete(qual)
            session.commit()
            return True
    
    def clear_user_qualifications(self, user_id: str) -> bool:
        """Remove all qualifications for a user"""
        with self.db_session() as session:
            qualifications = session.query(Qualification).filter(
                Qualification.UserID == user_id
            ).all()
            
            if not qualifications:
                return False
            
            for qual in qualifications:
                session.delete(qual)
            
            session.commit()
            return True