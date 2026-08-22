from src.domain.models.CentralOffice import CentralOffice
from src.infrastructure.repositories.CentralOfficeRepository import CentralOfficeRepository
from src.core.exceptions import ConflictError


class CreateCentralOfficeUseCase:
    def __init__(self, repository: CentralOfficeRepository):
        self._repository = repository

    async def execute(self, office: CentralOffice) -> CentralOffice:
        existing = await self._repository.get_by_prefix(office.prefix)
        if existing is not None:
            raise ConflictError(f"A central office with prefix '{office.prefix}' already exists")

        return await self._repository.create(office)