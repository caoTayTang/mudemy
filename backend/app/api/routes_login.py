from fastapi import APIRouter, Body
from ..models import*
from ..services import*
from fastapi.responses import JSONResponse
from ..core import*
from fastapi import Depends, HTTPException, status, Cookie, Response
from datetime import datetime, timezone, timedelta
import uuid
from ..hcmut_database import*

logger = get_logger("LOGIN")
router = APIRouter()
user_service = UserService(mututor_session)

@router.get("/roles")
def get_role():
    return [
            { 'id': 'TUTOR', 'label': 'tutor', 'description': 'Dành cho sinh viên muốn dạy kèm' },
            { 'id': 'TUTEE', 'label': 'tutee', 'description': 'Dành cho sinh viên cần học thêm' },
            { 'id': 'ADMIN', 'label': 'admin', 'description': 'Quản trị hệ thống' },
         ]

@router.post("/login")
def login(
    response: Response, 
    data: dict = Body(...), 
):
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    
    #logger.info(role.__len__())
    if not hcmut_api.check_password(username, password) :
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    user = hcmut_api.get_user_by_username(username)
    user_id = user.id
    if role.lower() == 'tutor' or role.lower() == 'admin':
        mu_user = user_service.get_by_id(user_id)
        if not mu_user or mu_user.role != role:
            raise HTTPException(
            status_code=403,
            detail=f"You don't have permission to login as {role}",
        )

    session = MuSession(
        session_id=str(uuid.uuid4()),
        user_id=user.id,
        role= UserRole(role.lower()),
        expires_at= datetime.now(timezone.utc) + timedelta(hours=1)
    )
    db = mututor_session()

    old_session = db.query(MuSession).filter(MuSession.user_id == user_id).first()
    if old_session:
        db.delete(old_session)
        db.commit()

    db.add(session)
    db.commit()
    db.close()

    response.set_cookie(
        key="session_id",
        value=session.session_id,
        httponly=True,  
        secure=True,    
        samesite="lax"  
    )
    
    return {"username": user.username, "role": role, "status": "Login successful"}

@router.post("/logout")
def logout(
    response: Response,
    session_id: str | None = Cookie(None), 
):
    db = mututor_session()
    if session_id:
        session = db.query(MuSession).filter(MuSession.session_id == session_id).first()
        if session:
            db.delete(session)
            db.commit()

    db.close()
    response.delete_cookie(key="session_id")
    return {"status": "Logout successful"}

