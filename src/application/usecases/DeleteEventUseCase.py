from src.infrastructure.repositories.EventRepository import EventRepository
from src.core.exceptions import NotFoundError, ForbiddenError


class DeleteEventUseCase:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    async def execute(self, event_id: int, requesting_user_id: int) -> None:
        event = await self._repository.get_by_id(event_id)
        if event is None:
            raise NotFoundError(f"Event with id={event_id} not found")

        if event.reported_by_id != requesting_user_id:
            raise ForbiddenError("You can only delete events you reported")

        await self._repository.delete(event_id)
