from src.domain.models.User import User
from src.infrastructure.repositories.UserRepository import UserRepository
from src.services.technician_code_service import generate_technician_code

MAX_GENERATION_ATTEMPTS = 10


class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, user: User) -> User:
        user.technician_code = await self._generate_unique_technician_code()
        return await self._repository.create(user)

    async def _generate_unique_technician_code(self) -> str:
        for _ in range(MAX_GENERATION_ATTEMPTS):
            code = generate_technician_code()
            existing = await self._repository.get_by_technician_code(code)
            if existing is None:
                return code

        raise RuntimeError(
            "Could not generate a unique technician_code after "
            f"{MAX_GENERATION_ATTEMPTS} attempts"
        )