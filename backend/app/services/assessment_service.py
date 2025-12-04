from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ..models.models import (
    Assignment, Quiz, Question, Answer,
    AssignSubmission, QuizSubmission
)
from ..models import generate_id


class AssignmentService:
    """Service for Assignment CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries: int = 50):
        self.db_session = db_session
        self.max_retries = max_retries
    
    def create_assignment(self, assignment_data: Dict[str, Any]) -> Assignment:
        """Create a new assignment"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, Assignment.AssID)
            assignment_data["AssID"] = new_id
            with self.db_session() as session:
                try:
                    assignment = Assignment(**assignment_data)
                    session.add(assignment)
                    session.commit()
                    session.refresh(assignment)
                    return assignment
                except IntegrityError:
                    session.rollback()
                    continue
                except Exception as e:
                    session.rollback()
                    raise ValueError(f"Error creating assignment: {str(e)}")
        raise Exception(f"Failed to generate unique ID for {Assignment.__name__} after {self.max_retries} attempts.")
    
    def get_assignment_by_id(self, ass_id: str) -> Optional[Assignment]:
        """Get assignment by ID"""
        with self.db_session() as session:
            return session.query(Assignment).filter(Assignment.AssID == ass_id).first()
    
    def get_assignments_by_module(self, module_id: str) -> List[Assignment]:
        """Get all assignments for a module"""
        with self.db_session() as session:
            return session.query(Assignment).filter(Assignment.ModuleID == module_id).all()
    
    def get_all_assignments(self) -> List[Assignment]:
        """Get all assignments"""
        with self.db_session() as session:
            return session.query(Assignment).all()
    
    def update_assignment(self, ass_id: str, update_data: Dict[str, Any]) -> Optional[Assignment]:
        """Update assignment information"""
        with self.db_session() as session:
            assignment = session.query(Assignment).filter(Assignment.AssID == ass_id).first()
            if not assignment:
                return None
            
            for key, value in update_data.items():
                if hasattr(assignment, key):
                    setattr(assignment, key, value)
            
            session.commit()
            session.refresh(assignment)
            return assignment
    
    def delete_assignment(self, ass_id: str) -> bool:
        """Delete an assignment"""
        with self.db_session() as session:
            assignment = session.query(Assignment).filter(Assignment.AssID == ass_id).first()
            if not assignment:
                return False
            
            session.delete(assignment)
            session.commit()
            return True
    
    def get_overdue_assignments(self) -> List[Assignment]:
        """Get all assignments past their deadline"""
        with self.db_session() as session:
            return session.query(Assignment).filter(
                Assignment.Deadline < datetime.utcnow()
            ).all()
    
    def get_upcoming_assignments(self, days: int = 7) -> List[Assignment]:
        """Get assignments due within specified days"""
        with self.db_session() as session:
            future_date = datetime.utcnow() + timedelta(days=days)
            return session.query(Assignment).filter(
                Assignment.Deadline <= future_date,
                Assignment.Deadline >= datetime.utcnow()
            ).all()


class QuizService:
    """Service for Quiz CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries: int = 50):
        self.db_session = db_session
        self.max_retries = max_retries
    
    def create_quiz(self, quiz_data: Dict[str, Any]) -> Quiz:
        """Create a new quiz"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, Quiz.QuizID)
            quiz_data["QuizID"] = new_id
            with self.db_session() as session:
                try:
                    quiz = Quiz(**quiz_data)
                    session.add(quiz)
                    session.commit()
                    session.refresh(quiz)
                    return quiz
                except IntegrityError:
                    session.rollback()
                    continue
                except Exception as e:
                    session.rollback()
                    raise ValueError(f"Error creating quiz: {str(e)}")
        raise Exception(f"Failed to generate unique ID for {Quiz.__name__} after {self.max_retries} attempts.")
    
    def get_quiz_by_id(self, quiz_id: str) -> Optional[Quiz]:
        """Get quiz by ID"""
        with self.db_session() as session:
            return session.query(Quiz).filter(Quiz.QuizID == quiz_id).first()
    
    def get_quizzes_by_module(self, module_id: str) -> List[Quiz]:
        """Get all quizzes for a module"""
        with self.db_session() as session:
            return session.query(Quiz).filter(Quiz.ModuleID == module_id).all()
    
    def get_all_quizzes(self) -> List[Quiz]:
        """Get all quizzes"""
        with self.db_session() as session:
            return session.query(Quiz).all()
    
    def update_quiz(self, quiz_id: str, update_data: Dict[str, Any]) -> Optional[Quiz]:
        """Update quiz information"""
        with self.db_session() as session:
            quiz = session.query(Quiz).filter(Quiz.QuizID == quiz_id).first()
            if not quiz:
                return None
            
            for key, value in update_data.items():
                if hasattr(quiz, key):
                    setattr(quiz, key, value)
            
            session.commit()
            session.refresh(quiz)
            return quiz
    
    def delete_quiz(self, quiz_id: str) -> bool:
        """Delete a quiz"""
        with self.db_session() as session:
            quiz = session.query(Quiz).filter(Quiz.QuizID == quiz_id).first()
            if not quiz:
                return False
            
            session.delete(quiz)
            session.commit()
            return True
    
    def get_overdue_quizzes(self) -> List[Quiz]:
        """Get all quizzes past their deadline"""
        with self.db_session() as session:
            return session.query(Quiz).filter(
                Quiz.Deadline < datetime.utcnow()
            ).all()
    
    def get_upcoming_quizzes(self, days: int = 7) -> List[Quiz]:
        """Get quizzes due within specified days"""
        with self.db_session() as session:
            future_date = datetime.utcnow() + timedelta(days=days)
            return session.query(Quiz).filter(
                Quiz.Deadline <= future_date,
                Quiz.Deadline >= datetime.utcnow()
            ).all()


