from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.models.EventComment import EventComment


class EventCommentRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, comment: EventComment) -> EventComment:
        self._session.add(comment)
        await self._session.commit()
        await self._session.refresh(comment, attribute_names=["user"])
        return comment

    async def list_by_event(self, event_id: int) -> list[EventComment]:
        result = await self._session.execute(
            select(EventComment)
            .options(selectinload(EventComment.user))
            .where(EventComment.event_id == event_id)
            .order_by(EventComment.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, comment_id: int) -> EventComment | None:
        result = await self._session.execute(
            select(EventComment)
            .options(selectinload(EventComment.user))
            .where(EventComment.id == comment_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, comment_id: int) -> None:
     comment = await self._session.get(EventComment, comment_id)
     if comment is not None:
        await self._session.delete(comment)
        await self._session.commit()