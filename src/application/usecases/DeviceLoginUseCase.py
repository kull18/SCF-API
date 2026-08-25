from datetime import datetime, timezone

from src.infrastructure.repositories.UserRepository import UserRepository
from src.infrastructure.repositories.DeviceTokenRepository import DeviceTokenRepository
from src.services.token_service import create_access_token
from src.domain.models.User import User
from src.core.exceptions import ForbiddenError
from src.application.usecases.LoginUseCase import InvalidCredentialsError


class DeviceLoginUseCase:
    def __init__(
        self,
        device_token_repository: DeviceTokenRepository,
        user_repository: UserRepository,
    ):
        self._device_token_repository = device_token_repository
        self._user_repository = user_repository

    async def execute(self, device_token_value: str) -> tuple[User, str]:
        device_token = await self._device_token_repository.get_by_token(device_token_value)

        if device_token is None or not device_token.is_active:
            raise InvalidCredentialsError("Invalid or revoked device token")

        if device_token.expires_at < datetime.now(timezone.utc):
            raise InvalidCredentialsError("Device token expired")

        user = await self._user_repository.get_by_id(device_token.user_id)
        if user is None or not user.is_active:
            raise ForbiddenError("This user account is inactive")

        device_token.last_used_at = datetime.now(timezone.utc)
        await self._device_token_repository.update(device_token)

        access_token = create_access_token(subject=user.technician_code, role=user.role.value)
        return user, access_token