class QuestionService:
    """Service for Question CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries: int = 50):
        self.db_session = db_session
        self.max_retries = max_retries
    
    def create_question(self, question_data: Dict[str, Any]) -> Question:
        """Create a new question"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, Question.QuestionID)
            question_data["QuestionID"] = new_id
            with self.db_session() as session:
                try:
                    question = Question(**question_data)
                    session.add(question)
                    session.commit()
                    session.refresh(question)
                    return question
                except IntegrityError:
                    session.rollback()
                    continue
                except Exception as e:
                    session.rollback()
                    raise ValueError(f"Error creating question: {str(e)}")
        raise Exception(f"Failed to generate unique ID for {Question.__name__} after {self.max_retries} attempts.")
    
    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Get question by ID"""
        with self.db_session() as session:
            return session.query(Question).filter(Question.QuestionID == question_id).first()
    
    def get_questions_by_quiz(self, quiz_id: str) -> List[Question]:
        """Get all questions for a quiz"""
        with self.db_session() as session:
            return session.query(Question).filter(Question.QuizID == quiz_id).all()
    
    def update_question(self, question_id: str, update_data: Dict[str, Any]) -> Optional[Question]:
        """Update question information"""
        with self.db_session() as session:
            question = session.query(Question).filter(Question.QuestionID == question_id).first()
            if not question:
                return None
            
            for key, value in update_data.items():
                if hasattr(question, key):
                    setattr(question, key, value)
            
            session.commit()
            session.refresh(question)
            return question
    
    def delete_question(self, question_id: str) -> bool:
        """Delete a question"""
        with self.db_session() as session:
            question = session.query(Question).filter(Question.QuestionID == question_id).first()
            if not question:
                return False
            
            session.delete(question)
            session.commit()
            return True
    
    def get_question_count(self, quiz_id: str) -> int:
        """Get the number of questions in a quiz"""
        with self.db_session() as session:
            return session.query(Question).filter(Question.QuizID == quiz_id).count()


class AnswerService:
    """Service for Answer CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries: int = 50):
        self.db_session = db_session
        self.max_retries = max_retries
    
    def create_answer(self, answer_data: Dict[str, Any]) -> Answer:
        """Create a new answer option"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, Answer.AnswerID)
            answer_data["AnswerID"] = new_id
            with self.db_session() as session:
                try:
                    answer = Answer(**answer_data)
                    session.add(answer)
                    session.commit()
                    session.refresh(answer)
                    return answer
                except IntegrityError:
                    session.rollback()
                    continue
                except Exception as e:
                    session.rollback()
                    raise ValueError(f"Error creating answer: {str(e)}")
        raise Exception(f"Failed to generate unique ID for {Answer.__name__} after {self.max_retries} attempts.")
    
    def get_answer_by_id(self, question_id: str, quiz_id: str, answer_id: str) -> Optional[Answer]:
        """Get answer by composite key"""
        with self.db_session() as session:
            return session.query(Answer).filter(
                Answer.QuestionID == question_id,
                Answer.QuizID == quiz_id,
                Answer.AnswerID == answer_id
            ).first()
    
    def get_answers_by_question(self, question_id: str, quiz_id: str) -> List[Answer]:
        """Get all answers for a question"""
        with self.db_session() as session:
            return session.query(Answer).filter(
                Answer.QuestionID == question_id,
                Answer.QuizID == quiz_id
            ).all()
    
    def update_answer(self, question_id: str, quiz_id: str, answer_id: str, 
                      update_data: Dict[str, Any]) -> Optional[Answer]:
        """Update answer information"""
        with self.db_session() as session:
            answer = session.query(Answer).filter(
                Answer.QuestionID == question_id,
                Answer.QuizID == quiz_id,
                Answer.AnswerID == answer_id
            ).first()
            
            if not answer:
                return None
            
            for key, value in update_data.items():
                if hasattr(answer, key):
                    setattr(answer, key, value)
            
            session.commit()
            session.refresh(answer)
            return answer
    
    def delete_answer(self, question_id: str, quiz_id: str, answer_id: str) -> bool:
        """Delete an answer"""
        with self.db_session() as session:
            answer = session.query(Answer).filter(
                Answer.QuestionID == question_id,
                Answer.QuizID == quiz_id,
                Answer.AnswerID == answer_id
            ).first()
            
            if not answer:
                return False
            
            session.delete(answer)
            session.commit()
            return True
    
    def delete_all_answers_for_question(self, question_id: str, quiz_id: str) -> bool:
        """Delete all answers for a question"""
        with self.db_session() as session:
            answers = session.query(Answer).filter(
                Answer.QuestionID == question_id,
                Answer.QuizID == quiz_id
            ).all()
            
            if not answers:
                return False
            
            for answer in answers:
                session.delete(answer)
            
            session.commit()
            return True


class AssignSubmissionService:
    """Service for Assignment Submission CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries: int = 50):
        self.db_session = db_session
        self.max_retries = max_retries
    
    def create_submission(self, submission_data: Dict[str, Any]) -> AssignSubmission:
        """Create a new assignment submission"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, AssignSubmission.SubID)
            submission_data["SubID"] = new_id
            with self.db_session() as session:
                try:
                    submission = AssignSubmission(**submission_data)
                    session.add(submission)
                    session.commit()
                    session.refresh(submission)
                    return submission
                except IntegrityError:
                    session.rollback()
                    continue
                except Exception as e:
                    session.rollback()
                    raise ValueError(f"Error creating submission: {str(e)}")
        raise Exception(f"Failed to generate unique ID for {AssignSubmission.__name__} after {self.max_retries} attempts.")
    
    def get_submission_by_id(self, sub_id: str) -> Optional[AssignSubmission]:
        """Get submission by ID"""
        with self.db_session() as session:
            return session.query(AssignSubmission).filter(AssignSubmission.SubID == sub_id).first()
    
    def get_submissions_by_assignment(self, ass_id: str) -> List[AssignSubmission]:
        """Get all submissions for an assignment"""
        with self.db_session() as session:
            return session.query(AssignSubmission).filter(AssignSubmission.AssID == ass_id).all()
    
    def get_submissions_by_user(self, user_id: str) -> List[AssignSubmission]:
        """Get all submissions by a user"""
        with self.db_session() as session:
            return session.query(AssignSubmission).filter(AssignSubmission.UserID == user_id).all()
    
    def get_user_submission_for_assignment(self, user_id: str, ass_id: str) -> Optional[AssignSubmission]:
        """Get a specific user's submission for an assignment"""
        with self.db_session() as session:
            return session.query(AssignSubmission).filter(
                AssignSubmission.UserID == user_id,
                AssignSubmission.AssID == ass_id
            ).first()
    
    def update_submission(self, sub_id: str, update_data: Dict[str, Any]) -> Optional[AssignSubmission]:
        """Update submission information"""
        with self.db_session() as session:
            submission = session.query(AssignSubmission).filter(AssignSubmission.SubID == sub_id).first()
            if not submission:
                return None
            
            for key, value in update_data.items():
                if hasattr(submission, key):
                    setattr(submission, key, value)
            
            session.commit()
            session.refresh(submission)
            return submission
    
    def grade_submission(self, sub_id: str, grade: float) -> Optional[AssignSubmission]:
        """Grade an assignment submission"""
        with self.db_session() as session:
            submission = session.query(AssignSubmission).filter(AssignSubmission.SubID == sub_id).first()
            if not submission:
                return None
            
            submission.Grade = grade
            session.commit()
            session.refresh(submission)
            return submission
    
    def delete_submission(self, sub_id: str) -> bool:
        """Delete a submission"""
        with self.db_session() as session:
            submission = session.query(AssignSubmission).filter(AssignSubmission.SubID == sub_id).first()
            if not submission:
                return False
            
            session.delete(submission)
            session.commit()
            return True
    
    def get_graded_submissions(self, ass_id: str) -> List[AssignSubmission]:
        """Get all graded submissions for an assignment"""
        with self.db_session() as session:
            return session.query(AssignSubmission).filter(
                AssignSubmission.AssID == ass_id,
                AssignSubmission.Grade.isnot(None)
            ).all()
    
    def get_ungraded_submissions(self, ass_id: str) -> List[AssignSubmission]:
        """Get all ungraded submissions for an assignment"""
        with self.db_session() as session:
            return session.query(AssignSubmission).filter(
                AssignSubmission.AssID == ass_id,
                AssignSubmission.Grade.is_(None)
            ).all()


