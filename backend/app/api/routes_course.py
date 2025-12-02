from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy import text

from ..models import mudemy_session
from ..services import (
    CourseService, ModuleService, RequiresService, ContentService,
    LessonRefService, TextService, VideoService, ImageService,
    CategoryService)
from .auth import get_current_user_from_session, CurrentUser

router = APIRouter()

# Initialize all services
course_service = CourseService(mudemy_session)
module_service = ModuleService(mudemy_session)
requires_service = RequiresService(mudemy_session)
content_service = ContentService(mudemy_session)
lesson_ref_service = LessonRefService(mudemy_session)
text_service = TextService(mudemy_session)
video_service = VideoService(mudemy_session)
image_service = ImageService(mudemy_session)
category_service = CategoryService(mudemy_session)


# ============================================================
# COURSE ROUTES
# ============================================================

@router.get("/courses")
def get_all_courses(
    limit: int = Query(100, ge=1, le=100),
    difficulty: Optional[str] = None,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get all courses with optional filtering"""
    if difficulty:
        courses = course_service.get_courses_by_difficulty(difficulty)
    else:
        courses = course_service.get_all_courses(limit)
    
    return {
        "status": "success",
        "count": len(courses),
        "courses": [
            {
                "CourseID": c.CourseID,
                "Title": c.Title,
                "Difficulty": c.Difficulty,
                "Language": c.Language,
                "Description": c.Description
            } for c in courses
        ]
    }


@router.post("/courses")
def create_course(
    course_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Create a new course (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    try:
        course = course_service.create_course(course_data)
        return JSONResponse(
            status_code=201,
            content={
                "status": "created",
                "course_id": course.CourseID,
                "title": course.Title
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/id/{course_id}")
def get_course(
    course_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get a specific course by ID"""
    course = course_service.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Get categories for this course
    categories = category_service.get_categories_by_course(course_id)
    
    # Get prerequisites
    prerequisites = requires_service.get_prerequisites(course_id)
    
    return {
        "status": "success",
        "course": {
            "CourseID": course.CourseID,
            "Title": course.Title,
            "Difficulty": course.Difficulty,
            "Language": course.Language,
            "Description": course.Description,
            "Categories": [c.Category for c in categories],
            "Prerequisites": [p.Required_courseID for p in prerequisites]
        }
    }


@router.put("/courses/{course_id}")
def update_course(
    course_id: str,
    update_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Update a course (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    course = course_service.update_course(course_id, update_data)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return {"status": "updated", "course_id": course.CourseID}


@router.delete("/courses/{course_id}")
def delete_course(
    course_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Delete a course (Instructor only)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    ok = course_service.delete_course(course_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return {"status": "deleted", "course_id": course_id}


@router.get("/courses/search")
def search_courses(
    title: str = Query(..., min_length=1),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Search courses by title"""
    courses = course_service.search_courses_by_title(title)
    return {
        "status": "success",
        "count": len(courses),
        "courses": [{
            "CourseID": c.CourseID,
            "Title": c.Title,
            "Difficulty": c.Difficulty,
            "Language": c.Language,
            "Description": c.Description
        } for c in courses]
    }


# ============================================================
# CATEGORY ROUTES
# ============================================================

@router.post("/courses/{course_id}/categories")
def add_category_to_course(
    course_id: str,
    category_data: Dict[str, str] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Add a category to a course"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    try:
        category = category_service.add_category(course_id, category_data.get("category"))
        return JSONResponse(status_code=201, content={"status": "added", "category": category.Category})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/categories")
def get_course_categories(
    course_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get all categories for a course"""
    categories = category_service.get_categories_by_course(course_id)
    return {
        "status": "success",
        "count": len(categories),
        "categories": [c.Category for c in categories]
    }


@router.delete("/courses/{course_id}/categories/{category}")
def remove_category_from_course(
    course_id: str,
    category: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Remove a category from a course"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    ok = category_service.remove_category(course_id, category)
    if not ok:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return {"status": "deleted"}


# ============================================================
# PREREQUISITE ROUTES
# ============================================================

@router.post("/courses/{course_id}/prerequisites")
def add_prerequisite(
    course_id: str,
    prereq_data: Dict[str, str] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Add a prerequisite course"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    try:
        required_course_id = prereq_data.get("required_course_id")
        prereq = requires_service.add_prerequisite(course_id, required_course_id)
        return JSONResponse(status_code=201, content={"status": "added", "prerequisite": required_course_id})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/prerequisites")
def get_prerequisites(
    course_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get all prerequisites for a course"""
    prereqs = requires_service.get_prerequisites(course_id)
    return {
        "status": "success",
        "prerequisites": [p.Required_courseID for p in prereqs]
    }

@router.get("/courses/{course_id}/prerequisites/f")
def check_prerequisites(course_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
    """Get all prerequisites for a course (Using CheckPrerequisiteCompletion PROCEDURE)"""
    print(course_id)
    sid = current_user.user_id
    result = []
    with mudemy_session() as session:
        rows = session.execute(text("EXEC CheckPrerequisiteCompletion :student_id, :target_course_id"), {"student_id": sid, "target_course_id": course_id}).fetchall()
        for r in rows:
            result.append({"CourseID":r[0],"Title":r[1]})
    return {"status": "success", "count": len(rows), "missing_prereqs": result}

@router.delete("/courses/{course_id}/prerequisites/{required_course_id}")
def remove_prerequisite(
    course_id: str,
    required_course_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Remove a prerequisite"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    ok = requires_service.remove_prerequisite(course_id, required_course_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Prerequisite not found")
    
    return {"status": "deleted"}


# ============================================================
# MODULE ROUTES
# ============================================================

@router.post("/modules")
def create_module(
    module_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Create a new module"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    try:
        module = module_service.create_module(module_data)
        return JSONResponse(status_code=201, content={"status": "created", "module_id": module.ModuleID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/courses/{course_id}/modules")
def get_course_modules(
    course_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get all modules for a course"""
    modules = module_service.get_modules_by_course(course_id)
    return {
        "status": "success",
        "count": len(modules),
        "modules": [
            {
                "ModuleID": m.ModuleID,
                "Title": m.Title,
                "CourseID": m.CourseID
            } for m in modules
        ]
    }


@router.get("/modules/{module_id}")
def get_module(
    module_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get a specific module"""
    module = module_service.get_module_by_id(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    return {
        "status": "success",
        "module": {
            "ModuleID": module.ModuleID,
            "Title": module.Title,
            "CourseID": module.CourseID
        }
    }


@router.put("/modules/{module_id}")
def update_module(
    module_id: str,
    update_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Update a module"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    module = module_service.update_module(module_id, update_data)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    return {"status": "updated", "module_id": module.ModuleID}


@router.delete("/modules/{module_id}")
def delete_module(
    module_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Delete a module"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    ok = module_service.delete_module(module_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Module not found")
    
    return {"status": "deleted", "module_id": module_id}


# ============================================================
# CONTENT ROUTES (TEXT, VIDEO, IMAGE)
# ============================================================

@router.post("/content")
def create_content(
    content_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Create new content (triggers handle LESSON_REF automatically)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    try:
        content = content_service.create_content(content_data)
        return JSONResponse(status_code=201, content={"status": "created", "content_id": content.ContentID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/modules/{module_id}/content")
def get_module_content(
    module_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get all content for a module"""
    contents = content_service.get_content_by_module(module_id)
    return {
        "status": "success",
        "count": len(contents),
        "contents": [
            {
                "ContentID": c.ContentID,
                "Title": c.Title,
                "Slides": c.Slides,
                "ModuleID": c.ModuleID
            } for c in contents
        ]
    }


@router.get("/content/{content_id}")
def get_content(
    content_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Get specific content with its media (text/video/image)"""
    content = content_service.get_content_by_id(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Check for text, video, or image
    text = text_service.get_text_by_content_id(content_id)
    video = video_service.get_video_by_content_id(content_id)
    image = image_service.get_image_by_content_id(content_id)
    
    result = {
        "ContentID": content.ContentID,
        "Title": content.Title,
        "Slides": content.Slides,
        "ModuleID": content.ModuleID
    }
    
    if text:
        result["Text"] = {"TextID": text.TextID, "Text": text.Text}
    if video:
        result["Video"] = {"VideoID": video.VideoID, "Video": video.Video}
    if image:
        result["Image"] = {"ImageID": image.ImageID, "Image": image.Image}
    
    return {"status": "success", "content": result}


@router.put("/content/{content_id}")
def update_content(
    content_id: str,
    update_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Update content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    content = content_service.update_content(content_id, update_data)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return {"status": "updated", "content_id": content.ContentID}


@router.delete("/content/{content_id}")
def delete_content(
    content_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Delete content (triggers handle LESSON_REF cleanup)"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    ok = content_service.delete_content(content_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return {"status": "deleted", "content_id": content_id}


# ============================================================
# TEXT ROUTES
# ============================================================

@router.post("/content/{content_id}/text")
def add_text_to_content(
    content_id: str,
    text_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Add text to content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    try:
        text_data["ContentID"] = content_id
        text = text_service.create_text(text_data)
        return JSONResponse(status_code=201, content={"status": "created", "text_id": text.TextID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/text/{content_id}/{text_id}")
def update_text(
    content_id: str,
    text_id: str,
    update_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Update text content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    text = text_service.update_text(content_id, text_id, update_data)
    if not text:
        raise HTTPException(status_code=404, detail="Text not found")
    
    return {"status": "updated"}


@router.delete("/text/{content_id}/{text_id}")
def delete_text(
    content_id: str,
    text_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Delete text content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    ok = text_service.delete_text(content_id, text_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Text not found")
    
    return {"status": "deleted"}


# ============================================================
# VIDEO ROUTES
# ============================================================

@router.post("/content/{content_id}/video")
def add_video_to_content(
    content_id: str,
    video_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Add video to content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    try:
        video_data["ContentID"] = content_id
        video = video_service.create_video(video_data)
        return JSONResponse(status_code=201, content={"status": "created", "video_id": video.VideoID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/video/{content_id}/{video_id}")
def update_video(
    content_id: str,
    video_id: str,
    update_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Update video content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    video = video_service.update_video(content_id, video_id, update_data)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {"status": "updated"}


@router.delete("/video/{content_id}/{video_id}")
def delete_video(
    content_id: str,
    video_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Delete video content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    ok = video_service.delete_video(content_id, video_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return {"status": "deleted"}


# ============================================================
# IMAGE ROUTES
# ============================================================

@router.post("/content/{content_id}/image")
def add_image_to_content(
    content_id: str,
    image_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Add image to content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    try:
        image_data["ContentID"] = content_id
        image = image_service.create_image(image_data)
        return JSONResponse(status_code=201, content={"status": "created", "image_id": image.ImageID})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/image/{content_id}/{image_id}")
def update_image(
    content_id: str,
    image_id: str,
    update_data: Dict[str, Any] = Body(...),
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Update image content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    image = image_service.update_image(content_id, image_id, update_data)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {"status": "updated"}


@router.delete("/image/{content_id}/{image_id}")
def delete_image(
    content_id: str,
    image_id: str,
    current_user: CurrentUser = Depends(get_current_user_from_session)
):
    """Delete image content"""
    if current_user.role == 'tutee':
        raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
    
    ok = image_service.delete_image(content_id, image_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {"status": "deleted"}