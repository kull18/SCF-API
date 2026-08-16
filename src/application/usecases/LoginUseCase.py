from src.infrastructure.repositories.UserRepository import UserRepository
from src.services.password_service import verify_password
from src.services.token_service import create_access_token
from src.domain.models.User import User


class InvalidCredentialsError(Exception):
    pass


class InactiveUserError(Exception):
    pass


class LoginUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, technician_code: str, password: str) -> tuple[User, str]:
        user = await self._repository.get_by_technician_code(technician_code)

        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid technician_code or password")

        if not user.is_active:
            raise InactiveUserError("This user account is inactive")

        token = create_access_token(subject=user.technician_code)
        return user, token