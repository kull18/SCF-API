from src.domain.models.Event import Event
from src.infrastructure.repositories.EventRepository import EventRepository
from src.services.geo import coords_from_point


class CreateEventUseCase:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    async def execute(self, event: Event) -> Event:
        latitude, longitude = coords_from_point(event.location)

        event.distance_to_origin = await self._repository.calculate_distance_km(
            event.origin_office_id, latitude, longitude
        )
        event.distance_to_destination = await self._repository.calculate_distance_km(
            event.destination_office_id, latitude, longitude
        )

        return await self._repository.create(event)