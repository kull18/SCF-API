from src.domain.schemas.Event import EventUpdateSchema
from src.domain.models.Event import Event
from src.infrastructure.repositories.EventRepository import EventRepository


class UpdateEventUseCase:
    def __init__(self, repository: EventRepository):
        self._repository = repository

    async def execute(self, event_id: int, schema: EventUpdateSchema) -> Event:
        event = await self._repository.get_by_id(event_id)
        if event is None:
            raise ValueError(f"Event with id={event_id} not found")

        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(event, field, value)

        return await self._repository.update(event)