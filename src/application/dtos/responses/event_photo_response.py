from datetime import datetime

from pydantic import BaseModel


class EventPhotoResponse(BaseModel):
    id: int
    event_id: int
    url: str
    label: str | None
    size_bytes: int | None
    uploaded_at: datetime