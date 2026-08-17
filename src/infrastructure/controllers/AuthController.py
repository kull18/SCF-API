from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.infrastructure.repositories.UserRepository import UserRepository
from src.application.usecases.LoginUseCase import (
    LoginUseCase,
    InvalidCredentialsError,
    InactiveUserError,
)
from src.domain.schemas.AuthSchema import LoginSchema
from src.application.dtos.responses.auth_response import LoginResponse
from src.application.mappers.user_mapper import UserMapper

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
        user=UserMapper.model_to_response(user),
    )