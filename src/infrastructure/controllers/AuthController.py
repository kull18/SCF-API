from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.rate_limiter import limiter
from src.core.middlewares.role_middleware import get_current_user
from src.infrastructure.repositories.UserRepository import UserRepository
from src.application.usecases.LoginUseCase import LoginUseCase, InvalidCredentialsError
from src.application.usecases.ChangePasswordUseCase import ChangePasswordUseCase
from src.application.usecases.LogoutUseCase import LogoutUseCase
from src.infrastructure.repositories.RevokedTokenRepository import RevokedTokenRepository
from src.domain.schemas.AuthSchema import LoginSchema, ChangePasswordSchema
from src.application.dtos.responses.auth_response import LoginResponse
from src.application.mappers.user_mapper import UserMapper
from src.domain.models.User import User
from src.domain.schemas.DeviceToken import RegisterDeviceTokenSchema, DeviceLoginSchema
from src.application.dtos.responses.device_token_response import DeviceTokenResponse
from src.infrastructure.repositories.DeviceTokenRepository import DeviceTokenRepository
from src.application.usecases.RegisterDeviceTokenUseCase import RegisterDeviceTokenUseCase
from src.application.usecases.DeviceLoginUseCase import DeviceLoginUseCase
from src.services.device_token_service import DEVICE_TOKEN_EXPIRE_DAYS
from src.domain.schemas.AuthSchema import ForgotPasswordSchema
from src.application.usecases.ForgotPasswordUseCase import ForgotPasswordUseCase
from src.services.credential_sender_factory import get_credential_sender_context

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
@limiter.limit("10/minute")
async def login(
    request: Request,
    schema: LoginSchema,
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    use_case = LoginUseCase(repository)

    try:
        user, token = await use_case.execute(schema.technician_code, schema.password)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return LoginResponse(
        access_token=token,
        must_change_password=user.must_change_password,
        user=UserMapper.model_to_response(user),
    )


@router.post("/logout", status_code=204)
async def logout(
    request: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    jti = request.state.jti
    exp = request.state.token_exp

    if jti is None or exp is None:
        return

    repository = RevokedTokenRepository(session)
    use_case = LogoutUseCase(repository)
    await use_case.execute(jti, exp)


@router.post("/change-password", status_code=204)
async def change_password(
    schema: ChangePasswordSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = UserRepository(session)
    use_case = ChangePasswordUseCase(repository)
    await use_case.execute(current_user, schema.new_password)

@router.post("/register-device", response_model=DeviceTokenResponse, status_code=201)
async def register_device(
    schema: RegisterDeviceTokenSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = DeviceTokenRepository(session)
    use_case = RegisterDeviceTokenUseCase(repository)

    device_token = await use_case.execute(current_user, schema.device_label)

    return DeviceTokenResponse(
        device_token=device_token.token,
        expires_in_days=DEVICE_TOKEN_EXPIRE_DAYS,
    )


@router.post("/device-login", response_model=LoginResponse)
@limiter.limit("10/minute")
async def device_login(
    request: Request,
    schema: DeviceLoginSchema,
    session: AsyncSession = Depends(get_session),
):
    device_repository = DeviceTokenRepository(session)
    user_repository = UserRepository(session)
    use_case = DeviceLoginUseCase(device_repository, user_repository)

    try:
        user, token = await use_case.execute(schema.device_token)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))

    return LoginResponse(
        access_token=token,
        must_change_password=user.must_change_password,
        user=UserMapper.model_to_response(user),
    )

@router.delete("/device-token/{token_id}", status_code=204)
async def revoke_device_token(
    token_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    repository = DeviceTokenRepository(session)
    await repository.revoke(token_id)

@router.post("/forgot-password", status_code=200)
@limiter.limit("3/hour")
async def forgot_password(
    request: Request,
    schema: ForgotPasswordSchema,
    session: AsyncSession = Depends(get_session),
):
    repository = UserRepository(session)
    credential_sender_context = get_credential_sender_context()
    use_case = ForgotPasswordUseCase(repository, credential_sender_context)

    await use_case.execute(schema.technician_code)

    # Mensaje generico: nunca confirma si el technician_code existe o no.
    return {
        "detail": "Si el código es válido, se enviaron nuevas credenciales por WhatsApp."
    }