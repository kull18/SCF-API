from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.infrastructure.repositories.UserRepository import UserRepository
from src.application.usecases.CreateUserUseCase import CreateUserUseCase
from src.application.usecases.UpdateUserUseCase import UpdateUserUseCase
from src.domain.schemas.User import UserCreateSchema, UserUpdateSchema
from src.application.dtos.responses.user_response import UserResponse
from src.application.mappers.user_mapper import UserMapper

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(schema: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    use_case = CreateUserUseCase(repository)

    try:
        model = UserMapper.schema_to_model(schema)
        created = await use_case.execute(model)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return UserMapper.model_to_response(created)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, schema: UserUpdateSchema, session: AsyncSession = Depends(get_session)
):
    repository = UserRepository(session)
    use_case = UpdateUserUseCase(repository)

    try:
        updated = await use_case.execute(user_id, schema)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return UserMapper.model_to_response(updated)