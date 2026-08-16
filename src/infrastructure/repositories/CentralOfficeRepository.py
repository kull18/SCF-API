from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.CentralOffice import CentralOffice


class CentralOfficeRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, office: CentralOffice) -> CentralOffice:
        self._session.add(office)
        await self._session.commit()
        await self._session.refresh(office)
        return office

    async def get_by_id(self, office_id: int) -> CentralOffice | None:
        return await self._session.get(CentralOffice, office_id)

    async def get_by_prefix(self, prefix: str) -> CentralOffice | None:
        result = await self._session.execute(
            select(CentralOffice).where(CentralOffice.prefix == prefix)
        )
        return result.scalar_one_or_none()

    async def list(self) -> list[CentralOffice]:
        result = await self._session.execute(
            select(CentralOffice).order_by(CentralOffice.prefix)
        )
        return list(result.scalars().all())

    async def update(self, office: CentralOffice) -> CentralOffice:
        # office ya es una instancia trackeada por la sesión (obtenida vía
        # get_by_id en el UseCase antes de modificar sus campos)
        await self._session.commit()
        await self._session.refresh(office)
        return office

    async def delete(self, office_id: int) -> None:
        office = await self._session.get(CentralOffice, office_id)
        if office is None:
            raise ValueError(f"CentralOffice with id={office_id} not found")
        await self._session.delete(office)
        await self._session.commit()