class QuizSubmissionService:
    """Service for Quiz Submission CRUD operations"""
    
    def __init__(self, db_session: sessionmaker, max_retries: int = 50):
        self.db_session = db_session
        self.max_retries = max_retries
    
    def create_submission(self, submission_data: Dict[str, Any]) -> QuizSubmission:
        """Create a new quiz submission"""
        for attempt in range(self.max_retries):
            new_id = generate_id(self.db_session, QuizSubmission.SubID)
            submission_data["SubID"] = new_id
            with self.db_session() as session:
                try:
                    submission = QuizSubmission(**submission_data)
                    session.add(submission)
                    session.commit()
                    session.refresh(submission)
                    return submission
                except IntegrityError:
                    session.rollback()
                    continue
                except Exception as e:
                    session.rollback()
                    raise ValueError(f"Error creating quiz submission: {str(e)}")
        raise Exception(f"Failed to generate unique ID for {QuizSubmission.__name__} after {self.max_retries} attempts.")
    
    def get_submission_by_id(self, sub_id: str) -> Optional[QuizSubmission]:
        """Get submission by ID"""
        with self.db_session() as session:
            return session.query(QuizSubmission).filter(QuizSubmission.SubID == sub_id).first()
    
    def get_submissions_by_quiz(self, quiz_id: str) -> List[QuizSubmission]:
        """Get all submissions for a quiz"""
        with self.db_session() as session:
            return session.query(QuizSubmission).filter(QuizSubmission.QuizID == quiz_id).all()
    
    def get_submissions_by_user(self, user_id: str) -> List[QuizSubmission]:
        """Get all quiz submissions by a user"""
        with self.db_session() as session:
            return session.query(QuizSubmission).filter(QuizSubmission.UserID == user_id).all()
    
    def get_user_submissions_for_quiz(self, user_id: str, quiz_id: str) -> List[QuizSubmission]:
        """Get all attempts by a user for a specific quiz"""
        with self.db_session() as session:
            return session.query(QuizSubmission).filter(
                QuizSubmission.UserID == user_id,
                QuizSubmission.QuizID == quiz_id
            ).all()
    
    def get_attempt_count(self, user_id: str, quiz_id: str) -> int:
        """Get number of attempts by a user for a quiz"""
        with self.db_session() as session:
            return session.query(QuizSubmission).filter(
                QuizSubmission.UserID == user_id,
                QuizSubmission.QuizID == quiz_id
            ).count()
    
    def get_best_score(self, user_id: str, quiz_id: str) -> Optional[float]:
        """Get the best score for a user on a quiz"""
        with self.db_session() as session:
            submissions = session.query(QuizSubmission).filter(
                QuizSubmission.UserID == user_id,
                QuizSubmission.QuizID == quiz_id,
                QuizSubmission.Grade.isnot(None)
            ).all()
            
            if not submissions:
                return None
            
            return max(sub.Grade for sub in submissions)
    
    def update_submission(self, sub_id: str, update_data: Dict[str, Any]) -> Optional[QuizSubmission]:
        """Update submission information"""
        with self.db_session() as session:
            submission = session.query(QuizSubmission).filter(QuizSubmission.SubID == sub_id).first()
            if not submission:
                return None
            
            for key, value in update_data.items():
                if hasattr(submission, key):
                    setattr(submission, key, value)
            
            session.commit()
            session.refresh(submission)
            return submission
    
    def grade_submission(self, sub_id: str, grade: float) -> Optional[QuizSubmission]:
        """Grade a quiz submission"""
        with self.db_session() as session:
            submission = session.query(QuizSubmission).filter(QuizSubmission.SubID == sub_id).first()
            if not submission:
                return None
            
            submission.Grade = grade
            session.commit()
            session.refresh(submission)
            return submission
    
    def delete_submission(self, sub_id: str) -> bool:
        """Delete a quiz submission"""
        with self.db_session() as session:
            submission = session.query(QuizSubmission).filter(QuizSubmission.SubID == sub_id).first()
            if not submission:
                return False
            
            session.delete(submission)
            session.commit()
            return True
    
    def get_average_score(self, quiz_id: str) -> Optional[float]:
        """Get average score for a quiz"""
        with self.db_session() as session:
            result = session.query(func.avg(QuizSubmission.Grade)).filter(
                QuizSubmission.QuizID == quiz_id,
                QuizSubmission.Grade.isnot(None)
            ).scalar()
            
            return float(result) if result else None