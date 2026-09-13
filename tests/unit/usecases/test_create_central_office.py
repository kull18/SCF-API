import pytest
from unittest.mock import AsyncMock

from src.application.usecases.CreateCentralOfficeUseCase import CreateCentralOfficeUseCase
from src.domain.models.CentralOffice import CentralOffice
from src.core.exceptions import ConflictError


@pytest.mark.asyncio
async def test_creates_office_when_prefix_is_unique():
    repository = AsyncMock()
    repository.get_by_prefix.return_value = None
    repository.create.return_value = CentralOffice(id=1, prefix="TGZ", name="Tuxtla", city="Tuxtla Gutierrez")

    use_case = CreateCentralOfficeUseCase(repository)
    office = CentralOffice(prefix="TGZ", name="Tuxtla", city="Tuxtla Gutierrez")

    result = await use_case.execute(office)

    assert result.prefix == "TGZ"
    repository.get_by_prefix.assert_awaited_once_with("TGZ")
    repository.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_raises_conflict_when_prefix_already_exists():
    repository = AsyncMock()
    repository.get_by_prefix.return_value = CentralOffice(id=1, prefix="TGZ", name="Tuxtla", city="Tuxtla")

    use_case = CreateCentralOfficeUseCase(repository)
    office = CentralOffice(prefix="TGZ", name="Otra", city="Otra")

    with pytest.raises(ConflictError, match="TGZ"):
        await use_case.execute(office)

    repository.create.assert_not_awaited()