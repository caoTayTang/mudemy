from sqlalchemy.orm import Session, sessionmaker
from typing import List, Optional
from datetime import datetime, timezone
from ..models.feedback import Feedback, SessionEvaluation


class FeedbackService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, user_id: str, topic: str, content: str, 
               is_anonymous: bool = False) -> Feedback:
        feedback = Feedback(
            user_id=user_id,
            topic=topic,
            content=content,
            is_anonymous=is_anonymous
        )
        db = self.db_session()
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
        db.close()
        return feedback

    def get_by_id(self, feedback_id: int) -> Optional[Feedback]:
        db = self.db_session()
        result = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Feedback]:
        db = self.db_session()
        result = db.query(Feedback).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_user(self, user_id: str) -> List[Feedback]:
        db = self.db_session()
        result = db.query(Feedback).filter(Feedback.user_id == user_id).all()
        db.close()
        return result

    def get_by_topic(self, topic: str) -> List[Feedback]:
        db = self.db_session()
        result = db.query(Feedback).filter(Feedback.topic == topic).all()
        db.close()
        return result

    def get_anonymous(self) -> List[Feedback]:
        db = self.db_session()
        result = db.query(Feedback).filter(Feedback.is_anonymous == True).all()
        db.close()
        return result

    def update(self, feedback_id: int, topic: Optional[str] = None,
               content: Optional[str] = None, is_anonymous: Optional[bool] = None) -> Optional[Feedback]:
        db = self.db_session()
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not feedback:
            db.close()
            return None
        
        if topic is not None:
            feedback.topic = topic
        if content is not None:
            feedback.content = content
        if is_anonymous is not None:
            feedback.is_anonymous = is_anonymous
        
        feedback.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(feedback)
        db.close()
        return feedback

    def delete(self, feedback_id: int) -> bool:
        db = self.db_session()
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not feedback:
            db.close()
            return False
        
        db.delete(feedback)
        db.commit()
        db.close()
        return True
    
class SessionEvaluationService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, session_id: int, enrollment_id: int, rating: int,
               comment: Optional[str] = None, is_anonymous: bool = False) -> SessionEvaluation:
        evaluation = SessionEvaluation(
            session_id=session_id,
            enrollment_id=enrollment_id,
            rating=rating,
            comment=comment,
            is_anonymous=is_anonymous
        )
        db = self.db_session()
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        db.close()
        return evaluation

    def get_by_id(self, evaluation_id: int) -> Optional[SessionEvaluation]:
        db = self.db_session()
        result = db.query(SessionEvaluation).filter(SessionEvaluation.id == evaluation_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SessionEvaluation]:
        db = self.db_session()
        result = db.query(SessionEvaluation).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_session(self, session_id: int) -> List[SessionEvaluation]:
        db = self.db_session()
        result = db.query(SessionEvaluation).filter(SessionEvaluation.session_id == session_id).all()
        db.close()
        return result

    def get_by_enrollment(self, enrollment_id: int) -> List[SessionEvaluation]:
        db = self.db_session()
        result = db.query(SessionEvaluation).filter(SessionEvaluation.enrollment_id == enrollment_id).all()
        db.close()
        return result

    def get_by_rating(self, rating: int) -> List[SessionEvaluation]:
        db = self.db_session()
        result = db.query(SessionEvaluation).filter(SessionEvaluation.rating == rating).all()
        db.close()
        return result

    def get_anonymous(self) -> List[SessionEvaluation]:
        db = self.db_session()
        result = db.query(SessionEvaluation).filter(SessionEvaluation.is_anonymous == True).all()
        db.close()
        return result

    def update(self, evaluation_id: int, rating: Optional[int] = None,
               comment: Optional[str] = None, is_anonymous: Optional[bool] = None) -> Optional[SessionEvaluation]:
        db = self.db_session()
        evaluation = db.query(SessionEvaluation).filter(SessionEvaluation.id == evaluation_id).first()
        if not evaluation:
            db.close()
            return None
        
        if rating is not None:
            evaluation.rating = rating
        if comment is not None:
            evaluation.comment = comment
        if is_anonymous is not None:
            evaluation.is_anonymous = is_anonymous
        
        evaluation.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(evaluation)
        db.close()
        return evaluation

    def delete(self, evaluation_id: int) -> bool:
        db = self.db_session()
        evaluation = db.query(SessionEvaluation).filter(SessionEvaluation.id == evaluation_id).first()
        if not evaluation:
            db.close()
            return False
        
        db.delete(evaluation)
        db.commit()
        db.close()
        return True