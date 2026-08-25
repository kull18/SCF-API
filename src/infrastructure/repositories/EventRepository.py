from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

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
                selectinload(Event.photos),
            )
            .where(Event.id == event_id)
        )
        return result.scalar_one_or_none()

    async def list(self, status: EventStatus | None = None) -> list[Event]:
        query = select(Event).options(
            selectinload(Event.origin_office),
            selectinload(Event.destination_office),
            selectinload(Event.photos),
        )
        if status:
            query = query.where(Event.status == status)
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