from fastapi import APIRouter, Depends, HTTPException
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
from src.services.s3_service import build_event_photo_key, generate_upload_presigned_url

router = APIRouter(prefix="/event-photos", tags=["event-photos"])


@router.get("/upload-url")
async def get_upload_url(
    event_id: int,
    filename: str,
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    object_key = build_event_photo_key(event_id, filename)
    upload_url = generate_upload_presigned_url(object_key)

    return {
        "upload_url": upload_url,
        "object_key": object_key,
    }


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

    try:
        model = EventPhotoMapper.schema_to_model(schema)
        created = await use_case.execute(model)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

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