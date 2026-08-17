from src.domain.models.EventComment import EventComment
from src.infrastructure.repositories.EventCommentRepository import EventCommentRepository


class ListEventCommentsUseCase:
    def __init__(self, repository: EventCommentRepository):
        self._repository = repository

    async def execute(self, event_id: int) -> list[EventComment]:
        return await self._repository.list_by_event(event_id)