from src.infrastructure.repositories.CentralOfficeRepository import CentralOfficeRepository


class DeleteCentralOfficeUseCase:
    def __init__(self, repository: CentralOfficeRepository):
        self._repository = repository

    async def execute(self, office_id: int) -> None:
        await self._repository.delete(office_id)