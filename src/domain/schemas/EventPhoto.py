from pydantic import BaseModel


class EventPhotoCreateSchema(BaseModel):
    event_id: int
    object_key: str
    label: str | None = None
    size_bytes: int | None = None