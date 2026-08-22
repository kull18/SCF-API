from src.domain.models.CentralOffice import CentralOffice
from src.infrastructure.repositories.CentralOfficeRepository import CentralOfficeRepository
from src.core.exceptions import NotFoundError


class DeleteCentralOfficeUseCase:
    def __init__(self, repository: CentralOfficeRepository):
        self._repository = repository

    async def execute(self, office_id: int) -> None:
        office = await self._repository.get_by_id(office_id)
        if office is None:
            raise NotFoundError(f"CentralOffice with id={office_id} not found")
        await self._repository.delete(office_id)