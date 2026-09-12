from src.domain.models.User import User
from src.infrastructure.repositories.UserRepository import UserRepository
from src.infrastructure.repositories.DeviceTokenRepository import DeviceTokenRepository
from src.core.exceptions import NotFoundError, ValidationError

ANONYMIZED_NAME = "Técnico dado de baja"


class AnonymizeUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        device_token_repository: DeviceTokenRepository,
    ):
        self._user_repository = user_repository
        self._device_token_repository = device_token_repository

    async def execute(self, user_id: int, confirm: bool) -> None:
        if not confirm:
            raise ValidationError("Debes confirmar la eliminación de la cuenta (confirm=true)")

        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User with id={user_id} not found")

        # Datos personales identificables -- se eliminan
        user.full_name = ANONYMIZED_NAME
        user.email = None
        user.phone = f"ANONYMIZED-{user.id}"
        user.job_title = None
        user.profile_photo_key = None

        # La cuenta queda inutilizable, pero el registro (eventos, comentarios
        # ya creados) se conserva intacto, referenciando a este user_id.
        user.is_active = False

        await self._user_repository.update(user)

        # Revoca todos los device tokens de biometria asociados
        await self._device_token_repository.revoke_all_for_user(user_id)