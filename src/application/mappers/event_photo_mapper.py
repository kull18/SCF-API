from src.domain.schemas.EventPhoto import EventPhotoCreateSchema
from src.application.dtos.responses.event_photo_response import EventPhotoResponse
from src.domain.models.EventPhoto import EventPhoto


class EventPhotoMapper:
    @staticmethod
    def schema_to_model(schema: EventPhotoCreateSchema) -> EventPhoto:
        return EventPhoto(
            event_id=schema.event_id,
            url=schema.url,
            label=schema.label,
            size_bytes=schema.size_bytes,
        )

    @staticmethod
    def model_to_response(model: EventPhoto) -> EventPhotoResponse:
        return EventPhotoResponse(
            id=model.id,
            event_id=model.event_id,
            url=model.url,
            label=model.label,
            size_bytes=model.size_bytes,
            uploaded_at=model.uploaded_at,
        )