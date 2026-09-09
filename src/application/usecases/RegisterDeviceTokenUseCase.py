from src.domain.models.DeviceToken import DeviceToken
from src.domain.models.User import User
from src.infrastructure.repositories.DeviceTokenRepository import DeviceTokenRepository
from src.services.device_token_service import generate_device_token, device_token_expiry


class RegisterDeviceTokenUseCase:
    def __init__(self, repository: DeviceTokenRepository):
        self._repository = repository

    async def execute(self, user: User, device_label: str | None) -> DeviceToken:
        device_token = DeviceToken(
            user_id=user.id,
            token=generate_device_token(),
            device_label=device_label,
            is_active=True,
            expires_at=device_token_expiry(),
        )
        return await self._repository.create(device_token)