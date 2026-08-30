from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.core.middlewares.role_middleware import require_role
from src.domain.models.User import User, UserRole
from src.infrastructure.repositories.EventRepository import EventRepository
from src.infrastructure.repositories.NotificationRepository import NotificationRepository
from src.infrastructure.repositories.UserRepository import UserRepository
from src.application.usecases.CreateEventUseCase import CreateEventUseCase
from src.application.usecases.ListEventsUseCase import ListEventsUseCase
from src.application.usecases.UpdateEventUseCase import UpdateEventUseCase
from src.application.usecases.NotifyEventCreatedUseCase import NotifyEventCreatedUseCase
from src.domain.schemas.Event import EventCreateSchema, EventUpdateSchema
from src.domain.models.Event import EventStatus
from src.application.dtos.responses.event_response import EventResponse
from src.application.mappers.event_mapper import EventMapper
from src.application.usecases.GetEventUseCase import GetEventUseCase

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    schema: EventCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO, UserRole.ADMIN)),
):
    event_repository = EventRepository(session)
    notification_repository = NotificationRepository(session)
    user_repository = UserRepository(session)

    notify_use_case = NotifyEventCreatedUseCase(notification_repository, user_repository)
    use_case = CreateEventUseCase(event_repository, notify_use_case)

    model = EventMapper.schema_to_model(schema, reported_by_id=current_user.id)
    created = await use_case.execute(model)

    # Tras crear, recargamos con las relaciones para poder mapear la respuesta
    full_event = await event_repository.get_by_id(created.id)
    return EventMapper.model_to_response(
        full_event, full_event.origin_office, full_event.destination_office
    )


@router.get("", response_model=list[EventResponse])
async def list_events(
    status: EventStatus | None = Query(default=None),
    reported_by: str | None = Query(
        default=None, description="Usa 'me' para filtrar solo eventos propios"
    ),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = EventRepository(session)
    use_case = ListEventsUseCase(repository)

    reported_by_id = current_user.id if reported_by == "me" else None
    events = await use_case.execute(status=status, reported_by_id=reported_by_id)

    return [
        EventMapper.model_to_response(e, e.origin_office, e.destination_office)
        for e in events
    ]


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    schema: EventUpdateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO, UserRole.ADMIN)),
):
    repository = EventRepository(session)
    use_case = UpdateEventUseCase(repository)
    updated = await use_case.execute(event_id, schema)

    full_event = await repository.get_by_id(updated.id)
    return EventMapper.model_to_response(
        full_event, full_event.origin_office, full_event.destination_office
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO, UserRole.ADMIN)),
):
    repository = EventRepository(session)
    use_case = GetEventUseCase(repository)

    event = await use_case.execute(event_id)

    return EventMapper.model_to_response(event, event.origin_office, event.destination_office)