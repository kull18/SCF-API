import pytest
from unittest.mock import AsyncMock

from src.application.usecases.UpdateEventUseCase import UpdateEventUseCase
from src.domain.models.Event import Event, EventType, LocationMethod, EventStatus
from src.domain.schemas.Event import EventUpdateSchema
from src.core.exceptions import NotFoundError, ForbiddenError


def _make_event(reported_by_id=12):
    return Event(
        id=42, type=EventType.FIBER_CUT, origin_office_id=1, destination_office_id=2,
        location="POINT(-93.1 16.7)", location_method=LocationMethod.GPS, accuracy=8.2,
        distance_to_origin=4.8, distance_to_destination=7.2,
        description="test", status=EventStatus.ACTIVE, reported_by_id=reported_by_id,
    )


@pytest.mark.asyncio
async def test_owner_can_update_status():
    repository = AsyncMock()
    repository.get_by_id.return_value = _make_event(reported_by_id=12)
    repository.update.side_effect = lambda e: e

    use_case = UpdateEventUseCase(repository)
    schema = EventUpdateSchema(status=EventStatus.RESOLVED)

    result = await use_case.execute(42, schema, requesting_user_id=12)

    assert result.status == EventStatus.RESOLVED
    repository.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_non_owner_cannot_update_status():
    repository = AsyncMock()
    repository.get_by_id.return_value = _make_event(reported_by_id=12)

    use_case = UpdateEventUseCase(repository)
    schema = EventUpdateSchema(status=EventStatus.RESOLVED)

    with pytest.raises(ForbiddenError):
        await use_case.execute(42, schema, requesting_user_id=99)

    repository.update.assert_not_awaited()


@pytest.mark.asyncio
async def test_raises_not_found_when_event_missing():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    use_case = UpdateEventUseCase(repository)
    schema = EventUpdateSchema(status=EventStatus.RESOLVED)

    with pytest.raises(NotFoundError):
        await use_case.execute(99, schema, requesting_user_id=1)