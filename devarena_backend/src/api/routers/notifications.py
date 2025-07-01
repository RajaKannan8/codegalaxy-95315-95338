from fastapi import APIRouter
from ..models.notifications import Notification, NotificationCreate

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=list[Notification])
async def list_notifications():
    return []


# PUBLIC_INTERFACE
@router.post("/", response_model=Notification)
async def create_notification(notification: NotificationCreate):
    return Notification(
        id=1,
        message=notification.message,
        channel=notification.channel,
    )
