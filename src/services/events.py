from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.models.CentralOffice import CentralOffice
from src.domain.models.Event import Event
from src.services.geo import point_from_coords, coords_from_point
from src.domain.schemas.Event import EventCreate


async def calculate_distance_km(
    session: AsyncSession, office_id: int, longitude: float, latitude: float
) -> float:
    result = await session.execute(
        select(
            func.ST_Distance(
                CentralOffice.location,
                func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
            )
            / 1000.0
        ).where(CentralOffice.id == office_id)
    )
    return result.scalar_one()


async def create_event(
    session: AsyncSession, payload: EventCreate, reported_by_id: int
) -> Event:
    distance_to_origin = await calculate_distance_km(
        session, payload.origin_office_id, payload.longitude, payload.latitude
    )
    distance_to_destination = await calculate_distance_km(
        session, payload.destination_office_id, payload.longitude, payload.latitude
    )

    event = Event(
        origin_office_id=payload.origin_office_id,
        destination_office_id=payload.destination_office_id,
        location=point_from_coords(payload.latitude, payload.longitude),
        location_method=payload.location_method,
        accuracy=payload.accuracy,
        distance_to_origin=distance_to_origin,
        distance_to_destination=distance_to_destination,
        field_reference=payload.field_reference,
        description=payload.description,
        reported_by_id=reported_by_id,
    )

    session.add(event)
    await session.commit()
    await session.refresh(event)
    return await get_event(session, event.id)


async def get_event(session: AsyncSession, event_id: int) -> Event | None:
    result = await session.execute(
        select(Event)
        .options(
            selectinload(Event.origin_office),
            selectinload(Event.destination_office),
            selectinload(Event.photos),
        )
        .where(Event.id == event_id)
    )
    return result.scalar_one_or_none()


async def list_events(
    session: AsyncSession, status: str | None = None
) -> list[Event]:
    query = select(Event).options(
        selectinload(Event.origin_office),
        selectinload(Event.destination_office),
        selectinload(Event.photos),
    )
    if status:
        query = query.where(Event.status == status)

    result = await session.execute(query.order_by(Event.reported_at.desc()))
    return list(result.scalars().all())


def event_to_read_dict(event: Event) -> dict:
    """Flattens location + relationships into the shape EventRead expects."""
    latitude, longitude = coords_from_point(event.location)
    return {
        "id": event.id,
        "type": event.type,
        "origin_office": event.origin_office,
        "destination_office": event.destination_office,
        "latitude": latitude,
        "longitude": longitude,
        "location_method": event.location_method,
        "accuracy": event.accuracy,
        "distance_to_origin": event.distance_to_origin,
        "distance_to_destination": event.distance_to_destination,
        "field_reference": event.field_reference,
        "description": event.description,
        "status": event.status,
        "reported_by_id": event.reported_by_id,
        "reported_at": event.reported_at,
        "photos": event.photos,
        "created_at": event.created_at,
        "updated_at": event.updated_at,
    }