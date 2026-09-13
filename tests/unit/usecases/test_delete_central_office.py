import pytest
from unittest.mock import AsyncMock

from src.application.usecases.DeleteCentralOfficeUseCase import DeleteCentralOfficeUseCase
from src.domain.models.CentralOffice import CentralOffice
from src.core.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_deletes_when_office_exists():
    repository = AsyncMock()
    repository.get_by_id.return_value = CentralOffice(id=1, prefix="TGZ", name="Tuxtla", city="Tuxtla")

    use_case = DeleteCentralOfficeUseCase(repository)
    await use_case.execute(1)

    repository.delete.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_raises_not_found_when_office_does_not_exist():
    repository = AsyncMock()
    repository.get_by_id.return_value = None

    use_case = DeleteCentralOfficeUseCase(repository)

    with pytest.raises(NotFoundError):
        await use_case.execute(99)

    repository.delete.assert_not_awaited()