from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from ..models.models import Submission, Take

class SubmissionService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, sub_id: str, sub_content: Optional[str] = None,
               quiz_id: Optional[str] = None, assign_id: Optional[str] = None,
               grade: Optional[Decimal] = None) -> Submission:
        submission = Submission(
            SubID=sub_id,
            QuizID=quiz_id,
            AssignID=assign_id,
            Sub_content=sub_content,
            Grade=grade,
            Sub_date=datetime.utcnow()
        )
        db = self.db_session()
        db.add(submission)
        db.commit()
        db.refresh(submission)
        db.close()
        return submission

    def get_by_id(self, sub_id: str) -> Optional[Submission]:
        db = self.db_session()
        result = db.query(Submission).filter(Submission.SubID == sub_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Submission]:
        db = self.db_session()
        result = db.query(Submission).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_quiz(self, quiz_id: str) -> List[Submission]:
        db = self.db_session()
        result = db.query(Submission).filter(Submission.QuizID == quiz_id).all()
        db.close()
        return result

    def get_by_assignment(self, assign_id: str) -> List[Submission]:
        db = self.db_session()
        result = db.query(Submission).filter(Submission.AssignID == assign_id).all()
        db.close()
        return result

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Submission]:
        db = self.db_session()
        result = db.query(Submission).filter(
            Submission.Sub_date >= start_date,
            Submission.Sub_date <= end_date
        ).all()
        db.close()
        return result

    def get_graded(self) -> List[Submission]:
        """Get all submissions that have been graded"""
        db = self.db_session()
        result = db.query(Submission).filter(Submission.Grade.isnot(None)).all()
        db.close()
        return result

    def get_ungraded(self) -> List[Submission]:
        """Get all submissions that haven't been graded yet"""
        db = self.db_session()
        result = db.query(Submission).filter(Submission.Grade.is_(None)).all()
        db.close()
        return result

    def get_by_grade_range(self, min_grade: Decimal, max_grade: Decimal) -> List[Submission]:
        """Get submissions within a grade range"""
        db = self.db_session()
        result = db.query(Submission).filter(
            Submission.Grade >= min_grade,
            Submission.Grade <= max_grade
        ).all()
        db.close()
        return result

    def update(self, sub_id: str, sub_content: Optional[str] = None,
               grade: Optional[Decimal] = None) -> Optional[Submission]:
        db = self.db_session()
        submission = db.query(Submission).filter(Submission.SubID == sub_id).first()
        if not submission:
            db.close()
            return None
        
        if sub_content is not None:
            submission.Sub_content = sub_content
        if grade is not None:
            submission.Grade = grade
        
        db.commit()
        db.refresh(submission)
        db.close()
        return submission

    def grade_submission(self, sub_id: str, grade: Decimal) -> Optional[Submission]:
        """Grade a submission"""
        return self.update(sub_id, grade=grade)

    def delete(self, sub_id: str) -> bool:
        db = self.db_session()
        submission = db.query(Submission).filter(Submission.SubID == sub_id).first()
        if not submission:
            db.close()
            return False
        
        db.delete(submission)
        db.commit()
        db.close()
        return True

    def get_average_grade_by_quiz(self, quiz_id: str) -> Optional[float]:
        """Calculate average grade for a quiz"""
        db = self.db_session()
        submissions = db.query(Submission).filter(
            Submission.QuizID == quiz_id,
            Submission.Grade.isnot(None)
        ).all()
        db.close()
        
        if not submissions:
            return None
        
        total = sum(float(s.Grade) for s in submissions)
        return total / len(submissions)

    def get_average_grade_by_assignment(self, assign_id: str) -> Optional[float]:
        """Calculate average grade for an assignment"""
        db = self.db_session()
        submissions = db.query(Submission).filter(
            Submission.AssignID == assign_id,
            Submission.Grade.isnot(None)
        ).all()
        db.close()
        
        if not submissions:
            return None
        
        total = sum(float(s.Grade) for s in submissions)
        return total / len(submissions)

    def get_submission_stats(self, sub_id: str) -> dict:
        """Get detailed statistics about a submission"""
        db = self.db_session()
        submission = db.query(Submission).filter(Submission.SubID == sub_id).first()
        
        if not submission:
            db.close()
            return {}
        
        stats = {
            'submission_id': sub_id,
            'quiz_id': submission.QuizID,
            'assignment_id': submission.AssignID,
            'grade': float(submission.Grade) if submission.Grade else None,
            'submitted_at': submission.Sub_date,
            'has_content': bool(submission.Sub_content),
            'is_graded': submission.Grade is not None
        }
        
        db.close()
        return stats


