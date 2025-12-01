from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from .auth import *
from typing import Dict, Any
from ..models import mudemy_session
from ..services import ResourceService

router = APIRouter()

resource_service = ResourceService(mudemy_session)


@router.post("/resources")
def create_resource(data: Dict[str, Any] = Body(...), current_user: CurrentUser = Depends(get_current_user_from_session)):
	# only instructors may create resources
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

	r = resource_service.create_resource(data)
	return JSONResponse(status_code=201, content={"status": "created", "resource_id": r.ResourceID})


@router.get("/resources/{resource_id}")
def read_resource(resource_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	r = resource_service.get_resource_by_id(resource_id)
	if not r:
		raise HTTPException(status_code=404, detail="Resource not found")
	return {"status": "success", "resource": {"ResourceID": r.ResourceID, "File_Name": getattr(r, 'File_Name', None)}}


@router.delete("/resources/{resource_id}")
def delete_resource(resource_id: str, current_user: CurrentUser = Depends(get_current_user_from_session)):
	if current_user.role == 'tutee':
		raise HTTPException(status_code=403, detail="Not authorized, requires INSTRUCTOR role")

	ok = resource_service.delete_resource(resource_id)
	if not ok:
		raise HTTPException(status_code=404, detail="Resource not found")
	return {"status": "deleted", "resource_id": resource_id}

