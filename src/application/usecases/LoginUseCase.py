from src.infrastructure.repositories.UserRepository import UserRepository
from src.services.password_service import verify_password
from src.services.token_service import create_access_token
from src.domain.models.User import User
from src.core.exceptions import ForbiddenError


class InvalidCredentialsError(Exception):
    """Se mantiene separada de AppError a proposito: no queremos que un 401
    de login se confunda con errores 403/404/409 genericos de negocio."""
    pass


class LoginUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, technician_code: str, password: str) -> tuple[User, str]:
        user = await self._repository.get_by_technician_code(technician_code)

        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid technician_code or password")

        if not user.is_active:
            raise ForbiddenError("This user account is inactive")

        token = create_access_token(subject=user.technician_code, role=user.role.value)
        return user, token