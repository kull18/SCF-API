import pytest
from unittest.mock import AsyncMock

from src.application.usecases.DeleteEventCommentUseCase import DeleteEventCommentUseCase
from src.domain.models.EventComment import EventComment
from src.core.exceptions import NotFoundError, ForbiddenError


@pytest.mark.asyncio
async def test_author_can_delete_own_comment():
    repository = AsyncMock()
    repository.get_by_id.return_value = EventComment(id=1, event_id=1, user_id=42, content="test")

    use_case = DeleteEventCommentUseCase(repository)
    await use_case.execute(comment_id=1, requesting_user_id=42)

    repository.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_non_author_cannot_delete_comment():
    repository = AsyncMock()
    repository.get_by_id.return_value = EventComment(id=1, event_id=1, user_id=42, content="test")

    use_case = DeleteEventCommentUseCase(repository)

    with pytest.raises(ForbiddenError):
        await use_case.execute(comment_id=1, requesting_user_id=99)

    repository.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_raises_not_found_when_comment_missing():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    use_case = DeleteEventCommentUseCase(repository)

    with pytest.raises(NotFoundError):
        await use_case.execute(comment_id=99, requesting_user_id=42)