from datetime import datetime

from pydantic import BaseModel


class EventCommentAuthorResponse(BaseModel):
    id: int
    technician_code: str
    full_name: str


class EventCommentResponse(BaseModel):
    id: int
    event_id: int
    content: str
    author: EventCommentAuthorResponse
    created_at: datetime