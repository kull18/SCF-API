from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.infrastructure.repositories.UserRepository import UserRepository
from src.application.usecases.LoginUseCase import (
    LoginUseCase,
    InvalidCredentialsError,
    InactiveUserError,
)
from src.application.usecases.ChangePasswordUseCase import ChangePasswordUseCase
from src.domain.schemas.AuthSchema import LoginSchema, ChangePasswordSchema
from src.application.dtos.responses.auth_response import LoginResponse
from src.application.mappers.user_mapper import UserMapper
from src.domain.models.User import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(schema: LoginSchema, session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    use_case = LoginUseCase(repository)

    try:
        user, token = await use_case.execute(schema.technician_code, schema.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except InactiveUserError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return LoginResponse(
        access_token=token,
        must_change_password=user.must_change_password,
        user=UserMapper.model_to_response(user),
    )


@router.post("/change-password", status_code=204)
async def change_password(
    schema: ChangePasswordSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = UserRepository(session)
    use_case = ChangePasswordUseCase(repository)
    await use_case.execute(current_user, schema.new_password)