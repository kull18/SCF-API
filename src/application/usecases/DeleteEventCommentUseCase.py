from src.infrastructure.repositories.EventCommentRepository import EventCommentRepository


class DeleteEventCommentUseCase:
    def __init__(self, repository: EventCommentRepository):
        self._repository = repository

    async def execute(self, comment_id: int, requesting_user_id: int) -> None:
        comment = await self._repository.get_by_id(comment_id)
        if comment is None:
            raise ValueError(f"EventComment with id={comment_id} not found")

        if comment.user_id != requesting_user_id:
            raise PermissionError("You can only delete your own comments")

        await self._repository.delete(comment_id)