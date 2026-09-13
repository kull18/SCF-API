import pytest
from unittest.mock import AsyncMock

from src.application.usecases.MarkNotificationAsReadUseCase import MarkNotificationAsReadUseCase
from src.domain.models.Notification import Notification, NotificationType
from src.core.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_marks_existing_notification_as_read():
    notification = Notification(
        id=1, user_id=1, title="test", body="test",
        type=NotificationType.EVENT_CREATED, is_read=False,
    )
    repository = AsyncMock()
    repository.get_by_id.return_value = notification
    repository.update.return_value = notification

    use_case = MarkNotificationAsReadUseCase(repository)
    result = await use_case.execute(1)

    assert result.is_read is True
    repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_raises_not_found_when_notification_missing():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    use_case = MarkNotificationAsReadUseCase(repository)

    with pytest.raises(NotFoundError):
        await use_case.execute(99)