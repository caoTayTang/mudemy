from fastapi import APIRouter, Body
from ..models import *
from ..services import *
from fastapi.responses import JSONResponse
from ..core import *
from fastapi import Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
import uuid
from .auth import get_current_user_from_session
from ..hcmut_database import *
import asyncio

router = APIRouter()

course_service = CourseService(mututor_session)
enroll_service = EnrollmentService(mututor_session)
notification_service = NotificationService(mututor_session)
course_session_service = CourseSessionService(mututor_session)
course_resource_service = CourseResourceService(mututor_session)

@router.get("/tutor/courses")
def get_courses(
   current_user: MuSession = Depends(get_current_user_from_session)
):
    """Get all courses for the current tutor"""
    if current_user.role != UserRole('tutor'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR role")
    
    courses = course_service.get_by_tutor(current_user.user_id)

    courses_data = []
    for course in courses:
        sessions = course_session_service.get_by_course(course.id)
        sessions_data = []
        for session in sessions:
            sessions_data.append({
                "id": session.id,
                "session_number": session.session_number,
                "session_date": session.session_date.isoformat(),
                "start_time": str(session.start_time),
                "end_time": str(session.end_time),
                "format": session.format.value,
                "location": session.location
            })

        course_resources = course_resource_service.get_by_course(course.id)
        resources_data = []
        for resource_link in course_resources:
            resources_data.append({
                "id": resource_link.id,
                "resource_id": resource_link.resource_id
            })
        
        courses_data.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "cover_image_url": course.cover_image_url,
            "tutor_id": course.tutor_id,
            "subject_id": course.subject_id,
            "level": course.level.value,
            "max_students": course.max_students,
            "status": course.status.value,
            "created_at": course.created_at.isoformat(),
            "updated_at": course.updated_at.isoformat(),
            "sessions": sessions_data,
            "resources": resources_data
        })
    
    return {
        "status": "success",
        "tutor": current_user.user_id,
        "courses": courses_data
    }

