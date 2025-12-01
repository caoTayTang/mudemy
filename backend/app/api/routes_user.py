from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from .auth import *
from typing import Dict, Any
from ..models import mudemy_session
from ..services import UserService

router = APIRouter()

user_service = UserService(mudemy_session)


@router.get("/users/me")
def read_me(current_user: CurrentUser = Depends(get_current_user_from_session)):
	u = user_service.get_user_by_id(current_user.user_id)
	if not u:
		raise HTTPException(status_code=404, detail="User not found")
	return {"status": "success", "user": {"UserID": u.UserID, "User_name": getattr(u, 'User_name', None)}}


@router.get("/users")
def list_users(current_user: CurrentUser = Depends(get_current_user_from_session)):
	# only instructors (or higher) can list all users
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")

	items = user_service.get_all_users()
	return {"status": "success", "count": len(items)}


@router.put("/users/{user_id}")
def update_user(user_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# allow users to update their own profile; instructors can update anyone
	if current_user.role == 'tutee' and current_user.user_id != user_id:
		raise HTTPException(status_code=403, detail="Not authorized to update this user")

	u = user_service.update_user(user_id, data)
	if not u:
		raise HTTPException(status_code=404, detail="User not found")
	return {"status": "updated", "user_id": u.UserID}


@router.delete("/users/{user_id}")
def delete_user(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	# only instructors can delete other users
	if current_user.role == 'tutee' and current_user.user_id != user_id:
		raise HTTPException(status_code=403, detail="Not authorized to delete this user")

	ok = user_service.delete_user(user_id)
	if not ok:
		raise HTTPException(status_code=404, detail="User not found or could not be deleted")
	return {"status": "deleted", "user_id": user_id}

