from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from .auth import *
from typing import Dict, Any

from ..models import mudemy_session
from ..services import UserService, TakeService, InterestsService, InstructService, QualificationService

router = APIRouter()

user_service = UserService(mudemy_session)
take_service = TakeService(mudemy_session)
interests_service = InterestsService(mudemy_session)
instruct_service = InstructService(mudemy_session)
qualification_service = QualificationService(mudemy_session)


@router.get("/users/me")
def get_me(current_user: CurrentUser = Depends(get_current_user_from_session)):
	u = user_service.get_user_by_id(current_user.user_id)
	if not u:
		raise HTTPException(status_code=404, detail="User not found")
	return {
		"status": "success",
		"user": {
			"UserID": u.UserID,
			"User_name": u.User_name,
			"Email": u.Email,
			"Full_name": u.Full_name,
			"City": u.City,
			"Country": u.Country,
			"Phone": u.Phone,
			"Date_of_birth": u.Date_of_birth,
			"Last_login": u.Last_login,
			"IFlag": u.IFlag,
			"Bio_text": u.Bio_text,
			"Year_of_experience": u.Year_of_experience,
			"SFlag": u.SFlag,
			"Total_enrollments": u.Total_enrollments
		}
	}


@router.post("/users")
def create_user(data: Dict[str, Any] = Body(...)):
	try:
		u = user_service.create_user(data)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	return JSONResponse(status_code=201, content={"status": "created", "user_id": u.UserID})


