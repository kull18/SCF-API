from src.domain.schemas.EventPhoto import EventPhotoCreateSchema
from src.application.dtos.responses.event_photo_response import EventPhotoResponse
from src.domain.models.EventPhoto import EventPhoto
from src.services.s3_service import generate_download_presigned_url


class EventPhotoMapper:
    @staticmethod
    def schema_to_model(schema: EventPhotoCreateSchema) -> EventPhoto:
        return EventPhoto(
            event_id=schema.event_id,
            url=schema.object_key,  # el campo url del modelo ahora GUARDA el object_key
            label=schema.label,
            size_bytes=schema.size_bytes,
        )

    @staticmethod
    def model_to_response(model: EventPhoto) -> EventPhotoResponse:
        return EventPhotoResponse(
            id=model.id,
            event_id=model.event_id,
            url=generate_download_presigned_url(model.url),  # model.url = object_key guardado
            label=model.label,
            size_bytes=model.size_bytes,
            uploaded_at=model.uploaded_at,
        )