from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.core.middlewares.role_middleware import require_role
from src.domain.models.User import User, UserRole
from src.infrastructure.repositories.NotificationRepository import NotificationRepository
from src.application.usecases.MarkNotificationAsReadUseCase import (
    MarkNotificationAsReadUseCase,
)
from src.domain.schemas.Notification import DeviceTokenSchema
from src.application.dtos.responses.notification_response import NotificationResponse
from src.application.mappers.notification_mapper import NotificationMapper

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = NotificationRepository(session)
    notifications = await repository.list_by_user(current_user.id)
    return [NotificationMapper.model_to_response(n) for n in notifications]


@router.get("/unread-count")
async def get_unread_count(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = NotificationRepository(session)
    count = await repository.count_unread(current_user.id)
    return {"unread_count": count}


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_as_read(
    notification_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = NotificationRepository(session)
    use_case = MarkNotificationAsReadUseCase(repository)
    updated = await use_case.execute(notification_id)
    return NotificationMapper.model_to_response(updated)


@router.post("/device-token", status_code=204)
async def register_device_token(
    schema: DeviceTokenSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    current_user.onesignal_player_id = schema.player_id
    await session.commit()