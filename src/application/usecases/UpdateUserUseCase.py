from src.domain.schemas.User import UserUpdateSchema
from src.domain.models.User import User
from src.infrastructure.repositories.UserRepository import UserRepository
from src.core.exceptions import NotFoundError


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def execute(self, user_id: int, schema: UserUpdateSchema) -> User:
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User with id={user_id} not found")

        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        return await self._repository.update(user)