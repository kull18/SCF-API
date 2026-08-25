from src.domain.models.Event import Event
from src.infrastructure.repositories.EventRepository import EventRepository
from src.core.exceptions import NotFoundError


class GetEventUseCase:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    async def execute(self, event_id: int) -> Event:
        event = await self._repository.get_by_id(event_id)
        if event is None:
            raise NotFoundError(f"Event with id={event_id} not found")
        return event