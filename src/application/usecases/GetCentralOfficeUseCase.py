from src.domain.models.CentralOffice import CentralOffice
from src.infrastructure.repositories.CentralOfficeRepository import CentralOfficeRepository


class GetCentralOfficeUseCase:
    def __init__(self, repository: CentralOfficeRepository):
        self._repository = repository

    async def execute(self, office_id: int) -> CentralOffice:
        office = await self._repository.get_by_id(office_id)
        if office is None:
            raise ValueError(f"CentralOffice with id={office_id} not found")
        return office