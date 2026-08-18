from src.domain.models.User import User
from src.infrastructure.repositories.UserRepository import UserRepository


class CompleteProfileUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, user: User, full_name: str, email: str | None) -> User:
        user.full_name = full_name
        user.email = email
        user.profile_completed = True
        return await self._repository.update(user)