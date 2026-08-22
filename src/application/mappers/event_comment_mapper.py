from src.domain.schemas.EventComment import EventCommentCreateSchema
from src.application.dtos.responses.event_comment_response import (
    EventCommentResponse,
    EventCommentAuthorResponse,
)
from src.domain.models.EventComment import EventComment


class EventCommentMapper:
    @staticmethod
    def schema_to_model(schema: EventCommentCreateSchema, user_id: int) -> EventComment:
        return EventComment(
            event_id=schema.event_id,
            user_id=user_id,
            content=schema.content,
        )

    @staticmethod
    def model_to_response(model: EventComment) -> EventCommentResponse:
        return EventCommentResponse(
            id=model.id,
            event_id=model.event_id,
            content=model.content,
            author=EventCommentAuthorResponse(
                id=model.user.id,
                technician_code=model.user.technician_code,
                full_name=model.user.full_name,
            ),
            created_at=model.created_at,
        )