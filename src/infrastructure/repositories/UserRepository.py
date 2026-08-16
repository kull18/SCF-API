from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.User import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def get_by_technician_code(self, technician_code: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.technician_code == technician_code)
        )
        return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        await self._session.commit()
        await self._session.refresh(user)
        return user