from datetime import datetime, timezone

from src.infrastructure.repositories.RevokedTokenRepository import RevokedTokenRepository


class LogoutUseCase:
    def __init__(self, repository: RevokedTokenRepository):
        self._repository = repository

    async def execute(self, jti: str, exp_timestamp: int) -> None:
        expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        await self._repository.revoke(jti, expires_at)