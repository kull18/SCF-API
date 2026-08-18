from src.domain.models.User import User
from src.infrastructure.repositories.UserRepository import UserRepository


class CompleteProfileUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(
        self,
        user: User,
        full_name: str,
        email: str | None,
        job_title: str | None,
        profile_photo_key: str | None,
    ) -> User:
        user.full_name = full_name
        user.email = email
        user.job_title = job_title
        if profile_photo_key is not None:
            user.profile_photo_key = profile_photo_key
        user.profile_completed = True
        return await self._repository.update(user)