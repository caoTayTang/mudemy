from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from .auth import *
from typing import Dict, Any, List, Optional
from ..models import mudemy_session
from ..services import ResourceService, ProvideResourceService

router = APIRouter()

resource_service = ResourceService(mudemy_session)
provide_service = ProvideResourceService(mudemy_session)


@router.post("/resources")
def create_resource(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# only instructors may create resources
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

	r = resource_service.create_resource(data)
	return JSONResponse(status_code=201, content={"status": "created", "resource_id": r.ResourceID})


@router.get("/resources/id/{resource_id}")
def read_resource(resource_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	r = resource_service.get_resource_by_id(resource_id)
	if not r:
		raise HTTPException(status_code=404, detail=f"Resource not found: {resource_id}")
	return {"status": "success", "resource": {"ResourceID": r.ResourceID, "File_Name": getattr(r, 'File_Name', None), "External_link": getattr(r, 'External_link', None)}}


@router.get("/resources")
def list_resources(limit: int = 100, current_user: CurrentUser = Depends(get_current_user_from_session)):
	# resources are generally viewable by authenticated users
	items = resource_service.get_all_resources(limit=limit)
	return {"status": "success", "count": len(items), "resources": [{"ResourceID": i.ResourceID, "File_Name": getattr(i, 'File_Name', None)} for i in items]}


@router.get("/resources/search")
def search_resources(name: str = Query(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	items = resource_service.search_resources_by_name(name)
	return {"status": "success", "count": len(items), "resources": [{"ResourceID": i.ResourceID, "File_Name": getattr(i, 'File_Name', None)} for i in items]}


@router.get("/resources/external")
def resources_with_external_links(current_user: CurrentUser = Depends(get_current_user_from_session)):
	items = resource_service.get_resources_with_external_links()
	return {"status": "success", "count": len(items), "resources": [{"ResourceID": i.ResourceID, "External_link": getattr(i, 'External_link', None)} for i in items]}


@router.put("/resources/{resource_id}")
def update_resource(resource_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# instructor only
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	updated = resource_service.update_resource(resource_id, data)
	if not updated:
		raise HTTPException(status_code=404, detail="Resource not found")
	return {"status": "updated", "resource_id": updated.ResourceID}


@router.put("/resources/{resource_id}/file-link")
def update_resource_file_link(resource_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	file_link = data.get('file_link') or data.get('File_link')
	if not file_link:
		raise HTTPException(status_code=400, detail="Missing file_link")
	updated = resource_service.update_resource_file_link(resource_id, file_link)
	if not updated:
		raise HTTPException(status_code=404, detail="Resource not found")
	return {"status": "updated", "resource_id": updated.ResourceID}


@router.put("/resources/{resource_id}/external-link")
def update_resource_external_link(resource_id: str, data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	external_link = data.get('external_link') or data.get('External_link')
	if not external_link:
		raise HTTPException(status_code=400, detail="Missing external_link")
	updated = resource_service.update_resource_external_link(resource_id, external_link)
	if not updated:
		raise HTTPException(status_code=404, detail="Resource not found")
	return {"status": "updated", "resource_id": updated.ResourceID}


@router.get("/resources/count")
def resource_count(current_user: CurrentUser = Depends(get_current_user_from_session)):
	cnt = resource_service.get_resource_count()
	return {"status": "success", "count": cnt}


@router.delete("/resources/{resource_id}")
def delete_resource(resource_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

	ok = resource_service.delete_resource(resource_id)
	if not ok:
		raise HTTPException(status_code=404, detail="Resource not found")
	return {"status": "deleted", "resource_id": resource_id}


# ---------------------------
# ProvideResource (relationship) endpoints
# ---------------------------


@router.post("/provide")
def provide_resource(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# instructor only
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	resource_id = data.get('ResourceID')
	lesson_id = data.get('LessonID')
	if not resource_id or not lesson_id:
		raise HTTPException(status_code=400, detail="Missing ResourceID or LessonID")
	obj = provide_service.provide_resource_to_lesson(resource_id, lesson_id)
	return JSONResponse(status_code=201, content={"status": "provided", "ResourceID": obj.ResourceID, "LessonID": obj.LessonID})


@router.get("/lessons/{lesson_id}/resources")
def get_resources_by_lesson(lesson_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	items = provide_service.get_resources_by_lesson(lesson_id)
	return {"status": "success", "count": len(items), "provides": [{"ResourceID": p.ResourceID, "LessonID": p.LessonID} for p in items]}


@router.get("/resources/{resource_id}/lessons")
def get_lessons_by_resource(resource_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	items = provide_service.get_lessons_by_resource(resource_id)
	return {"status": "success", "count": len(items), "provides": [{"ResourceID": p.ResourceID, "LessonID": p.LessonID} for p in items]}


@router.delete("/provide/{resource_id}/{lesson_id}")
def remove_resource_from_lesson(resource_id: str, lesson_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	ok = provide_service.remove_resource_from_lesson(resource_id, lesson_id)
	if not ok:
		raise HTTPException(status_code=404, detail="Provide relationship not found")
	return {"status": "deleted"}


@router.post("/provide/bulk")
def bulk_provide(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	resource_ids = data.get('ResourceIDs') or data.get('resource_ids')
	lesson_id = data.get('LessonID') or data.get('lesson_id')
	if not resource_ids or not lesson_id:
		raise HTTPException(status_code=400, detail="Missing ResourceIDs or LessonID")
	provided = provide_service.bulk_provide_resources(resource_ids, lesson_id)
	return {"status": "success", "provided_count": len(provided)}


@router.get("/provide/count/lesson/{lesson_id}")
def get_resource_count_by_lesson(lesson_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	cnt = provide_service.get_resource_count_by_lesson(lesson_id)
	return {"status": "success", "lesson_id": lesson_id, "count": cnt}


@router.get("/provide/count/resource/{resource_id}")
def get_lesson_count_by_resource(resource_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	cnt = provide_service.get_lesson_count_by_resource(resource_id)
	return {"status": "success", "resource_id": resource_id, "count": cnt}


@router.delete("/provide/lesson/{lesson_id}")
def remove_all_resources_from_lesson(lesson_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	ok = provide_service.remove_all_resources_from_lesson(lesson_id)
	if not ok:
		raise HTTPException(status_code=404, detail="No resources found for lesson")
	return {"status": "deleted"}


@router.delete("/provide/resource/{resource_id}")
def remove_resource_from_all_lessons(resource_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")
	ok = provide_service.remove_resource_from_all_lessons(resource_id)
	if not ok:
		raise HTTPException(status_code=404, detail="No provides found for resource")
	return {"status": "deleted"}