class TakeService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, user_id: str, lesson_id: str, is_finished: bool = False) -> Take:
        take = Take(
            UserID=user_id,
            LessonID=lesson_id,
            is_finished=is_finished
        )
        db = self.db_session()
        db.add(take)
        db.commit()
        db.refresh(take)
        db.close()
        return take

    def get_by_user_and_lesson(self, user_id: str, lesson_id: str) -> Optional[Take]:
        db = self.db_session()
        result = db.query(Take).filter(
            Take.UserID == user_id,
            Take.LessonID == lesson_id
        ).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Take]:
        db = self.db_session()
        result = db.query(Take).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_user(self, user_id: str) -> List[Take]:
        """Get all lessons taken by a user"""
        db = self.db_session()
        result = db.query(Take).filter(Take.UserID == user_id).all()
        db.close()
        return result

    def get_by_lesson(self, lesson_id: str) -> List[Take]:
        """Get all users who took a specific lesson"""
        db = self.db_session()
        result = db.query(Take).filter(Take.LessonID == lesson_id).all()
        db.close()
        return result

    def get_finished_by_user(self, user_id: str) -> List[Take]:
        """Get all finished lessons for a user"""
        db = self.db_session()
        result = db.query(Take).filter(
            Take.UserID == user_id,
            Take.is_finished == True
        ).all()
        db.close()
        return result

    def get_unfinished_by_user(self, user_id: str) -> List[Take]:
        """Get all unfinished lessons for a user"""
        db = self.db_session()
        result = db.query(Take).filter(
            Take.UserID == user_id,
            Take.is_finished == False
        ).all()
        db.close()
        return result

    def mark_as_finished(self, user_id: str, lesson_id: str) -> Optional[Take]:
        """Mark a lesson as finished"""
        db = self.db_session()
        take = db.query(Take).filter(
            Take.UserID == user_id,
            Take.LessonID == lesson_id
        ).first()
        
        if not take:
            db.close()
            return None
        
        take.is_finished = True
        db.commit()
        db.refresh(take)
        db.close()
        return take

    def mark_as_unfinished(self, user_id: str, lesson_id: str) -> Optional[Take]:
        """Mark a lesson as unfinished"""
        db = self.db_session()
        take = db.query(Take).filter(
            Take.UserID == user_id,
            Take.LessonID == lesson_id
        ).first()
        
        if not take:
            db.close()
            return None
        
        take.is_finished = False
        db.commit()
        db.refresh(take)
        db.close()
        return take

    def update(self, user_id: str, lesson_id: str, is_finished: Optional[bool] = None) -> Optional[Take]:
        db = self.db_session()
        take = db.query(Take).filter(
            Take.UserID == user_id,
            Take.LessonID == lesson_id
        ).first()
        
        if not take:
            db.close()
            return None
        
        if is_finished is not None:
            take.is_finished = is_finished
        
        db.commit()
        db.refresh(take)
        db.close()
        return take

    def delete(self, user_id: str, lesson_id: str) -> bool:
        db = self.db_session()
        take = db.query(Take).filter(
            Take.UserID == user_id,
            Take.LessonID == lesson_id
        ).first()
        
        if not take:
            db.close()
            return False
        
        db.delete(take)
        db.commit()
        db.close()
        return True

    def get_progress_by_user(self, user_id: str) -> dict:
        """Get lesson progress statistics for a user"""
        db = self.db_session()
        all_lessons = db.query(Take).filter(Take.UserID == user_id).all()
        finished = db.query(Take).filter(
            Take.UserID == user_id,
            Take.is_finished == True
        ).count()
        
        total = len(all_lessons)
        
        progress = {
            'user_id': user_id,
            'total_lessons': total,
            'finished_lessons': finished,
            'unfinished_lessons': total - finished,
            'completion_rate': (finished / total * 100) if total > 0 else 0
        }
        
        db.close()
        return progress

    def get_completion_rate_by_lesson(self, lesson_id: str) -> dict:
        """Get completion statistics for a specific lesson"""
        db = self.db_session()
        all_takes = db.query(Take).filter(Take.LessonID == lesson_id).all()
        finished = db.query(Take).filter(
            Take.LessonID == lesson_id,
            Take.is_finished == True
        ).count()
        
        total = len(all_takes)
        
        stats = {
            'lesson_id': lesson_id,
            'total_students': total,
            'finished_students': finished,
            'unfinished_students': total - finished,
            'completion_rate': (finished / total * 100) if total > 0 else 0
        }
        
        db.close()
        return stats