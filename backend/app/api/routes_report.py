from fastapi import APIRouter, Body
from ..models import *
from ..services import *
from fastapi.responses import JSONResponse
from ..core import *
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from .auth import get_current_user_from_session
from ..hcmut_database import*
router = APIRouter()

course_service = CourseService(mututor_session)
enrollment_service = EnrollmentService(mututor_session)
course_session_service = CourseSessionService(mututor_session)
session_evaluation_service = SessionEvaluationService(mututor_session)

@router.get("/tutor/tracking/classes")
def track_tutor_class(
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Get overview of all courses with statistics (admin only)"""
    if current_user.role != UserRole('admin'):
        raise HTTPException(status_code=403, detail="Not authorized, requires ADMIN role")
    
    try:
        all_courses = course_service.get_all()
        
        courses_data = []
        for course in all_courses:
            enrollments = enrollment_service.get_by_course(course.id)
            enrolled_count = sum(1 for e in enrollments if e.status == EnrollmentStatus.ENROLLED)
            dropped_count = sum(1 for e in enrollments if e.status == EnrollmentStatus.DROPPED)
            
            sessions = course_session_service.get_by_course(course.id)

            all_ratings = []
            for session in sessions:
                evaluations = session_evaluation_service.get_by_session(session.id)
                all_ratings.extend([e.rating for e in evaluations])
            
            avg_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0
            
            courses_data.append({
                "id": course.id,
                "title": course.title,
                "tutor_id": course.tutor_id,
                "status": course.status.value,
                "level": course.level.value,
                "max_students": course.max_students,
                "enrolled_students": enrolled_count,
                "dropped_students": dropped_count,
                "total_sessions": len(sessions),
                "average_rating": round(avg_rating, 2),
                "total_evaluations": len(all_ratings),
                "created_at": course.created_at.isoformat()
            })
        
        return {
            "status": "success",
            "total_courses": len(courses_data),
            "courses": courses_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get course tracking: {str(e)}")

@router.get("/tutor/tracking/classes/{id}")
def track_specific_class(
    id: int,
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Get detailed tracking for a specific course (admin only)"""
    if current_user.role != UserRole('admin'):
        raise HTTPException(status_code=403, detail="Not authorized, requires ADMIN role")
    
    try:
        course = course_service.get_by_id(id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        enrollments = enrollment_service.get_by_course(id)
        sessions = course_session_service.get_by_course(id)
        
        enrolled_students = []
        for enrollment in enrollments:
            if enrollment.status == EnrollmentStatus.ENROLLED:
                enrolled_students.append({
                    "tutee_id": enrollment.tutee_id,
                    "enrollment_date": enrollment.enrollment_date.isoformat(),
                    "status": enrollment.status.value
                })
        
        sessions_data = []
        for session in sessions:
            evaluations = session_evaluation_service.get_by_session(session.id)
            avg_session_rating = sum([e.rating for e in evaluations]) / len(evaluations) if evaluations else 0
            
            sessions_data.append({
                "id": session.id,
                "session_number": session.session_number,
                "session_date": session.session_date.isoformat(),
                "start_time": str(session.start_time),
                "end_time": str(session.end_time),
                "format": session.format.value,
                "location": session.location,
                "evaluations_count": len(evaluations),
                "average_rating": round(avg_session_rating, 2)
            })
        
        return {
            "status": "success",
            "course": {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "tutor_id": course.tutor_id,
                "status": course.status.value,
                "level": course.level.value,
                "max_students": course.max_students,
                "enrolled_count": len(enrolled_students),
                "created_at": course.created_at.isoformat()
            },
            "enrolled_students": enrolled_students,
            "sessions": sessions_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get course details: {str(e)}")

@router.get("/tutor/tracking/tutees")
def track_all_tutees(
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Get overview of all tutees with statistics (admin only)"""
    if current_user.role != UserRole('admin'):
        raise HTTPException(status_code=403, detail="Not authorized, requires ADMIN role")
    
    try:
        all_enroll = enrollment_service.get_all()
        all_tutees = list(set([e.tutee_id for e in all_enroll]))
        tutees_data = []
        for tutee in all_tutees:
            enrollments = enrollment_service.get_by_tutee(tutee)
            active_enrollments = [e for e in enrollments if e.status == EnrollmentStatus.ENROLLED]
            completed_enrollments = [e for e in enrollments if e.status == EnrollmentStatus.COMPLETED]
            dropped_enrollments = [e for e in enrollments if e.status == EnrollmentStatus.DROPPED]
            user = hcmut_api.get_student_by_id(tutee)
            tutees_data.append({
                "id": tutee,
                "name": user.full_name,
                "total_enrollments": len(enrollments),
                "active_courses": len(active_enrollments),
                "completed_courses": len(completed_enrollments),
                "dropped_courses": len(dropped_enrollments)
            })
        
        return {
            "status": "success",
            "total_tutees": len(tutees_data),
            "tutees": tutees_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tutee tracking: {str(e)}")

@router.get("/tutor/tracking/tutees/{id}")
def track_specific_tutee(
    id: str,
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Get detailed tracking for a specific tutee (admin only)"""
    if current_user.role != UserRole('admin'):
        raise HTTPException(status_code=403, detail="Not authorized, requires ADMIN role")
    
    try:        
        enrollments = enrollment_service.get_by_tutee(id)
        
        enrollments_data = []
        for enrollment in enrollments:
            course = course_service.get_by_id(enrollment.course_id)
            if course:
                evaluations = session_evaluation_service.get_by_enrollment(enrollment.id)
                
                enrollments_data.append({
                    "enrollment_id": enrollment.id,
                    "course_id": course.id,
                    "course_title": course.title,
                    "tutor_id": course.tutor_id,
                    "status": enrollment.status.value,
                    "enrollment_date": enrollment.enrollment_date.isoformat(),
                    "drop_reason": enrollment.drop_reason,
                    "evaluations_submitted": len(evaluations)
                })
        user = hcmut_api.get_student_by_id(id)
        return {
            "status": "success",
            "tutee": {
                "id": id,
                "name": user.full_name,
                "role": "Tutee"
            },
            "total_enrollments": len(enrollments_data),
            "enrollments": enrollments_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tutee details: {str(e)}")

@router.post("/reports")
def create_report(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Generate and save a custom report (admin only)"""
    if current_user.role != UserRole('admin'):
        raise HTTPException(status_code=403, detail="Not authorized, requires ADMIN role")
    
    report_data = data.get('reportData')
    
    if not report_data:
        raise HTTPException(status_code=400, detail="Missing reportData")
    
    report_type = report_data.get('type')  # e.g., 'course_summary', 'enrollment_summary'
    filters = report_data.get('filters', {})
    
    if not report_type:
        raise HTTPException(status_code=400, detail="Missing report type")
    
    try:
        if report_type == 'course_summary':
            courses = course_service.get_all()
            
            report = {
                "type": "course_summary",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "generated_by": current_user.user_id,
                "total_courses": len(courses),
                "courses_by_status": {},
                "courses_by_level": {}
            }
            
            for course in courses:
                status = course.status.value
                level = course.level.value
                
                report["courses_by_status"][status] = report["courses_by_status"].get(status, 0) + 1
                report["courses_by_level"][level] = report["courses_by_level"].get(level, 0) + 1
            
            return {
                "status": "success",
                "message": "Report generated successfully",
                "report": report
            }
        
        elif report_type == 'enrollment_summary':
            all_enrollments = enrollment_service.get_all()
            
            report = {
                "type": "enrollment_summary",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "generated_by": current_user.user_id,
                "total_enrollments": len(all_enrollments),
                "enrollments_by_status": {}
            }
            
            for enrollment in all_enrollments:
                status = enrollment.status.value
                report["enrollments_by_status"][status] = report["enrollments_by_status"].get(status, 0) + 1
            
            return {
                "status": "success",
                "message": "Report generated successfully",
                "report": report
            }
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown report type: {report_type}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")