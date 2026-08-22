from src.domain.models.EventPhoto import EventPhoto
from src.infrastructure.repositories.EventPhotoRepository import EventPhotoRepository


class ListEventPhotosUseCase:
    def __init__(self, repository: EventPhotoRepository):
        self._repository = repository

    async def execute(self, event_id: int) -> list[EventPhoto]:
        return await self._repository.list_by_event(event_id)