@router.get("/users")
def list_users(limit: int = 100, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")

	users = user_service.get_all_users(limit=limit)
	return {
		"status": "success",
		"count": len(users),
		"users": [{
			"UserID": u.UserID,
			"User_name": u.User_name,
			"Email": u.Email,
			"Full_name": u.Full_name,
			"City": u.City,
			"Country": u.Country,
			"Phone": u.Phone,
			"Date_of_birth": u.Date_of_birth,
			"Last_login": u.Last_login,
			"IFlag": u.IFlag,
			"Bio_text": u.Bio_text,
			"Year_of_experience": u.Year_of_experience,
			"SFlag": u.SFlag,
			"Total_enrollments": u.Total_enrollments
		} for u in users]
	}


@router.get("/users/id/{user_id}")
def get_user(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	u = user_service.get_user_by_id(user_id)
	if not u:
		raise HTTPException(status_code=404, detail="User not found")
	if current_user.role == 'tutee' and current_user.user_id != user_id:
		raise HTTPException(status_code=403, detail="Not authorized to view this user")
	return {
		"status": "success",
		"user": {
			"UserID": u.UserID,
			"User_name": u.User_name,
			"Email": u.Email,
			"Full_name": u.Full_name,
			"City": u.City,
			"Country": u.Country,
			"Phone": u.Phone,
			"Date_of_birth": u.Date_of_birth,
			"Last_login": u.Last_login,
			"IFlag": u.IFlag,
			"Bio_text": u.Bio_text,
			"Year_of_experience": u.Year_of_experience,
			"SFlag": u.SFlag,
			"Total_enrollments": u.Total_enrollments
		}
	}


@router.put("/users/{user_id}")
def update_user(user_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# allow users to update their own profile; admin can update anyone
	if current_user.role == 'tutee' and current_user.user_id != user_id:
		raise HTTPException(status_code=403, detail="Not authorized to update this user")

	u = user_service.update_user(user_id, data)
	if not u:
		raise HTTPException(status_code=404, detail="User not found")
	return {"status": "updated", "user_id": u.UserID}


@router.delete("/users/{user_id}")
def delete_user(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	# only instructors/admins can delete other users
	if current_user.role == 'tutee' and current_user.user_id != user_id:
		raise HTTPException(status_code=403, detail="Not authorized to delete this user")

	ok = user_service.delete_user(user_id)
	if not ok:
		raise HTTPException(status_code=404, detail="User not found or could not be deleted")
	return {"status": "deleted", "user_id": user_id}


# ---------------------------
# Helper endpoints (in user_service)
# ---------------------------


@router.get("/users/instructors")
def list_instructors(current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")
	items = user_service.get_instructors()
	return {
		"status": "success",
		"count": len(items),
		"instructors": [{
			"UserID": u.UserID,
			"User_name": u.User_name,
			"Email": u.Email,
			"Full_name": u.Full_name,
			"City": u.City,
			"Country": u.Country,
			"Phone": u.Phone,
			"Bio_text": u.Bio_text,
			"Year_of_experience": u.Year_of_experience
		} for u in items]
	}


@router.get("/users/students")
def list_students(current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")
	items = user_service.get_students()
	return {
		"status": "success",
		"count": len(items),
		"students": [{
			"UserID": u.UserID,
			"User_name": u.User_name,
			"Email": u.Email,
			"Full_name": u.Full_name,
			"City": u.City,
			"Country": u.Country,
			"Total_enrollments": u.Total_enrollments
		} for u in items]
	}

@router.post("/users/{user_id}/last-login")
def touch_last_login(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	# users can update their own last login (typically used internally)
	if current_user.role == 'tutee' and current_user.user_id != user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	u = user_service.update_last_login(user_id)
	if not u:
		raise HTTPException(status_code=404, detail="User not found")
	return {"status": "updated", "user_id": u.UserID}


@router.post("/users/{user_id}/increment-enrollments")
def increment_enrollments(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	# typically called by enrollment logic; restrict to non-students or the user themselves
	if current_user.role == 'tutee' and current_user.user_id != user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	u = user_service.increment_enrollments(user_id)
	if not u:
		raise HTTPException(status_code=404, detail="User not found")
	return {"status": "updated", "user_id": u.UserID, "total_enrollments": getattr(u, 'Total_enrollments', None)}


@router.get("/users/search")
def search_users(name: str = Query(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")
	items = user_service.search_users_by_name(name)
	return {
		"status": "success",
		"count": len(items),
		"users": [{
			"UserID": u.UserID,
			"User_name": u.User_name,
			"Email": u.Email,
			"Full_name": u.Full_name,
			"City": u.City,
			"Country": u.Country
		} for u in items]
	}


# ---------------------------
# Take (lesson progress) endpoints
# ---------------------------


@router.post("/takes")
def create_take(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# data must include UserID and LessonID; student can create for self
	user_id = data.get('UserID') or current_user.user_id
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to create take for another user")
	t = take_service.create_take(user_id, data.get('LessonID'), data.get('is_finished', False))
	return JSONResponse(status_code=201, content={"status": "created", "UserID": t.UserID, "LessonID": t.LessonID})


@router.get("/takes/{user_id}/{lesson_id}")
def get_take(user_id: str, lesson_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	t = take_service.get_take(user_id, lesson_id)
	if not t:
		raise HTTPException(status_code=404, detail="Take not found")
	return {"status": "success", "take": {"UserID": t.UserID, "LessonID": t.LessonID, "is_finished": getattr(t, 'is_finished', None)}}


@router.get("/takes/user/{user_id}")
def get_user_lessons(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	items = take_service.get_user_lessons(user_id)
	return {
		"status": "success",
		"count": len(items),
		"lessons": [{
			"UserID": t.UserID,
			"LessonID": t.LessonID,
			"is_finished": t.is_finished
		} for t in items]
	}


@router.post("/takes/{user_id}/{lesson_id}/finish")
def mark_lesson_finished(user_id: str, lesson_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	t = take_service.mark_lesson_finished(user_id, lesson_id)
	if not t:
		raise HTTPException(status_code=404, detail="Take not found")
	return {"status": "updated", "UserID": t.UserID, "LessonID": t.LessonID}


@router.post("/takes/{user_id}/{lesson_id}/unfinished")
def mark_lesson_unfinished(user_id: str, lesson_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	t = take_service.mark_lesson_unfinished(user_id, lesson_id)
	if not t:
		raise HTTPException(status_code=404, detail="Take not found")
	return {"status": "updated", "UserID": t.UserID, "LessonID": t.LessonID}


@router.delete("/takes/{user_id}/{lesson_id}")
def delete_take(user_id: str, lesson_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	ok = take_service.delete_take(user_id, lesson_id)
	if not ok:
		raise HTTPException(status_code=404, detail="Take not found")
	return {"status": "deleted"}


@router.get("/takes/{user_id}/progress")
def get_lesson_progress(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	stats = take_service.get_lesson_progress(user_id)
	return {"status": "success", "progress": stats}


# ---------------------------
# Interests endpoints
# ---------------------------


@router.post("/users/{user_id}/interests")
def add_interest(user_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	interest = data.get('interest') or data.get('Interest')
	if not interest:
		raise HTTPException(status_code=400, detail="Missing interest")
	obj = interests_service.add_interest(user_id, interest)
	return JSONResponse(status_code=201, content={"status": "created", "user_id": obj.UserID, "interest": obj.Interest})


@router.get("/users/{user_id}/interests")
def get_user_interests(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	items = interests_service.get_user_interests(user_id)
	return {
		"status": "success",
		"count": len(items),
		"interests": [{
			"UserID": i.UserID,
			"Interest": i.Interest
		} for i in items]
	}


@router.delete("/users/{user_id}/interests")
def clear_user_interests(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	ok = interests_service.clear_user_interests(user_id)
	if not ok:
		raise HTTPException(status_code=404, detail="No interests to clear")
	return {"status": "deleted"}


# ---------------------------
# Instruct endpoints
# ---------------------------


@router.post("/instruct")
def assign_instructor(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# only instructors/admins can assign instructors
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")
	user_id = data.get('UserID')
	course_id = data.get('CourseID')
	if not user_id or not course_id:
		raise HTTPException(status_code=400, detail="Missing UserID or CourseID")
	obj = instruct_service.assign_instructor(user_id, course_id)
	return JSONResponse(status_code=201, content={"status": "assigned", "UserID": obj.UserID, "CourseID": obj.CourseID})


@router.get("/instructors/{user_id}/courses")
def get_instructor_courses(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	items = instruct_service.get_instructor_courses(user_id)
	return {
		"status": "success",
		"count": len(items),
		"courses": [{
			"UserID": i.UserID,
			"CourseID": i.CourseID
		} for i in items]
	}


@router.get("/courses/{course_id}/instructors")
def get_course_instructors(course_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")
	items = instruct_service.get_course_instructors(course_id)
	return {
		"status": "success",
		"count": len(items),
		"instructors": [{
			"UserID": i.UserID,
			"CourseID": i.CourseID
		} for i in items]
	}


@router.delete("/instruct/{user_id}/{course_id}")
def remove_instructor(user_id: str, course_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")
	ok = instruct_service.remove_instructor(user_id, course_id)
	if not ok:
		raise HTTPException(status_code=404, detail="Instructor assignment not found")
	return {"status": "deleted"}


@router.get("/instruct/is/{user_id}/{course_id}")
def is_instructor_of_course(user_id: str, course_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	ok = instruct_service.is_instructor_of_course(user_id, course_id)
	return {"status": "success", "is_instructor": ok}


# ---------------------------
# Qualification endpoints
# ---------------------------


@router.post("/users/{user_id}/qualifications")
def add_qualification(user_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized to add qualification")
	qual = data.get('qualification') or data.get('Qualification')
	if not qual:
		raise HTTPException(status_code=400, detail="Missing qualification")
	obj = qualification_service.add_qualification(user_id, qual)
	return JSONResponse(status_code=201, content={"status": "created", "user_id": obj.UserID})


@router.get("/users/{user_id}/qualifications")
def get_user_qualifications(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized")
	items = qualification_service.get_user_qualifications(user_id)
	return {
		"status": "success",
		"count": len(items),
		"qualifications": [{
			"UserID": q.UserID,
			"Qualification": q.Qualification
		} for q in items]
	}

@router.delete("/users/{user_id}/qualifications/{qualification}")
def remove_user_qualifications(user_id: str, qualification:str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")
	ok = qualification_service.remove_qualification(user_id, qualification)
	if not ok:
		raise HTTPException(status_code=404, detail="No qualifications to remove")
	return {"status": "deleted"}

@router.delete("/users/{user_id}/qualifications")
def clear_user_qualifications(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized")
	ok = qualification_service.clear_user_qualifications(user_id)
	if not ok:
		raise HTTPException(status_code=404, detail="No qualifications to clear")
	return {"status": "deleted"}

