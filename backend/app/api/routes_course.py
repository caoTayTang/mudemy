from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from ..core import *
from fastapi import Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from .auth import *
from typing import Dict, Any
from ..models import mudemy_session
from ..services import CourseService
router = APIRouter()

course_service = CourseService(mudemy_session)



@router.get("/tutor/courses")
def get_courses(
   current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get all courses for the current tutor"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    return {
        "status": "success",
        "tutor": current_user.user_id,
    }


# Simple CRUD for courses



@router.post("/courses")
def create_course(
    course_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session),
):
    # only instructors may create courses
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    course = course_service.create_course(course_data)
    return JSONResponse(status_code=201, content={"status": "created", "course_id": course.CourseID})


@router.get("/courses/{course_id}")
def read_course(course_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"status": "success", "course": {"CourseID": course.CourseID, "Title": getattr(course, 'Title', None)}}


@router.put("/courses/{course_id}")
def update_course(course_id: str, update_data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    course = course_service.update_course(course_id, update_data)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"status": "updated", "course_id": course.CourseID}


@router.delete("/courses/{course_id}")
def delete_course(course_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

    ok = course_service.delete_course(course_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"status": "deleted", "course_id": course_id}

