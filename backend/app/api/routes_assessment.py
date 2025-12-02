from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from sqlalchemy import text

from ..models import mudemy_session
from ..services import (
    AssignmentService,
    QuizService,
    QuestionService,
    AnswerService,
    AssignSubmissionService,
    QuizSubmissionService,
    ModuleService,
)
from .auth import get_current_user_from_session, CurrentUser

router = APIRouter()

# Initialize services
assignment_service = AssignmentService(mudemy_session)
quiz_service = QuizService(mudemy_session)
question_service = QuestionService(mudemy_session)
answer_service = AnswerService(mudemy_session)
assign_submission_service = AssignSubmissionService(mudemy_session)
quiz_submission_service = QuizSubmissionService(mudemy_session)
module_service = ModuleService(mudemy_session)

# ============================================================
# ASSIGNMENT ROUTES
# ============================================================

@router.post("/assignments")
def create_assignment(
    data: Dict[str, Any] = Body(...), 
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Create a new assignment (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    try:
        assignment = assignment_service.create_assignment(data)
        return JSONResponse(status_code=201, content={"status": "created", "assignment_id": assignment.AssID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/assignments/{ass_id}")
def read_assignment(
    ass_id: str, 
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
	assignment = assignment_service.get_assignment_by_id(ass_id)
	if not assignment:
		raise HTTPException(status_code=404, detail="Assignment not found")
	return {
		"status": "success",
		"assignment": {
			"AssID": assignment.AssID,
			"Deadline": assignment.Deadline,
			"Description": assignment.Description,
			"Title": assignment.Title,
			"ModuleID": assignment.ModuleID
		}
	}

@router.put("/assignments/{ass_id}")
def update_assignment(
    ass_id: str,
    data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    """Update an assignment's details (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    updated = assignment_service.update_assignment(ass_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"status": "updated", "assignment_id": updated.AssID}

@router.delete("/assignments/{ass_id}")
def delete_assignment(
    ass_id: str, 
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Delete an assignment (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    ok = assignment_service.delete_assignment(ass_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"status": "deleted", "ass_id": ass_id}

@router.get("/modules/{module_id}/assignments")
def get_assignments_by_module(
    module_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
	assignments = assignment_service.get_assignments_by_module(module_id)
	return {
		"status": "success",
		"count": len(assignments),
		"assignments": [{
			"AssID": a.AssID,
			"Deadline": a.Deadline,
			"Description": a.Description,
			"Title": a.Title,
			"ModuleID": a.ModuleID
		} for a in assignments]
	}

# ============================================================
# QUIZ ROUTES
# ============================================================

@router.post("/quizzes")
def create_quiz(
    data: Dict[str, Any] = Body(...), 
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Create a new quiz (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    try:
        quiz = quiz_service.create_quiz(data)
        return JSONResponse(status_code=201, content={"status": "created", "quiz_id": quiz.QuizID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/quizzes/{quiz_id}")
def read_quiz(
    quiz_id: str, 
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
	quiz = quiz_service.get_quiz_by_id(quiz_id)
	if not quiz:
		raise HTTPException(status_code=404, detail="Quiz not found")
	return {
		"status": "success",
		"quiz": {
			"QuizID": quiz.QuizID,
			"Time_limit": quiz.Time_limit,
			"Num_attempt": quiz.Num_attempt,
			"Deadline": quiz.Deadline,
			"Title": quiz.Title,
			"ModuleID": quiz.ModuleID
		}
	}
    
@router.put("/quizzes/{quiz_id}")
def update_quiz(
    quiz_id: str,
    data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    """Update a quiz's details (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    updated = quiz_service.update_quiz(quiz_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"status": "updated", "quiz_id": updated.QuizID}

@router.delete("/quizzes/{quiz_id}")
def delete_quiz(
    quiz_id: str, 
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Delete a quiz (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    ok = quiz_service.delete_quiz(quiz_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"status": "deleted", "quiz_id": quiz_id}

@router.get("/modules/{module_id}/quizzes")
def get_quizzes_by_module(
    module_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
	quizzes = quiz_service.get_quizzes_by_module(module_id)
	return {
		"status": "success",
		"count": len(quizzes),
		"quizzes": [{
			"QuizID": q.QuizID,
			"Time_limit": q.Time_limit,
			"Num_attempt": q.Num_attempt,
			"Deadline": q.Deadline,
			"Title": q.Title,
			"ModuleID": q.ModuleID
		} for q in quizzes]
	}

# ============================================================
# QUESTION & ANSWER ROUTES
# ============================================================

@router.post("/quizzes/{quiz_id}/questions")
def create_question(
    quiz_id: str,
    data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Add a new question to a quiz (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    data["QuizID"] = quiz_id
    try:
        question = question_service.create_question(data)
        return JSONResponse(status_code=201, content={"status": "created", "question_id": question.QuestionID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/quizzes/{quiz_id}/questions")
def get_questions_for_quiz(
    quiz_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
	questions = question_service.get_questions_by_quiz(quiz_id)
	return {
		"status": "success",
		"count": len(questions),
		"questions": [{
			"QuestionID": q.QuestionID,
			"QuizID": q.QuizID,
			"Correct_answer": q.Correct_answer,
			"Content": q.Content
		} for q in questions]
	}

@router.put("/quizzes/{quiz_id}/questions/{question_id}")
def update_question(
    quiz_id: str,
    question_id: str,
    data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    """Update a question (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    q = question_service.get_question_by_id(question_id)
    if not q or q.QuizID != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found for this quiz")

    updated = question_service.update_question(question_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"status": "updated", "question_id": updated.QuestionID}


@router.delete("/quizzes/{quiz_id}/questions/{question_id}")
def delete_question(
    quiz_id: str,
    question_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    """Delete a question from a quiz (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    q = question_service.get_question_by_id(question_id)
    if not q or q.QuizID != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found for this quiz")

    ok = question_service.delete_question(question_id)
    if not ok:
        raise HTTPException(status_code=400, detail="Could not delete question")
    return {"status": "deleted", "question_id": question_id}

@router.post("/questions/{question_id}/answers")
def create_answer(
    question_id: str,
    data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Add a possible answer to a question (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    question = question_service.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
        
    data["QuestionID"] = question_id
    data["QuizID"] = question.QuizID
    try:
        answer = answer_service.create_answer(data)
        return JSONResponse(status_code=201, content={"status": "created", "answer_id": answer.AnswerID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/questions/{question_id}/answers")
def get_answers_for_question(
    question_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
	question = question_service.get_question_by_id(question_id)
	if not question:
		raise HTTPException(status_code=404, detail="Question not found")
		
	answers = answer_service.get_answers_by_question(question_id, question.QuizID)
	return {
		"status": "success",
		"count": len(answers),
		"answers": [{
			"QuestionID": a.QuestionID,
			"QuizID": a.QuizID,
			"AnswerID": a.AnswerID,
			"Answer": a.Answer
		} for a in answers]
	}

@router.put("/quizzes/{quiz_id}/questions/{question_id}/answers/{answer_id}")
def update_answer(
    quiz_id: str,
    question_id: str,
    answer_id: str,
    data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    """Update an answer (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    question = question_service.get_question_by_id(question_id)
    if not question or question.QuizID != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found for this quiz")

    updated = answer_service.update_answer(question_id, quiz_id, answer_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Answer not found")
    return {"status": "updated", "answer_id": updated.AnswerID}


@router.delete("/quizzes/{quiz_id}/questions/{question_id}/answers/{answer_id}")
def delete_answer(
    quiz_id: str,
    question_id: str,
    answer_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    """Delete an answer (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    question = question_service.get_question_by_id(question_id)
    if not question or question.QuizID != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found for this quiz")

    ok = answer_service.delete_answer(question_id, quiz_id, answer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Answer not found or could not be deleted")
    return {"status": "deleted", "answer_id": answer_id}

# ============================================================
# SUBMISSION ROUTES
# ============================================================

@router.post("/assignments/{ass_id}/submit")
def submit_assignment(
    ass_id: str,
    data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Submit work for an assignment (Student only)"""
    if current_user.role != 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires STUDENT role")
    
    data["UserID"] = current_user.user_id
    data["AssID"] = ass_id
    try:
        submission = assign_submission_service.create_submission(data)
        return JSONResponse(status_code=201, content={"status": "submitted", "submission_id": submission.SubID})
    except ValueError as e:
        # This will catch DB-level errors, but deadline is checked by a trigger
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/assignments/{ass_id}/submissions")
def get_assignment_submissions(
    ass_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	submissions = assign_submission_service.get_submissions_by_assignment(ass_id)
	return {
		"status": "success",
		"count": len(submissions),
		"submissions": [{
			"SubID": s.SubID,
			"UserID": s.UserID,
			"AssID": s.AssID,
			"Sub_content": s.Sub_content,
			"Grade": s.Grade,
			"Sub_date": s.Sub_date
		} for s in submissions]
	}
    
@router.put("/submissions/assignment/{sub_id}/grade")
def grade_assignment_submission(
    sub_id: str,
    data: Dict[str, float] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Grade a student's assignment submission (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    grade = data.get("grade")
    if grade is None:
        raise HTTPException(status_code=400, detail="Grade not provided")

    submission = assign_submission_service.grade_submission(sub_id, grade)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"status": "graded", "submission_id": sub_id, "grade": submission.Grade}

@router.post("/quizzes/{quiz_id}/submit")
def submit_quiz(
    quiz_id: str,
    data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Submit answers for a quiz (Student only)"""
    if current_user.role != 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires STUDENT role")

    data["UserID"] = current_user.user_id
    data["QuizID"] = quiz_id
    try:
        submission = quiz_submission_service.create_submission(data)
        return JSONResponse(status_code=201, content={"status": "submitted", "submission_id": submission.SubID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/quizzes/{quiz_id}/submissions")
def get_quiz_submissions(
    quiz_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	submissions = quiz_submission_service.get_submissions_by_quiz(quiz_id)
	return {
		"status": "success",
		"count": len(submissions),
		"submissions": [{
			"SubID": s.SubID,
			"UserID": s.UserID,
			"QuizID": s.QuizID,
			"Sub_content": s.Sub_content,
			"Grade": s.Grade,
			"Sub_date": s.Sub_date
		} for s in submissions]
	}
    
@router.put("/submissions/quiz/{sub_id}/grade")
def grade_quiz_submission(
    sub_id: str,
    data: Dict[str, float] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Grade a student's quiz submission (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    grade = data.get("grade")
    if grade is None:
        raise HTTPException(status_code=400, detail="Grade not provided")

    submission = quiz_submission_service.grade_submission(sub_id, grade)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"status": "graded", "submission_id": sub_id, "grade": submission.Grade}

@router.get("/quizzes/{quiz_id}/submissions/latest")
def get_latest_quiz_submissions(
    quiz_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    """Return the latest submission per student for a quiz (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    sql = text("""
        SELECT qs.SubID, qs.UserID, qs.QuizID, qs.Grade, qs.Sub_date, qs.Sub_content
        FROM QUIZ_SUBMISSION qs
        JOIN (
            SELECT UserID, MAX(Sub_date) AS max_sub_date
            FROM QUIZ_SUBMISSION
            WHERE QuizID = :quiz_id
            GROUP BY UserID
        ) latest ON qs.UserID = latest.UserID AND qs.Sub_date = latest.max_sub_date
        WHERE qs.QuizID = :quiz_id
    """)

    with mudemy_session() as session:
        rows = session.execute(sql, {"quiz_id": quiz_id}).fetchall()
        submissions = [
            {"SubID": r[0], "UserID": r[1], "QuizID": r[2], "Grade": r[3], "Sub_date": r[4], "Sub_content": r[5]}
            for r in rows
        ]
        return {"status": "success", "count": len(submissions), "submissions": submissions}


@router.get("/assignments/{ass_id}/submissions/latest")
def get_latest_assignment_submissions(
    ass_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    """Return the latest submission per student for an assignment (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    sql = text("""
        SELECT s.SubID, s.UserID, s.AssID, s.Grade, s.Sub_date, s.Sub_content
        FROM ASSIGN_SUBMISSION s
        JOIN (
            SELECT UserID, MAX(Sub_date) AS max_sub_date
            FROM ASSIGN_SUBMISSION
            WHERE AssID = :ass_id
            GROUP BY UserID
        ) latest ON s.UserID = latest.UserID AND s.Sub_date = latest.max_sub_date
        WHERE s.AssID = :ass_id
    """)

    with mudemy_session() as session:
        rows = session.execute(sql, {"ass_id": ass_id}).fetchall()
        submissions = [
            {"SubID": r[0], "UserID": r[1], "AssID": r[2], "Grade": r[3], "Sub_date": r[4], "Sub_content": r[5]}
            for r in rows
        ]
        return {"status": "success", "count": len(submissions), "submissions": submissions}

# ============================================================
# STATS ROUTES (from SQL Procedures)
# ============================================================

@router.get("/modules/{module_id}/quiz-stats")
def get_quiz_performance_stats(
    module_id: str,
    min_submissions: int = Query(1, ge=0),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """
    Get performance statistics for all quizzes in a module.
    Calls the `GetQuizPerformanceStats` stored procedure.
    (Instructor only)
    """
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    if not module_service.get_module_by_id(module_id):
        raise HTTPException(status_code=404, detail=f"Module with id <{module_id}> does not exist.")

    with mudemy_session() as session:
        try:
            query = text("EXEC GetQuizPerformanceStats @ModuleID=:module_id, @MinSubmissions=:min_submissions")
            result = session.execute(query, {"module_id": module_id, "min_submissions": min_submissions}).fetchall()
            
            stats = [
                {
                    "QuizID": row[0],
                    "QuizTitle": row[1],
                    "AverageGrade": row[2],
                    "HighestGrade": row[3],
                    "LowestGrade": row[4],
                    "TotalSubmissions": row[5]
                } for row in result
            ]
            return {"status": "success", "stats": stats}
        except Exception as e:
            # Catch potential exceptions from the stored procedure (e.g., THROW)
            raise HTTPException(status_code=500, detail=f"Database procedure error: {str(e)}")
