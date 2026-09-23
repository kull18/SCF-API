from __future__ import annotations
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.domain.models.Event import Event, EventStatus
from src.domain.models.CentralOffice import CentralOffice


class EventRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, event: Event) -> Event:
        self._session.add(event)
        await self._session.commit()
        await self._session.refresh(event)
        return event

    async def get_by_id(self, event_id: int) -> Event | None:
        result = await self._session.execute(
            select(Event)
            .options(
                selectinload(Event.origin_office),
                selectinload(Event.destination_office),
                selectinload(Event.reported_by),
                selectinload(Event.photos),
            )
            .where(Event.id == event_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        status: EventStatus | None = None,
        reported_by_id: int | None = None,
    ) -> list[Event]:
        query = select(Event).options(
            selectinload(Event.origin_office),
            selectinload(Event.destination_office),
            selectinload(Event.reported_by),
            selectinload(Event.photos),
        )
        if status:
            query = query.where(Event.status == status)
        if reported_by_id:
            query = query.where(Event.reported_by_id == reported_by_id)

        result = await self._session.execute(query.order_by(Event.reported_at.desc()))
        return list(result.scalars().all())

    async def update(self, event: Event) -> Event:
        await self._session.commit()
        await self._session.refresh(event)
        return event

    async def calculate_distance_km(
        self, office_id: int, latitude: float, longitude: float
    ) -> float:
        result = await self._session.execute(
            select(
                func.ST_Distance(
                    CentralOffice.location,
                    func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
                )
                / 1000.0
            ).where(CentralOffice.id == office_id)
        )
        return result.scalar_one()

    async def list_resolved_before(self, cutoff: datetime) -> list[Event]:
        result = await self._session.execute(
            select(Event).where(
                Event.status == EventStatus.RESOLVED,
                Event.updated_at < cutoff,
            )
        )
        return list(result.scalars().all())

    async def delete(self, event_id: int) -> None:
        event = await self._session.get(Event, event_id)
        if event is not None:
            await self._session.delete(event)
            await self._session.commit()