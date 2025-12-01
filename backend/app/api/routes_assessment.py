from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from .auth import *
from typing import Dict, Any
from ..models import mudemy_session
from ..services import (
	AssignmentService,
	QuizService,
	AssignSubmissionService,
	QuizSubmissionService,
)

router = APIRouter()

assignment_service = AssignmentService(mudemy_session)
quiz_service = QuizService(mudemy_session)
assign_sub_service = AssignSubmissionService(mudemy_session)
quiz_sub_service = QuizSubmissionService(mudemy_session)


@router.post("/assignments")
def create_assignment(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

	a = assignment_service.create_assignment(data)
	return JSONResponse(status_code=201, content={"status": "created", "ass_id": a.AssID})


@router.get("/assignments/{ass_id}")
def read_assignment(ass_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	ass = assignment_service.get_assignment_by_id(ass_id)
	if not ass:
		raise HTTPException(status_code=404, detail="Assignment not found")
	return {"status": "success", "assignment": {"AssID": ass.AssID}}


@router.delete("/assignments/{ass_id}")
def delete_assignment(ass_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

	ok = assignment_service.delete_assignment(ass_id)
	if not ok:
		raise HTTPException(status_code=404, detail="Assignment not found")
	return {"status": "deleted", "ass_id": ass_id}


@router.post("/quizzes")
def create_quiz(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

	q = quiz_service.create_quiz(data)
	return JSONResponse(status_code=201, content={"status": "created", "quiz_id": q.QuizID})


@router.get("/quizzes/{quiz_id}")
def read_quiz(quiz_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	q = quiz_service.get_quiz_by_id(quiz_id)
	if not q:
		raise HTTPException(status_code=404, detail="Quiz not found")
	return {"status": "success", "quiz": {"QuizID": q.QuizID}}


@router.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

	ok = quiz_service.delete_quiz(quiz_id)
	if not ok:
		raise HTTPException(status_code=404, detail="Quiz not found")
	return {"status": "deleted", "quiz_id": quiz_id}

