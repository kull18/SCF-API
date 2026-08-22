from src.domain.models.CentralOffice import CentralOffice
from src.infrastructure.repositories.CentralOfficeRepository import CentralOfficeRepository


class ListCentralOfficesUseCase:
    def __init__(self, repository: CentralOfficeRepository):
        self._repository = repository

    async def execute(self) -> list[CentralOffice]:
        return await self._repository.list()