from pydantic import BaseModel


# PUBLIC_INTERFACE
class Notification(BaseModel):
    id: int
    message: str
    channel: str


# PUBLIC_INTERFACE
class NotificationCreate(BaseModel):
    message: str
    channel: str

