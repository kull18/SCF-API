from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.Notification import Notification


class NotificationRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, notification: Notification) -> Notification:
        self._session.add(notification)
        await self._session.commit()
        await self._session.refresh(notification)
        return notification

    async def list_by_user(self, user_id: int) -> list[Notification]:
        result = await self._session.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        return list(result.scalars().all())

    async def count_unread(self, user_id: int) -> int:
        result = await self._session.execute(
            select(func.count())
            .select_from(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
        )
        return result.scalar_one()

    async def mark_as_read(self, notification_id: int) -> Notification:
        notification = await self._session.get(Notification, notification_id)
        if notification is None:
            raise ValueError(f"Notification with id={notification_id} not found")
        notification.is_read = True
        await self._session.commit()
        await self._session.refresh(notification)
        return notification