from src.domain.models.User import User
from src.infrastructure.repositories.UserRepository import UserRepository
from src.services.password_service import hash_password


class ChangePasswordUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, user: User, new_password: str) -> User:
        user.password_hash = hash_password(new_password)
        user.must_change_password = False
        return await self._repository.update(user)