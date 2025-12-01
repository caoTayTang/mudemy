from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from .auth import *
from typing import Dict, Any
from ..models import mudemy_session
from ..services import EnrollmentService, PaymentService

router = APIRouter()

enrollment_service = EnrollmentService(mudemy_session)
payment_service = PaymentService(mudemy_session)


@router.post("/enroll")
def create_enrollment(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# only students (tutee) should enroll
	if current_user.role != 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires STUDENT role")

	# ensure StudentID is set to current user if not provided
	data.setdefault('StudentID', current_user.user_id)
	e = enrollment_service.create_enrollment(data)
	return JSONResponse(status_code=201, content={"status": "created", "enrollment_id": e.EnrollmentID})


@router.get("/enrollments/me")
def my_enrollments(current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role != 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires STUDENT role")

	items = enrollment_service.get_student_enrollments(current_user.user_id)
	return {"status": "success", "count": len(items)}


@router.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	# allow only the student who owns it or instructors
	e = enrollment_service.get_enrollment_by_id(enrollment_id)
	if not e:
		raise HTTPException(status_code=404, detail="Enrollment not found")

	if current_user.role == 'tutee' and e.StudentID != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to delete this enrollment")

	ok = enrollment_service.delete_enrollment(enrollment_id)
	if not ok:
		raise HTTPException(status_code=400, detail="Unable to delete enrollment")

	return {"status": "deleted", "enrollment_id": enrollment_id}

