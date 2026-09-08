from datetime import datetime, timedelta, timezone

from src.domain.models.Event import EventStatus
from src.infrastructure.repositories.EventRepository import EventRepository

RESOLVED_TO_CLOSED_HOURS = 24


class CloseResolvedEventsUseCase:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    async def execute(self) -> int:
        """Cierra automaticamente los eventos que llevan mas de
        RESOLVED_TO_CLOSED_HOURS en estado RESOLVED. Retorna cuantos se cerraron."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=RESOLVED_TO_CLOSED_HOURS)
        events = await self._repository.list_resolved_before(cutoff)

        for event in events:
            event.status = EventStatus.CLOSED
            await self._repository.update(event)

        return len(events)