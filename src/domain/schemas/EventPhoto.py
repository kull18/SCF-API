from pydantic import BaseModel


class EventPhotoCreateSchema(BaseModel):
    event_id: int
    url: str
    label: str | None = None
    size_bytes: int | None = None