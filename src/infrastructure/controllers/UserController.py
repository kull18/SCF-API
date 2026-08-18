from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import get_session
from src.core.middlewares.role_middleware import get_current_user
from src.core.middlewares.role_middleware import require_role
from src.domain.models.User import User, UserRole
from src.infrastructure.repositories.UserRepository import UserRepository
from src.application.usecases.BulkCreateUsersUseCase import BulkCreateUsersUseCase
from src.application.usecases.CompleteProfileUseCase import CompleteProfileUseCase
from src.domain.schemas.User import (
    BulkUserCreateSchema,
    CompleteProfileSchema,
    UserUpdateSchema,
)
from src.application.dtos.responses.user_response import (
    UserResponse,
    BulkUserCreatedResponse,
)
from src.services.s3_service import (
    build_profile_photo_key,
    generate_upload_presigned_url,
)
from src.application.mappers.user_mapper import UserMapper

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/bulk", response_model=list[BulkUserCreatedResponse], status_code=201)
async def bulk_create_users(
    schema: BulkUserCreateSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.ADMIN)),
):
    repository = UserRepository(session)
    use_case = BulkCreateUsersUseCase(repository)

    phones = [item.phone for item in schema.users]
    created = await use_case.execute(phones)

    return created


@router.get("", response_model=list[UserResponse])
async def list_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.ADMIN)),
):
    repository = UserRepository(session)
    users = await repository.list()
    return [UserMapper.model_to_response(u) for u in users]

@router.get("/me/profile-photo-upload-url")
async def get_profile_photo_upload_url(
    filename: str,
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    object_key = build_profile_photo_key(current_user.id, filename)
    upload_url = generate_upload_presigned_url(object_key)

    return {
        "upload_url": upload_url,
        "object_key": object_key,
    }


@router.patch("/me/complete-profile", response_model=UserResponse)
async def complete_profile(
    schema: CompleteProfileSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    _: str = Depends(require_role(UserRole.TECNICO)),
):
    repository = UserRepository(session)
    use_case = CompleteProfileUseCase(repository)

    updated = await use_case.execute(
        current_user,
        schema.full_name,
        schema.email,
        schema.job_title,
        schema.profile_photo_key,
    )
    return UserMapper.model_to_response(updated)