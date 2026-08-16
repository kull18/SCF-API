from src.domain.models.EventPhoto import EventPhoto
from src.infrastructure.repositories.EventPhotoRepository import EventPhotoRepository
from src.infrastructure.repositories.EventRepository import EventRepository


class CreateEventPhotoUseCase:
    def __init__(
        self, photo_repository: EventPhotoRepository, event_repository: EventRepository
    ):
        self._photo_repository = photo_repository
        self._event_repository = event_repository

    async def execute(self, photo: EventPhoto) -> EventPhoto:
        event = await self._event_repository.get_by_id(photo.event_id)
        if event is None:
            raise ValueError(f"Event with id={photo.event_id} not found")

        return await self._photo_repository.create(photo)