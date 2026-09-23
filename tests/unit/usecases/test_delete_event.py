import pytest
from unittest.mock import AsyncMock

from src.application.usecases.DeleteEventUseCase import DeleteEventUseCase
from src.domain.models.Event import Event, EventType, LocationMethod, EventStatus
from src.core.exceptions import NotFoundError, ForbiddenError


def _make_event(reported_by_id=12):
    return Event(
        id=42,
        type=EventType.FIBER_CUT,
        origin_office_id=1,
        destination_office_id=2,
        location="POINT(-93.1 16.7)",
        location_method=LocationMethod.GPS,
        accuracy=8.2,
        distance_to_origin=4.8,
        distance_to_destination=7.2,
        description="test",
        status=EventStatus.ACTIVE,
        reported_by_id=reported_by_id,
    )


@pytest.mark.asyncio
async def test_owner_can_delete_own_event():
    repository = AsyncMock()
    repository.get_by_id.return_value = _make_event(reported_by_id=12)

    use_case = DeleteEventUseCase(repository)
    await use_case.execute(event_id=42, requesting_user_id=12)

    repository.delete.assert_awaited_once_with(42)


@pytest.mark.asyncio
async def test_non_owner_cannot_delete_event():
    repository = AsyncMock()
    repository.get_by_id.return_value = _make_event(reported_by_id=12)

    use_case = DeleteEventUseCase(repository)

    with pytest.raises(ForbiddenError):
        await use_case.execute(event_id=42, requesting_user_id=99)

    repository.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_raises_not_found_when_event_missing():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    use_case = DeleteEventUseCase(repository)

    with pytest.raises(NotFoundError):
        await use_case.execute(event_id=99, requesting_user_id=12)

    repository.delete.assert_not_awaited()
