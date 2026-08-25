from src.infrastructure.repositories.UserRepository import UserRepository
from src.services.password_service import hash_password
from src.services.temp_password_service import generate_temp_password
from src.application.strategies.credential_sender_context import CredentialSenderContext


class ForgotPasswordUseCase:
    def __init__(
        self,
        repository: UserRepository,
        credential_sender_context: CredentialSenderContext,
    ):
        self._repository = repository
        self._credential_sender_context = credential_sender_context

    async def execute(self, technician_code: str) -> None:
        user = await self._repository.get_by_technician_code(technician_code)

        # Respuesta identica exista o no el usuario (evita que alguien
        # confirme technician_codes validos por prueba y error).
        if user is None or not user.is_active:
            return

        temp_password = generate_temp_password()
        user.password_hash = hash_password(temp_password)
        user.must_change_password = True
        await self._repository.update(user)

        await self._credential_sender_context.send_credentials(
            phone=user.phone,
            technician_code=user.technician_code,
            temp_password=temp_password,
        )