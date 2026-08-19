from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.EventPhoto import EventPhoto


class EventPhotoRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, photo: EventPhoto) -> EventPhoto:
        self._session.add(photo)
        await self._session.commit()
        await self._session.refresh(photo)
        return photo

    async def list_by_event(self, event_id: int) -> list[EventPhoto]:
        result = await self._session.execute(
            select(EventPhoto).where(EventPhoto.event_id == event_id)
        )
        return list(result.scalars().all())

    async def delete(self, photo_id: int) -> None:
     photo = await self._session.get(EventPhoto, photo_id)
     if photo is not None:
        await self._session.delete(photo)
        await self._session.commit()