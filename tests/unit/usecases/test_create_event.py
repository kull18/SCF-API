import pytest
from unittest.mock import AsyncMock, patch

from src.application.usecases.CreateEventUseCase import CreateEventUseCase
from src.domain.models.Event import Event, EventType, LocationMethod, EventStatus


@pytest.mark.asyncio
async def test_calculates_both_distances_before_creating():
    repository = AsyncMock()
    repository.calculate_distance_km.side_effect = [4.8, 7.2]

    created_event = Event(
        id=1, type=EventType.FIBER_CUT, origin_office_id=1, destination_office_id=2,
        location="POINT(-93.1 16.7)", location_method=LocationMethod.GPS, accuracy=8.2,
        distance_to_origin=4.8, distance_to_destination=7.2,
        description="test", status=EventStatus.ACTIVE, reported_by_id=1,
    )
    repository.create.return_value = created_event

    notify_use_case = AsyncMock()

    with patch(
        "src.application.usecases.CreateEventUseCase.coords_from_point",
        return_value=(16.7, -93.1),
    ):
        use_case = CreateEventUseCase(repository, notify_use_case)
        event = Event(
            type=EventType.FIBER_CUT, origin_office_id=1, destination_office_id=2,
            location="POINT(-93.1 16.7)", location_method=LocationMethod.GPS, accuracy=8.2,
            distance_to_origin=0, distance_to_destination=0,
            description="test", status=EventStatus.ACTIVE, reported_by_id=1,
        )

        result = await use_case.execute(event)

    assert repository.calculate_distance_km.await_count == 2
    notify_use_case.execute.assert_awaited_once_with(created_event)
    assert result.distance_to_origin == 4.8