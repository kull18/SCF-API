from src.domain.models.EventComment import EventComment
from src.infrastructure.repositories.EventCommentRepository import EventCommentRepository
from src.infrastructure.repositories.EventRepository import EventRepository


class CreateEventCommentUseCase:
    def __init__(
        self,
        comment_repository: EventCommentRepository,
        event_repository: EventRepository,
    ):
        self._comment_repository = comment_repository
        self._event_repository = event_repository

    async def execute(self, comment: EventComment) -> EventComment:
        event = await self._event_repository.get_by_id(comment.event_id)
        if event is None:
            raise ValueError(f"Event with id={comment.event_id} not found")

        return await self._comment_repository.create(comment)