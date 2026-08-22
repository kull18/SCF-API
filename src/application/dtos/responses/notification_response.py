from datetime import datetime

from pydantic import BaseModel

from src.domain.models.Notification import NotificationType


class NotificationResponse(BaseModel):
    id: int
    title: str
    body: str
    type: NotificationType
    related_event_id: int | None
    is_read: bool
    created_at: datetime