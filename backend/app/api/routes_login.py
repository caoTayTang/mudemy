from fastapi import APIRouter, Body, Response, HTTPException
from ..models import *
from ..services import *
from ..core import *
from .auth import create_access_token 
# No need for uuid or datetime imports here anymore

logger = get_logger("LOGIN")
router = APIRouter()
user_service = UserService(mudemy_session)

@router.get("/roles")
def get_role():
    return [
            { 'id': 'TUTOR', 'label': 'tutor', 'description': 'Dành cho giảng viên' },
            { 'id': 'TUTEE', 'label': 'tutee', 'description': 'Dành cho học viên' },
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
    
    user = user_service.get_user_by_username(username)
    if not username: 
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    if user.Password != password :
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    
    if (role.lower() == 'tutor' and not user.IFlag) or (role.lower() == 'tutee' and not user.SFlag):
        raise HTTPException(
        status_code=403,
        detail=f"You don't have permission to login as {role}",
    )

    if role.lower() == 'admin' and username != 'sManager':
        raise HTTPException(
        status_code=403,
        detail=f"You don't have permission to login as {role}",
    )

   #payload
    access_token = create_access_token(
        data={"sub": str(user.UserID), "role": role.lower()}
    )

    response.set_cookie(
        key="session_id",
        value=access_token,
        httponly=True,  
        secure=True,    
        samesite="lax"  
    )
    
    return {"username": username, "role": role, "status": "Login successful"}

@router.post("/logout")
def logout(
    response: Response,
):
    response.delete_cookie(key="session_id")
    return {"status": "Logout successful"}