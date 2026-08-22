from src.domain.models.Event import Event, EventStatus
from src.infrastructure.repositories.EventRepository import EventRepository


class ListEventsUseCase:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    async def execute(self, status: EventStatus | None = None) -> list[Event]:
        return await self._repository.list(status=status)