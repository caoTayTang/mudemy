from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from .auth import *
from typing import Dict, Any, List, Optional

from ..models import mudemy_session
from ..services import EnrollmentService, PaymentService, CertificateService

router = APIRouter()

enrollment_service = EnrollmentService(mudemy_session)
payment_service = PaymentService(mudemy_session)
certificate_service = CertificateService(mudemy_session)


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


# ---------------------------
# Additional Enrollment CRUD
# ---------------------------


@router.get("/enrollments/{enrollment_id}")
def get_enrollment(enrollment_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get a enrollment"""
	e = enrollment_service.get_enrollment_by_id(enrollment_id)
	if not e:
		raise HTTPException(status_code=404, detail="Enrollment not found")

	if current_user.role == 'tutee' and e.StudentID != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to view this enrollment")

	return {"status": "success", "enrollment": {"EnrollmentID": e.EnrollmentID, "CourseID": e.CourseID, "StudentID": e.StudentID, "Status": getattr(e, 'Status', None)}}


@router.get("/courses/{course_id}/enrollments")
def get_enrollments_by_course(course_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get enrollments by course"""
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires instructor/admin role")

	items = enrollment_service.get_course_enrollments(course_id)
	return {"status": "success", "count": len(items), "enrollments": [{"EnrollmentID": i.EnrollmentID, "StudentID": i.StudentID, "Status": getattr(i, 'Status', None)} for i in items]}


@router.put("/enrollments/{enrollment_id}")
def update_enrollment(enrollment_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Update a enrollment"""
	e = enrollment_service.get_enrollment_by_id(enrollment_id)
	if not e:
		raise HTTPException(status_code=404, detail="Enrollment not found")

	# student can update their own enrollment; instructors can update any
	if current_user.role == 'tutee' and e.StudentID != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to update this enrollment")

	updated = enrollment_service.update_enrollment(enrollment_id, data)
	if not updated:
		raise HTTPException(status_code=400, detail="Unable to update enrollment")

	return {"status": "updated", "enrollment_id": updated.EnrollmentID}


@router.put("/enrollments/{enrollment_id}/status")
def update_enrollment_status(enrollment_id: str, status: str = Body(..., embed=True), current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Update a enrollment status"""
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized to change status")

	updated = enrollment_service.update_enrollment_status(enrollment_id, status)
	if not updated:
		raise HTTPException(status_code=400, detail="Unable to update status")
	return {"status": "updated", "enrollment_id": updated.EnrollmentID, "new_status": status}


@router.get("/courses/{course_id}/enrollments/count")
def enrollment_count(course_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get enrollments count"""
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires instructor/admin role")
	cnt = enrollment_service.get_enrollment_count_by_course(course_id)
	return {"status": "success", "course_id": course_id, "count": cnt}


@router.get("/enrollments/me/stats")
def my_enrollment_stats(current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get all my enrollments"""
	stats = enrollment_service.get_enrollment_stats(current_user.user_id)
	return {"status": "success", "stats": stats}


# ---------------------------
# Payment Endpoints
# ---------------------------


@router.post("/payments")
def create_payment(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Create a payment"""
	if current_user.role == 'tutor':
		raise HTTPException(status_code=403, detail="Not authorized, requires STUDENT role")
	data.setdefault('UserID', current_user.user_id)
	p = payment_service.create_payment(data)
	return JSONResponse(status_code=201, content={"status": "created", "payment_id": p.PaymentID})


@router.get("/payments/{payment_id}")
def get_payment(payment_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get a payment"""
	p = payment_service.get_payment_by_id(payment_id)
	if not p:
		raise HTTPException(status_code=404, detail="Payment not found")
	if current_user.role == 'tutee' and getattr(p, 'UserID', None) != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to view this payment")
	return {"status": "success", "payment": {"PaymentID": p.PaymentID, "Amount": getattr(p, 'Amount', None), "UserID": getattr(p, 'UserID', None)}}


@router.get("/payments/user/{user_id}")
def get_payments_by_user(user_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get a payment by user"""
	if current_user.role == 'tutee' and user_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to view other user's payments")
	items = payment_service.get_payments_by_user(user_id)
	return {"status": "success", "count": len(items), "payments": [{"PaymentID": i.PaymentID, "Amount": getattr(i, 'Amount', None)} for i in items]}


@router.get("/payments")
def get_all_payments(skip: int = 0, limit: int = 100, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get all payment"""
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires admin role")
	items = payment_service.get_all_payments(skip=skip, limit=limit)
	return {"status": "success", "count": len(items)}


@router.put("/payments/{payment_id}")
def update_payment(payment_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Update a payment"""
	p = payment_service.get_payment_by_id(payment_id)
	if not p:
		raise HTTPException(status_code=404, detail="Payment not found")
	# only owner or admin
	if current_user.role == 'tutee' and getattr(p, 'UserID', None) != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to update this payment")
	updated = payment_service.update_payment(payment_id, data)
	if not updated:
		raise HTTPException(status_code=400, detail="Unable to update payment")
	return {"status": "updated", "payment_id": updated.PaymentID}


@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Delete a payment"""
	p = payment_service.get_payment_by_id(payment_id)
	if not p:
		raise HTTPException(status_code=404, detail="Payment not found")
	if current_user.role == 'tutee' and getattr(p, 'UserID', None) != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to delete this payment")
	ok = payment_service.delete_payment(payment_id)
	if not ok:
		raise HTTPException(status_code=400, detail="Unable to delete payment")
	return {"status": "deleted", "payment_id": payment_id}


# ---------------------------
# Certificate Endpoints
# ---------------------------


@router.post("/certificates")
def create_certificate(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Create a certificate (INSTRUCTOR only)"""
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized to create certificate")
	c = certificate_service.create_certificate(data)
	return JSONResponse(status_code=201, content={"status": "created", "certificate_id": c.CertificateID})


@router.get("/certificates/{certificate_id}")
def get_certificate(certificate_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get certificates by certificate_id"""
	c = certificate_service.get_certificate_by_id(certificate_id)
	if not c:
		raise HTTPException(status_code=404, detail="Certificate not found")
	# students can view their own certificates
	if current_user.role == 'tutee' and getattr(c, 'StudentID', None) != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to view this certificate")
	return {"status": "success", "certificate": {"CertificateID": c.CertificateID, "CourseID": getattr(c, 'CourseID', None), "StudentID": getattr(c, 'StudentID', None)}}


@router.get("/certificates/student/{student_id}")
def get_student_certificates(student_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	"""Get certificates for a student"""
	if current_user.role == 'tutee' and student_id != current_user.user_id:
		raise HTTPException(status_code=403, detail="Not authorized to view other student's certificates")
	items = certificate_service.get_student_certificates(student_id)
	return {"status": "success", "count": len(items)}


@router.put("/certificates/{certificate_id}")
def update_certificate(
	certificate_id: str, 
	data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)
):
	"""Update a certificate (INSTRUCTOR only)"""
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized to update certificate")
	updated = certificate_service.update_certificate(certificate_id, data)
	if not updated:
		raise HTTPException(status_code=400, detail="Unable to update certificate")
	return {"status": "updated", "certificate_id": updated.CertificateID}


@router.delete("/certificates/{certificate_id}")
def delete_certificate(
	certificate_id: str, 
	current_user: CurrentUser = Depends(get_current_user_from_session)
):
	"""Delete a certificate (INSTRUCTOR only)"""
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized to delete certificate")
	ok = certificate_service.delete_certificate(certificate_id)
	if not ok:
		raise HTTPException(status_code=400, detail="Unable to delete certificate")
	return {"status": "deleted", "certificate_id": certificate_id}
