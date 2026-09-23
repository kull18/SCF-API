from src.infrastructure.repositories.RevokedTokenRepository import RevokedTokenRepository
from src.infrastructure.repositories.DeviceTokenRepository import DeviceTokenRepository


class PurgeExpiredTokensUseCase:
    def __init__(
        self,
        revoked_token_repository: RevokedTokenRepository,
        device_token_repository: DeviceTokenRepository,
    ):
        self._revoked_token_repository = revoked_token_repository
        self._device_token_repository = device_token_repository

    async def execute(self) -> dict:
        revoked_purged = await self._revoked_token_repository.purge_expired()
        device_purged = await self._device_token_repository.purge_expired_or_revoked()

        return {
            "revoked_tokens_purged": revoked_purged,
            "device_tokens_purged": device_purged,
        }