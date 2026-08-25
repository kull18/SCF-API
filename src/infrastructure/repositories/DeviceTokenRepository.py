from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.DeviceToken import DeviceToken


class DeviceTokenRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, device_token: DeviceToken) -> DeviceToken:
        self._session.add(device_token)
        await self._session.commit()
        await self._session.refresh(device_token)
        return device_token

    async def get_by_token(self, token: str) -> DeviceToken | None:
        result = await self._session.execute(
            select(DeviceToken).where(DeviceToken.token == token)
        )
        return result.scalar_one_or_none()

    async def update(self, device_token: DeviceToken) -> DeviceToken:
        await self._session.commit()
        await self._session.refresh(device_token)
        return device_token

    async def revoke(self, token_id: int) -> None:
        device_token = await self._session.get(DeviceToken, token_id)
        if device_token is not None:
            device_token.is_active = False
            await self._session.commit()