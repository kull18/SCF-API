from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.RevokedToken import RevokedToken


class RevokedTokenRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def revoke(self, jti: str, expires_at: datetime) -> None:
        entry = RevokedToken(jti=jti, expires_at=expires_at)
        self._session.add(entry)
        await self._session.commit()

    async def is_revoked(self, jti: str) -> bool:
        result = await self._session.execute(
            select(RevokedToken.id).where(RevokedToken.jti == jti)
        )
        return result.scalar_one_or_none() is not None

    async def purge_expired(self) -> None:
        """Limpieza opcional de tokens ya vencidos, se puede correr periodicamente."""
        from sqlalchemy import delete
        await self._session.execute(
            delete(RevokedToken).where(RevokedToken.expires_at < datetime.now(timezone.utc))
        )
        await self._session.commit()