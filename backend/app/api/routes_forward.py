from fastapi import APIRouter, Body
from ..models import *
from ..services import *
from fastapi.responses import JSONResponse
from ..core import *
from fastapi import Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from .auth import get_current_user_from_session
from ..hcmut_database import *

router = APIRouter()

# GET /api/library?type={mode}&q={keyword}
@router.get("/library")
def get_resource(
    type: str | None = None,     # /library?type=material or exam
    q: str | None = None,         # /library?q=python (search keyword)
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """
    Get library resources with optional filters for type and search keyword.
    All authenticated users can access.
    """
    try:
        if type and q:
            try:
                resource_type = ResourceType(type.lower())
                all_resources = hcmut_api.get_library_resources_by_type(resource_type)
                resources = [r for r in all_resources if q.lower() in r.name.lower()]
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid resource type: {type}")
        elif type:
            try:
                resource_type = ResourceType(type.lower())
                resources = hcmut_api.get_library_resources_by_type(resource_type)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid resource type: {type}")
        elif q:
            resources = hcmut_api.search_library_resources(q)
        else:
            resources = hcmut_api.get_all_library_resources()
        
        resources_data = []
        for resource in resources:
            uploader = hcmut_api.get_user_by_id(resource.uploader_id)
            resources_data.append({
                "id": resource.id,
                "name": resource.name,
                "resource_type": resource.resource_type.value,
                "file_type": resource.file_type.value,
                "file_size": resource.file_size,
                "uploader_id": resource.uploader_id,
                "uploader_name": uploader.full_name if uploader else "Unknown",
                "uploaded_at": resource.uploaded_at.isoformat()
            })
        
        return {
            "status": "success",
            "count": len(resources_data),
            "filters": {
                "type": type,
                "search": q
            },
            "resources": resources_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get library resources: {str(e)}")

# GET /api/library/:id
@router.get("/library/{id}")
def get_resource_by_id(
    id: int,
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """
    Get a specific library resource by ID.
    All authenticated users can access.
    """
    try:
        resource = hcmut_api.get_library_resource_by_id(id)
        
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        uploader = hcmut_api.get_user_by_id(resource.uploader_id)
        
        return {
            "status": "success",
            "resource": {
                "id": resource.id,
                "name": resource.name,
                "resource_type": resource.resource_type.value,
                "file_type": resource.file_type.value,
                "file_size": resource.file_size,
                "uploader_id": resource.uploader_id,
                "uploader_name": uploader.full_name if uploader else "Unknown",
                "uploaded_at": resource.uploaded_at.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get resource: {str(e)}")

# POST /api/library/download
@router.post("/library/download")
def download_resource(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """
    Download a library resource. Returns download information.
    All authenticated users can download.
    """
    resource_id = data.get('id')
    
    if not resource_id:
        raise HTTPException(status_code=400, detail="Missing resource id")
    
    try:
        resource = hcmut_api.get_library_resource_by_id(resource_id)
        
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        
        return {
            "status": "success",
            "message": "Resource ready for download",
            "resource": {
                "id": resource.id,
                "name": resource.name,
                "file_type": resource.file_type.value,
                "file_size": resource.file_size,

                "download_url": f"/files/library/{resource.id}.{resource.file_type.value}"
            },
            "downloaded_by": current_user.user_id,
            "downloaded_at": datetime.now(timezone.utc).isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download resource: {str(e)}")

# POST /api/library/attach
@router.post("/library/attach")
def attach_resource(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """
    Attach a library resource to a course.
    Only tutors can attach resources to their own courses.
    """
    if current_user.role != UserRole('tutor'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR role")
    
    resource_id = data.get('docId')  # Using docId to match the parameter name
    course_id = data.get('classId')  # Using classId to match the parameter name
    tutor_id = data.get('tutorId')
    
    if not resource_id or not course_id:
        raise HTTPException(status_code=400, detail="Missing required fields: docId and classId")

    if tutor_id and tutor_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="You can only attach resources to your own courses")
    
    try:      
        course_service = CourseService(mututor_session)
        course_resource_service = CourseResourceService(mututor_session)

        course = course_service.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        if course.tutor_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="You can only attach resources to your own courses")
        
        resource = hcmut_api.get_library_resource_by_id(resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Library resource not found")
        
        existing = course_resource_service.get_by_course_and_resource(course_id, resource_id)
        if existing:
            raise HTTPException(status_code=400, detail="Resource is already attached to this course")
        
        course_resource = course_resource_service.create(
            course_id=course_id,
            resource_id=resource_id
        )
        
        return {
            "status": "success",
            "message": "Resource attached to course successfully",
            "attachment": {
                "id": course_resource.id,
                "course_id": course_id,
                "course_title": course.title,
                "resource_id": resource_id,
                "resource_name": resource.name
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to attach resource: {str(e)}")

# POST /api/library/detach
@router.post("/library/detach")
def detach_resource(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """
    Detach a library resource from a course.
    Only tutors can detach resources from their own courses.
    """
    if current_user.role != UserRole('tutor'):
        raise HTTPException(status_code=403, detail="Not authorized, requires TUTOR role")
    
    resource_id = data.get('docId')
    course_id = data.get('classId')
    
    if not resource_id or not course_id:
        raise HTTPException(status_code=400, detail="Missing required fields: docId and classId")
    
    try: 
        course_service = CourseService(mututor_session)
        course_resource_service = CourseResourceService(mututor_session)
        
        course = course_service.get_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        if course.tutor_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="You can only detach resources from your own courses")

        success = course_resource_service.delete_by_course_and_resource(course_id, resource_id)
        if not success:
            raise HTTPException(status_code=404, detail="Resource attachment not found")
        
        return {
            "status": "success",
            "message": "Resource detached from course successfully",
            "course_id": course_id,
            "resource_id": resource_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detach resource: {str(e)}")