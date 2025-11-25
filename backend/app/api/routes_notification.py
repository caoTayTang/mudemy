from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect
from ..models import *
from ..services import *
from fastapi.responses import JSONResponse
from ..core import *
from fastapi import Depends, HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from .auth import get_current_user_from_session
from ..core import manager
router = APIRouter()

notification_service = NotificationService(mututor_session)


@router.websocket("/ws/notifications/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


@router.get("/notifications")
def get_notifications(
    current_user: MuSession = Depends(get_current_user_from_session),
    unread_only: bool = False
):
    """Get all notifications for the current user"""
    try:
        if unread_only:
            notifications = notification_service.get_unread_by_user(current_user.user_id)
        else:
            notifications = notification_service.get_by_user(current_user.user_id)
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                "id": notification.id,
                "type": notification.type.value,
                "title": notification.title,
                "content": notification.content,
                "related_id": notification.related_id,
                "is_read": notification.is_read,
                "created_at": notification.created_at.isoformat()
            })
        
        return {
            "status": "success",
            "user_id": current_user.user_id,
            "count": len(notifications_data),
            "notifications": notifications_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get notifications: {str(e)}")

@router.post("/notifications/read")
def read_notification(
    data: dict = Body(...),
    current_user: MuSession = Depends(get_current_user_from_session)
):
    """Mark a notification as read or mark all as read"""
    noti_id = data.get('id')
    mark_all = data.get('markAll', False)
    
    try:
        if mark_all:
            count = notification_service.mark_all_as_read(current_user.user_id)
            return {
                "status": "success",
                "message": f"Marked {count} notifications as read"
            }
        
        if not noti_id:
            raise HTTPException(status_code=400, detail="Missing notification id")
        
        notification = notification_service.get_by_id(noti_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        if notification.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="You can only mark your own notifications as read")
        
        updated_notification = notification_service.mark_as_read(noti_id)
        
        return {
            "status": "success",
            "message": "Notification marked as read",
            "notification": {
                "id": updated_notification.id,
                "is_read": updated_notification.is_read
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark notification as read: {str(e)}")