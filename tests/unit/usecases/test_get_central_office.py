import pytest
from unittest.mock import AsyncMock

from src.application.usecases.GetCentralOfficeUseCase import GetCentralOfficeUseCase
from src.domain.models.CentralOffice import CentralOffice
from src.core.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_returns_office_when_found():
    repository = AsyncMock()
    repository.get_by_id.return_value = CentralOffice(id=1, prefix="TGZ", name="Tuxtla", city="Tuxtla")

    use_case = GetCentralOfficeUseCase(repository)
    result = await use_case.execute(1)

    assert result.id == 1


@pytest.mark.asyncio
async def test_raises_not_found_when_missing():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    use_case = GetCentralOfficeUseCase(repository)

    with pytest.raises(NotFoundError, match="id=99"):
        await use_case.execute(99)