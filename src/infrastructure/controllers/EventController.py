from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.core.middlewares.role_middleware import require_role
from src.domain.models.User import User, UserRole
from src.infrastructure.repositories.EventRepository import EventRepository
from src.application.usecases.CreateEventUseCase import CreateEventUseCase
from src.application.usecases.ListEventsUseCase import ListEventsUseCase
from src.application.usecases.UpdateEventUseCase import UpdateEventUseCase
from src.domain.schemas.Event import EventCreateSchema, EventUpdateSchema
from src.domain.models.Event import EventStatus
from src.application.dtos.responses.event_response import EventResponse
from src.application.mappers.event_mapper import EventMapper

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(
    schema: EventCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = EventRepository(session)
    use_case = CreateEventUseCase(repository)

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