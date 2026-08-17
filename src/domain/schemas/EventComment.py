from pydantic import BaseModel, Field


class EventCommentCreateSchema(BaseModel):
    event_id: int
    content: str = Field(min_length=1, max_length=1000)