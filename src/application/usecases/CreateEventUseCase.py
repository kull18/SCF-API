from src.domain.models.Event import Event
from src.infrastructure.repositories.EventRepository import EventRepository
from src.services.geo import coords_from_point
from src.application.usecases.NotifyEventCreatedUseCase import NotifyEventCreatedUseCase

class CreateEventUseCase:
    def __init__(self, repository: EventRepository, notify_use_case: NotifyEventCreatedUseCase):
        self._repository = repository
        self._notify_use_case = notify_use_case

    async def execute(self, event: Event) -> Event:
        latitude, longitude = coords_from_point(event.location)

        event.distance_to_origin = await self._repository.calculate_distance_km(
            event.origin_office_id, latitude, longitude
        )
        event.distance_to_destination = await self._repository.calculate_distance_km(
            event.destination_office_id, latitude, longitude
        )

        created = await self._repository.create(event)
        await self._notify_use_case.execute(created)
        return created