from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from ..core import *
from fastapi import Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from .auth import *

router = APIRouter()


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

