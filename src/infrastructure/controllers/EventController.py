from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecases import NotifyEventCreatedUseCase
from src.infrastructure.repositories import NotificationRepository
from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.core.middlewares.role_middleware import require_role
from src.domain.models.User import User, UserRole
from src.infrastructure.repositories import UserRepository
from src.infrastructure.repositories.EventRepository import EventRepository
from src.application.usecases.CreateEventUseCase import CreateEventUseCase
from src.application.usecases.ListEventsUseCase import ListEventsUseCase
from src.application.usecases.UpdateEventUseCase import UpdateEventUseCase
from src.domain.schemas.Event import EventCreateSchema, EventUpdateSchema
from src.domain.models.Event import EventStatus
from src.application.dtos.responses.event_response import EventResponse
from src.application.mappers.event_mapper import EventMapper
from src.services.s3_service import (
    build_content_addressed_key,
    generate_upload_presigned_url,
    object_exists,
)
router = APIRouter(prefix="/events", tags=["events"])



@router.get("/upload-url")
async def get_upload_url(
    event_id: int,
    filename: str,
    content_hash: str,  # SHA-256 calculado en el cliente
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    object_key = build_content_addressed_key("events", event_id, content_hash, filename)

    if object_exists(object_key):
        # Ya existe una foto idéntica subida antes — el cliente se salta el PUT a S3
        return {
            "upload_url": None,
            "object_key": object_key,
            "already_exists": True,
        }

    upload_url = generate_upload_presigned_url(object_key)
    return {
        "upload_url": upload_url,
        "object_key": object_key,
        "already_exists": False,
    }

@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    schema: EventCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    event_repository = EventRepository(session)
    notification_repository = NotificationRepository(session)
    user_repository = UserRepository(session)

    notify_use_case = NotifyEventCreatedUseCase(notification_repository, user_repository)
    use_case = CreateEventUseCase(event_repository, notify_use_case)

    model = EventMapper.schema_to_model(schema, reported_by_id=current_user.id)
    created = await use_case.execute(model)

    return EventMapper.model_to_response(created)

@router.get("", response_model=list[EventResponse])
async def list_events(
    status: EventStatus | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = EventRepository(session)
    use_case = ListEventsUseCase(repository)

    events = await use_case.execute(status=status)
    return [EventMapper.model_to_response(e) for e in events]


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    schema: EventUpdateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = EventRepository(session)
    use_case = UpdateEventUseCase(repository)

    try:
        updated = await use_case.execute(event_id, schema)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return EventMapper.model_to_response(updated)