@router.post("/courses")
def create_course(
    data: dict = Body(...),
   current_user: MuSession = Depends(get_current_user_from_session)
):
    """Create a new course with sessions and resources (tutor only)"""
    if current_user.role != UserRole('tutor'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR role")
    
    course_data = data.get('courseData')
    course_sessions = data.get('courseSessions', [])  # List of session data
    course_resources = data.get('courseResources', [])  # List of resource IDs
    
    if not course_data:
        raise HTTPException(status_code=400, detail="Missing courseData")

    if course_sessions:
        for session_data in course_sessions:
            schedule_result = course_session_service.check_time_confict(tutor_id=current_user.user_id, sessions=session_data)
            if not schedule_result['valid']:
                raise HTTPException(
                    status_code=400,
                    detail={"message": "Schedule validation failed","errors": schedule_result['errors']} )
            
            if session_data.get('format', 'offline') == 'online': continue
            session_date = datetime.strptime(session_data.get('session_date'), '%Y-%m-%d').date()
            start_time = datetime.strptime(session_data.get('start_time'), '%H:%M').time()
            end_time = datetime.strptime(session_data.get('end_time'), '%H:%M').time()
            room_name = session_data.get('location')
            room = hcmut_api.get_room_by_name(room_name)
            if not room: 
                raise HTTPException(
                    status_code=400,
                    detail={"message": f"Session {session_date} ({start_time}-{end_time}): Room not found for room {room_name}"})
            
            capacity = course_data.get('max_students')
            room_result = hcmut_api.can_book_room(room.id,session_date,start_time,end_time,capacity=capacity if capacity is not None else None)
            
            if not room_result:
                other_room = [room.name for room in hcmut_api.get_free_rooms_by_datetime(session_date,start_time,end_time)]
                raise HTTPException(
                    status_code=400,    
                    detail={"message": f"Session {session_date} ({start_time}-{end_time}): Room validation fails, other free room: {other_room}"} )

    if course_resources:
        resource_validation = hcmut_api.validate_course_resources(course_resources)      
        if not resource_validation['valid']:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid resource IDs",
                    "errors": resource_validation['errors']
                }
            )

    try:
        course = course_service.create(
            title=course_data.get('title'),
            tutor_id=current_user.user_id,
            subject_id=course_data.get('subject_id'),
            max_students=course_data.get('max_students'),
            description=course_data.get('description'),
            cover_image_url=course_data.get('cover_image_url'),
            level=Level(course_data.get('level', 'beginner')),
            status=CourseStatus(course_data.get('status', 'open'))
        )

        created_sessions = []
        if course_sessions:
            for session_data in course_sessions:
                session_date = datetime.strptime(session_data.get('session_date'), '%Y-%m-%d').date()
                start_time = datetime.strptime(session_data.get('start_time'), '%H:%M').time()
                end_time = datetime.strptime(session_data.get('end_time'), '%H:%M').time()
                format = CourseFormat(session_data.get('format', 'offline'))
                location= session_data.get('location')
                session = course_session_service.create(
                    course_id=course.id,
                    session_number=session_data.get('session_number'),
                    session_date=session_date,
                    start_time=start_time,
                    end_time=end_time,
                    format=format,
                    location=location
                )
                if format == CourseFormat.OFFLINE:
                    ret = hcmut_api.book_room(location, current_user.user_id, session_date, start_time, end_time, f"Booked room for course {course_data.get('title')}")
                    if not ret:
                        raise HTTPException(status_code=400,detail={ "message": "Invalid resource IDs","errors": f"Failed to book room: {location}"})
                created_sessions.append({
                    "id": session.id,
                    "session_number": session.session_number,
                    "date": session.session_date.isoformat(),
                    "time": f"{session.start_time} - {session.end_time}",
                    "format": f"{format}"

                })

        created_resources = []
        if course_resources:
            for resource_id in course_resources:
                resource_link = course_resource_service.create(
                    course_id=course.id,
                    resource_id=resource_id
                )
                created_resources.append({
                    "id": resource_link.id,
                    "resource_id": resource_id
                })

        
        return {
            "status": "success",
            "message": "Course created successfully",
            "course_id": course.id,
            "course": {
                "id": course.id,
                "title": course.title,
                "tutor_id": course.tutor_id,
                "status": course.status.value
            },
            "sessions_created": len(created_sessions),
            "sessions": created_sessions,
            "resources_linked": len(created_resources),
            "resources": created_resources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create course: {str(e)}")

@router.put("/courses")
async def modify_course(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Modify an existing course with sessions and resources (tutor only) and notify all enrolled tutees"""
    if current_user.role != UserRole('tutor'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR role")
    
    course_id = data.get('id')
    updated_data = data.get('updatedData')
    updated_session_data = data.get('updatedSessionData',None)
    course_session_id = data.get('courseSessionId',None) 
    course_resources = data.get('courseResources', []) 
    
    if not course_id or not updated_data:
        raise HTTPException(status_code=400, detail="Missing course id or updatedData")
    
    course = course_service.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.tutor_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only modify your own courses")
    
    old_session = None
    if course_session_id:
        old_session = course_session_service.get_by_course_session(course_id, course_session_id)
        if not old_session:
            raise HTTPException(status_code=403, detail="Course Session not found")

        schedule_result = course_session_service.check_time_confict(current_user.user_id, updated_session_data, old_session.id)
        if not schedule_result['valid']:
            raise HTTPException(
                status_code=400,
                detail={"message": "Schedule validation failed","errors": schedule_result['errors']} )
        
        if updated_session_data.get('format') == 'offline':
            session_date = datetime.strptime(updated_session_data.get('session_date'), '%Y-%m-%d').date()
            start_time = datetime.strptime(updated_session_data.get('start_time'), '%H:%M').time()
            end_time = datetime.strptime(updated_session_data.get('end_time'), '%H:%M').time()
            room_name = updated_session_data.get('location')
            room = hcmut_api.get_room_by_name(room_name)
            if not room: 
                raise HTTPException(
                    status_code=400,
                    detail={"message": f"Session {session_date} ({start_time}-{end_time}): Room not found for room {room_name}"})
            
            capacity = updated_data.get('max_students')
            room_result = hcmut_api.can_book_room(room.id,session_date,start_time,end_time,exclude_session=old_session,capacity=capacity if capacity is not None else None)
            
            if not room_result:
                old_room = None if old_session.format == CourseFormat.ONLINE else old_session.location
                other_room = [room.name for room in hcmut_api.get_free_rooms_by_datetime(session_date,start_time,end_time,old_room)]
                raise HTTPException(
                    status_code=400,
                    detail={"message": f"Session {session_date} ({start_time}-{end_time}): Room validation failed, other free room: {other_room}"} )
        
    if course_resources:
        resource_validation = hcmut_api.validate_course_resources(course_resources) 
        if not resource_validation['valid']:
            raise HTTPException(
                status_code=400,
                detail={"message": "Invalid resource IDs","errors": resource_validation['errors']})

    try:
        updated_course = course_service.update(
            course_id=course_id,
            title=updated_data.get('title'),
            description=updated_data.get('description'),
            cover_image_url=updated_data.get('cover_image_url'),
            level=Level(updated_data['level']) if updated_data.get('level') else None,
            max_students=updated_data.get('max_students'),
            status=CourseStatus(updated_data['status']) if updated_data.get('status') else None
        )
        
        if not updated_course:
            raise HTTPException(status_code=500, detail="Failed to update course")

        updated_session = None
        if course_session_id:         
            try:
                session_date = datetime.strptime(updated_session_data.get('session_date'), '%Y-%m-%d').date()
                start_time = datetime.strptime(updated_session_data.get('start_time'), '%H:%M').time()
                end_time = datetime.strptime(updated_session_data.get('end_time'), '%H:%M').time()
                format=CourseFormat(updated_session_data.get('format', "online"))
                location=updated_session_data.get('location')
                updated_session = course_session_service.update(
                    session_id=old_session.id,
                    session_number=updated_session_data.get('session_number'),
                    session_date=session_date,
                    start_time=start_time,
                    end_time=end_time,
                    format=format,
                    location=location
                )
                if old_session.format == CourseFormat.OFFLINE:
                    old_room = hcmut_api.get_room_by_name(old_session.location)
                    old_schedule = hcmut_api.get_schedule_session(old_room.id, old_session.session_date, old_session.start_time, old_session.end_time)
                    hcmut_api.cancel_booking(old_schedule.id, current_user.user_id)
                    
                if format == CourseFormat.OFFLINE:
                    ret = hcmut_api.book_room(location, current_user.user_id, session_date, start_time, end_time, f"Booked room for course {updated_data.get('title')}")
                    if not ret:
                        raise HTTPException(status_code=400,detail={ "message": "Invalid resource IDs","errors": f"Failed to book room: {location}"})
            except Exception as e:
                print(f"Warning: Failed to create session: {str(e)}")

        updated_resources = []
        if course_resources:  
            course_resource_service.delete_all_by_course(course_id)
            for resource_id in course_resources:
                try:
                    resource_link = course_resource_service.create(
                        course_id=course.id,
                        resource_id=resource_id
                    )
                    updated_resources.append({
                        "id": resource_link.id,
                        "resource_id": resource_id
                    })
                except Exception as e:
                    print(f"Warning: Failed to link resource {resource_id}: {str(e)}")
        

        enrollments = enroll_service.get_by_course(course_id)
        notification_count = 0
        for enrollment in enrollments:
            if enrollment.status == EnrollmentStatus.ENROLLED:
                notif = notification_service.create(
                    user_id=enrollment.tutee_id,
                    type=NotificationType.SCHEDULE_CHANGE,
                    title=f"Course Updated: {updated_course.title}",
                    content=f"The course '{updated_course.title}' has been updated by the tutor. Please check the course details.",
                    related_id=course_id
                )
                await manager.send_personal_message({
                    "type": "NEW_NOTIFICATION",
                    "data": {
                        "id": notif.id,
                        "title": notif.title,
                        "content": notif.content,
                        "type": notif.type.value,
                        "created_at": notif.created_at.isoformat()
                    }
                }, user_id=enrollment.tutee_id)

                notification_count += 1
        
        return {
            "status": "success",
            "message": "Course updated successfully",
            "notifications_sent": notification_count,
            "course": {
                "id": updated_course.id,
                "title": updated_course.title,
                "status": updated_course.status.value,
                "updated_at": updated_course.updated_at.isoformat()
            },
            "sessions_updated": 1,
            "sessions": updated_session,
            "resources_updated": len(updated_resources),
            "resources": updated_resources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update course: {str(e)}")


@router.delete("/courses")
async def delete_course(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Delete a course (tutor only) and notify all enrolled tutees"""
    if current_user.role != UserRole('tutor'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR role")
    
    course_id = data.get('id')
    if not course_id:
        raise HTTPException(status_code=400, detail="Missing course id")
 
    course = course_service.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.tutor_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own courses")
    
    try:
        success = course_service.delete(course_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete course")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete course: {str(e)}")
    
    enrollments = enroll_service.get_by_course(course_id)
    course_title = course.title

    notification_count = 0
    for enrollment in enrollments:
        if enrollment.status == EnrollmentStatus.ENROLLED:
            notif = notification_service.create(
                user_id=enrollment.tutee_id,
                type=NotificationType.ENROLLMENT_CANCELLED,
                title=f"Course Cancelled: {course_title}",
                content=f"The course '{course_title}' has been cancelled by the tutor.",
                related_id=course_id
            )
            await manager.send_personal_message({
                "type": "NEW_NOTIFICATION",
                "data": {
                    "id": notif.id,
                    "title": notif.title,
                    "content": notif.content,
                    "type": notif.type.value,
                    "created_at": notif.created_at.isoformat()
                }
            }, user_id=enrollment.tutee_id)
            notification_count += 1
    
    return {"status": "success",
            "message": "Course deleted successfully",
            "notifications_sent": notification_count}

# ==================== TUTEE ROUTES ====================

@router.get("/courses")
def get_courses_tutee(
    current_user: MuSession = Depends(get_current_user_from_session),
    status: str | None = None,
    subject_id: int | None = None,
    level: str | None = None
):
    """Get all available courses for tutees with optional filters"""
    if current_user.role != UserRole('tutee'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTEE role")
    
    if status:
        courses = course_service.get_by_status(CourseStatus(status))
    elif subject_id:
        courses = course_service.get_by_subject(subject_id)
    elif level:
        courses = course_service.get_by_level(Level(level))
    else:
        courses = course_service.get_by_status(CourseStatus.OPEN)
    #exclude own courses
    courses = [course for course in courses if course.tutor_id != current_user.user_id]
    courses_data = []
    for course in courses:
        enrollment = enroll_service.get_by_tutee_and_course(current_user.user_id, course.id)
        is_enrolled = enrollment is not None and enrollment.status == EnrollmentStatus.ENROLLED
        
        enrollments = enroll_service.get_by_course(course.id)
        enrolled_count = sum(1 for e in enrollments if e.status == EnrollmentStatus.ENROLLED)
        
        sessions = course_session_service.get_by_course(course.id)
        sessions_data = []
        for session in sessions:
            sessions_data.append({
                "id": session.id,
                "session_number": session.session_number,
                "session_date": session.session_date.isoformat(),
                "start_time": str(session.start_time),
                "end_time": str(session.end_time),
                "format": session.format.value,
                "location": session.location
            })
        
        course_resources = course_resource_service.get_by_course(course.id)
        resources_data = []
        for resource_link in course_resources:
            resources_data.append({
                "id": resource_link.id,
                "resource_id": resource_link.resource_id
            })
        
        courses_data.append({
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "cover_image_url": course.cover_image_url,
            "tutor_id": course.tutor_id,
            "subject_id": course.subject_id,
            "level": course.level.value,
            "max_students": course.max_students,
            "enrolled_students": enrolled_count,
            "available_slots": course.max_students - enrolled_count,
            "status": course.status.value,
            "is_enrolled": is_enrolled,
            "created_at": course.created_at.isoformat(),
            "sessions": sessions_data,
            "resources": resources_data
        })
    
    return {
        "status": "success",
        "tutee": current_user.user_id,
        "courses": courses_data
    }

@router.post("/enrollments")
async def enroll_course(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Enroll a tutee in a course and notify the tutor"""
    if current_user.role != UserRole('tutee'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTEE role")
    
    course_id = data.get('courseId')
    tutee_id = data.get('tuteeId')
    
    if not course_id:
        raise HTTPException(status_code=400, detail="Missing courseId")
    

    if tutee_id and tutee_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only enroll yourself")
    
    tutee_id = current_user.user_id

    course = course_service.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if course.status != CourseStatus.OPEN:
        raise HTTPException(status_code=400, detail="Course is not open for enrollment")
    

    existing_enrollment = enroll_service.get_by_tutee_and_course(tutee_id, course_id)
    if existing_enrollment and existing_enrollment.status == EnrollmentStatus.ENROLLED:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")

    enrollments = enroll_service.get_by_course(course_id)
    enrolled_count = sum(1 for e in enrollments if e.status == EnrollmentStatus.ENROLLED)
    if enrolled_count >= course.max_students:
        raise HTTPException(status_code=400, detail="Course is full")

    conflict_check = enroll_service.check_time_conflict(tutee_id, course_id)
    if not conflict_check['valid']:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Enrollment time conflict detected",
                "errors": conflict_check['errors']
            }
        )

    try:
        if existing_enrollment:
            enrollment = enroll_service.update(existing_enrollment.id, EnrollmentStatus.ENROLLED)
        else:
            enrollment = enroll_service.create(
                tutee_id=tutee_id,
                course_id=course_id,
                status=EnrollmentStatus.ENROLLED
            )

        notif_1 = notification_service.create(
            user_id=course.tutor_id,
            type=NotificationType.ENROLLMENT_SUCCESS,
            title=f"New Enrollment: {course.title}",
            content=f"Student {current_user.user_id} has enrolled in your course '{course.title}'.",
            related_id=course_id
        )
        await manager.send_personal_message({
            "type": "NEW_NOTIFICATION",
            "data": {
                "id": notif_1.id,
                "title": notif_1.title,
                "content": notif_1.content,
                "type": notif_1.type.value,
                "created_at": notif_1.created_at.isoformat()
            }
        }, user_id=course.tutor_id)

        notif_2 = notification_service.create(
            user_id=tutee_id,
            type=NotificationType.ENROLLMENT_SUCCESS,
            title=f"Enrollment Confirmed: {course.title}",
            content=f"You have successfully enrolled in '{course.title}'.",
            related_id=course_id
        )

        await manager.send_personal_message({
            "type": "NEW_NOTIFICATION",
            "data": {
                "id": notif_2.id,
                "title": notif_2.title,
                "content": notif_2.content,
                "type": notif_2.type.value,
                "created_at": notif_2.created_at.isoformat()
            }
        }, user_id=tutee_id)

        return {
            "status": "success",
            "message": "Successfully enrolled in course",
            "enrollment_id": enrollment.id,
            "course": {
                "id": course.id,
                "title": course.title
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enroll: {str(e)}")

@router.delete("/enrollments")
async def unregister_course(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Unenroll a tutee from a course and notify the tutor"""
    if current_user.role != UserRole('tutee'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTEE role")
    
    course_id = data.get('courseId')
    tutee_id = data.get('tuteeId')
    drop_reason = data.get('reason', 'Student requested withdrawal')
    
    if not course_id:
        raise HTTPException(status_code=400, detail="Missing courseId")
    
    if tutee_id and tutee_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only unenroll yourself")
 
    tutee_id = current_user.user_id

    enrollment = enroll_service.get_by_tutee_and_course(tutee_id, course_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    if enrollment.status != EnrollmentStatus.ENROLLED:
        raise HTTPException(status_code=400, detail="Not currently enrolled in this course")
  
    course = course_service.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    try:
        updated_enrollment = enroll_service.update(
            enrollment_id=enrollment.id,
            status=EnrollmentStatus.DROPPED,
            drop_reason=drop_reason
        )

        notif_1 = notification_service.create(
            user_id=course.tutor_id,
            type=NotificationType.ENROLLMENT_CANCELLED,
            title=f"Student Dropped: {course.title}",
            content=f"Student {current_user.user_id} has dropped from your course '{course.title}'. Reason: {drop_reason}",
            related_id=course_id
        )
        
        await manager.send_personal_message({
            "type": "NEW_NOTIFICATION",
            "data": {
                "id": notif_1.id,
                "title": notif_1.title,
                "content": notif_1.content,
                "type": notif_1.type.value,
                "created_at": notif_1.created_at.isoformat()
            }
        }, user_id=course.tutor_id)

        notif_2 = notification_service.create(
            user_id=tutee_id,
            type=NotificationType.ENROLLMENT_CANCELLED,
            title=f"Unenrolled: {course.title}",
            content=f"You have been unenrolled from '{course.title}'.",
            related_id=course_id
        )
        
        await manager.send_personal_message({
            "type": "NEW_NOTIFICATION",
            "data": {
                "id": notif_2.id,
                "title": notif_2.title,
                "content": notif_2.content,
                "type": notif_2.type.value,
                "created_at": notif_2.created_at.isoformat()
            }
        }, user_id=tutee_id)

        return {
            "status": "success",
            "message": "Successfully unenrolled from course",
            "course": {
                "id": course.id,
                "title": course.title
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unenroll: {str(e)}")


@router.get("/tutee/enrollments")
def get_my_enrollments(
    current_user: MuSession = Depends(get_current_user_from_session),
    status: str | None = None
):
    """Get all enrollments for the current tutee"""
    if current_user.role != UserRole('tutee'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTEE role")
    

    enrollments = enroll_service.get_by_tutee(current_user.user_id)

    if status:
        enrollments = [e for e in enrollments if e.status == EnrollmentStatus(status)]
    
    enrollments_data = []
    for enrollment in enrollments:
        course = course_service.get_by_id(enrollment.course_id)
        if course:
            enrollments_data.append({
                "enrollment_id": enrollment.id,
                "course_id": course.id,
                "course_title": course.title,
                "tutor_id": course.tutor_id,
                "status": enrollment.status.value,
                "enrollment_date": enrollment.enrollment_date.isoformat(),
                "drop_reason": enrollment.drop_reason
            })
    
    return {
        "status": "success",
        "tutee": current_user.user_id,
        "enrollments": enrollments_data
    }