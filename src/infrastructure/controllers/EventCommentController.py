from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.core.middlewares.role_middleware import require_role
from src.domain.models.User import User, UserRole
from src.infrastructure.repositories.EventCommentRepository import EventCommentRepository
from src.infrastructure.repositories.EventRepository import EventRepository
from src.application.usecases.CreateEventCommentUseCase import CreateEventCommentUseCase
from src.application.usecases.ListEventCommentsUseCase import ListEventCommentsUseCase
from src.application.usecases.DeleteEventCommentUseCase import DeleteEventCommentUseCase
from src.domain.schemas.EventComment import EventCommentCreateSchema
from src.application.dtos.responses.event_comment_response import EventCommentResponse
from src.application.mappers.event_comment_mapper import EventCommentMapper

router = APIRouter(prefix="/event-comments", tags=["event-comments"])


@router.post("", response_model=EventCommentResponse, status_code=201)
async def create_event_comment(
    schema: EventCommentCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    comment_repository = EventCommentRepository(session)
    event_repository = EventRepository(session)
    use_case = CreateEventCommentUseCase(comment_repository, event_repository)

    model = EventCommentMapper.schema_to_model(schema, user_id=current_user.id)
    created = await use_case.execute(model)

    return EventCommentMapper.model_to_response(created)


@router.get("/event/{event_id}", response_model=list[EventCommentResponse])
async def list_event_comments(
    event_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = EventCommentRepository(session)
    use_case = ListEventCommentsUseCase(repository)
    comments = await use_case.execute(event_id)
    return [EventCommentMapper.model_to_response(c) for c in comments]


@router.delete("/{comment_id}", status_code=204)
async def delete_event_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = EventCommentRepository(session)
    use_case = DeleteEventCommentUseCase(repository)
    await use_case.execute(comment_id, requesting_user_id=current_user.id)