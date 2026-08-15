from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventPhotoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
    url: str
    label: str | None
    size_bytes: int | None
    uploaded_at: datetime