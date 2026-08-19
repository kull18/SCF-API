from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.core.middlewares.role_middleware import require_role
from src.domain.models.User import User, UserRole
from src.infrastructure.repositories.EventPhotoRepository import EventPhotoRepository
from src.infrastructure.repositories.EventRepository import EventRepository
from src.application.usecases.CreateEventPhotoUseCase import CreateEventPhotoUseCase
from src.application.usecases.ListEventPhotosUseCase import ListEventPhotosUseCase
from src.domain.schemas.EventPhoto import EventPhotoCreateSchema
from src.application.dtos.responses.event_photo_response import EventPhotoResponse
from src.application.mappers.event_photo_mapper import EventPhotoMapper
from src.services.s3_service import (
    build_content_addressed_key,
    generate_upload_presigned_url,
    object_exists,
)

router = APIRouter(prefix="/event-photos", tags=["event-photos"])


@router.get("/upload-url")
async def get_upload_url(
    event_id: int,
    filename: str,
    content_hash: str,
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    object_key = build_content_addressed_key("events", event_id, content_hash, filename)

    if object_exists(object_key):
        return {"upload_url": None, "object_key": object_key, "already_exists": True}

    upload_url = generate_upload_presigned_url(object_key)
    return {"upload_url": upload_url, "object_key": object_key, "already_exists": False}


@router.post("", response_model=EventPhotoResponse, status_code=201)
async def create_event_photo(
    schema: EventPhotoCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    photo_repository = EventPhotoRepository(session)
    event_repository = EventRepository(session)
    use_case = CreateEventPhotoUseCase(photo_repository, event_repository)

    model = EventPhotoMapper.schema_to_model(schema)
    created = await use_case.execute(model)

    return EventPhotoMapper.model_to_response(created)


@router.get("/event/{event_id}", response_model=list[EventPhotoResponse])
async def list_event_photos(
    event_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = EventPhotoRepository(session)
    use_case = ListEventPhotosUseCase(repository)

    photos = await use_case.execute(event_id)
    return [EventPhotoMapper.model_to_response(p) for p in photos]