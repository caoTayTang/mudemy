from fastapi import APIRouter, Body
from ..models import *
from ..services import *
from fastapi.responses import JSONResponse
from ..core import *
from fastapi import Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from .auth import get_current_user_from_session

router = APIRouter()

feedback_service = FeedbackService(mututor_session)
session_evaluation_service = SessionEvaluationService(mututor_session)
enrollment_service = EnrollmentService(mututor_session)
course_service = CourseService(mututor_session)
course_session_service = CourseSessionService(mututor_session)

@router.get("/feedback")
def get_feedback(
    current_user: MuSession = Depends(get_current_user_from_session),
    topic: str | None = None
):
    """Get all feedback (admin/tutor only)"""
    if current_user.role != UserRole('tutor') and current_user.role != UserRole('admin'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR or ADMIN role")
    
    try:
        if topic:
            feedbacks = feedback_service.get_by_topic(topic)
        else:
            feedbacks = feedback_service.get_all()
        
        feedback_data = []
        for feedback in feedbacks:
            feedback_data.append({
                "id": feedback.id,
                "user_id": feedback.user_id if not feedback.is_anonymous else None,
                "topic": feedback.topic,
                "content": feedback.content,
                "is_anonymous": feedback.is_anonymous,
                "created_at": feedback.created_at.isoformat()
            })
        
        return {
            "status": "success",
            "count": len(feedback_data),
            "feedback": feedback_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get feedback: {str(e)}")

@router.get("/feedback/topics")
def get_feedback_topics(
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Get all unique feedback topics"""
    if current_user.role != UserRole('tutor') and current_user.role != UserRole('admin'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR or ADMIN role")
    
    try:
        feedbacks = feedback_service.get_all()
        topics = list(set([f.topic for f in feedbacks]))
        
        return {
            "status": "success",
            "topics": topics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get feedback topics: {str(e)}")

@router.post("/feedback")
def create_feedback(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Create new feedback (any authenticated user)"""
    feedback_data = data.get('feedbackData')
    
    if not feedback_data:
        raise HTTPException(status_code=400, detail="Missing feedbackData")
    
    topic = feedback_data.get('topic')
    content = feedback_data.get('content')
    is_anonymous = feedback_data.get('isAnonymous', False)
    
    if not topic or not content:
        raise HTTPException(status_code=400, detail="Missing required fields: topic and content")
    
    try:
        feedback = feedback_service.create(
            user_id=current_user.user_id if not is_anonymous else "xxxxxxx",
            topic=topic,
            content=content,
            is_anonymous=is_anonymous
        )
        
        return {
            "status": "success",
            "message": "Feedback submitted successfully",
            "feedback": {
                "id": feedback.id,
                "topic": feedback.topic,
                "is_anonymous": feedback.is_anonymous,
                "created_at": feedback.created_at.isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create feedback: {str(e)}")

@router.post("/session-evaluations")
def create_session_evaluation(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Create evaluation for a course session (tutee only)"""
    if current_user.role != UserRole('tutee'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTEE role")
    
    evaluation_data = data.get('evaluationData')
    
    if not evaluation_data:
        raise HTTPException(status_code=400, detail="Missing evaluationData")
    
    session_id = evaluation_data.get('sessionId')
    course_id = evaluation_data.get('courseId')
    rating = evaluation_data.get('rating')
    comment = evaluation_data.get('comment')
    is_anonymous = evaluation_data.get('isAnonymous', False)
    
    if not session_id or not rating:
        raise HTTPException(status_code=400, detail="Missing required fields: sessionId and rating")
    
    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    try:

        enrollment = enrollment_service.get_by_tutee_and_course(current_user.user_id, course_id)
        if not enrollment or enrollment.status != EnrollmentStatus.ENROLLED:
            raise HTTPException(status_code=403, detail="You must be enrolled in this course to evaluate sessions")   

        session = course_session_service.get_by_course_snum(course_id, session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        existing_evaluations = session_evaluation_service.get_by_enrollment(enrollment.id)
        for eval in existing_evaluations:
            if eval.session_id == session_id:
                raise HTTPException(status_code=400, detail="You have already evaluated this session")
        
        evaluation = session_evaluation_service.create(
            session_id=session.id,
            enrollment_id=enrollment.id,
            rating=rating,
            comment=comment,
            is_anonymous=is_anonymous
        )
        
        return {
            "status": "success",
            "message": "Session evaluation submitted successfully",
            "evaluation": {
                "id": evaluation.id,
                "session_id": evaluation.session_id,
                "rating": evaluation.rating,
                "created_at": evaluation.created_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session evaluation: {str(e)}")

@router.get("/session-evaluations/course/{course_id}")
def get_course_evaluations(
    course_id: int,
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Get all evaluations for a course (tutor only for their courses)"""
    if current_user.role != UserRole('tutor') and current_user.role != UserRole('admin'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR or ADMIN role")
    
    try:
        course = course_service.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        if current_user.role == UserRole('tutor') and course.tutor_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="You can only view evaluations for your own courses")
        
        sessions = course_session_service.get_by_course(course_id)
        
        all_evaluations = []
        for session in sessions:
            evaluations = session_evaluation_service.get_by_session(session.id)
            for evaluation in evaluations:
                all_evaluations.append({
                    "id": evaluation.id,
                    "session_id": evaluation.session_id,
                    "session_number": session.session_number,
                    "rating": evaluation.rating,
                    "comment": evaluation.comment,
                    "is_anonymous": evaluation.is_anonymous,
                    "created_at": evaluation.created_at.isoformat()
                })
        
        avg_rating = sum([e['rating'] for e in all_evaluations]) / len(all_evaluations) if all_evaluations else 0
        
        return {
            "status": "success",
            "course_id": course_id,
            "course_title": course.title,
            "total_evaluations": len(all_evaluations),
            "average_rating": round(avg_rating, 2),
            "evaluations": all_evaluations
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get course evaluations: {str(e)}")