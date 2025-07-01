from fastapi import APIRouter, Depends
from typing import List, Dict
from ..models.notifications import Notification, NotificationCreate
from ..middleware import get_current_user
from .auth import require_roles, Role, User


router = APIRouter()

_NOTIFICATIONS: Dict[int, Notification] = {}
_next_notification_id = 1


class NotificationDispatcher:
    def send_slack(self, message, channel):
        pass

    def send_discord(self, message, channel):
        pass

    def send_email(self, message, recipient):
        pass


dispatcher_stub = NotificationDispatcher()


# PUBLIC_INTERFACE
@router.get("/", response_model=List[Notification], summary="List all notifications", tags=["Notifications"])
async def list_notifications(current_user: User = Depends(get_current_user)):
    # Only admins/reviewers see all, developers see only their notifications (not implemented in demo)
    return list(_NOTIFICATIONS.values())


# PUBLIC_INTERFACE
@router.post(
    "/",
    response_model=Notification,
    summary="Send a notification",
    tags=["Notifications"],
    responses={403: {"description": "Forbidden"}},
)
async def create_notification(
    notification: NotificationCreate,
    current_user: User = Depends(get_current_user)
):
    require_roles(current_user, [Role.ADMIN, Role.REVIEWER])
    global _next_notification_id
    new_notification = Notification(
        id=_next_notification_id,
        message=notification.message,
        channel=notification.channel,
    )
    _NOTIFICATIONS[_next_notification_id] = new_notification
    _next_notification_id += 1
    # Dispatcher stub: Could send via Slack, Discord, etc.
    return new_notification
