from src.application.dtos.responses.user_response import UserResponse
from src.domain.models.User import User
from src.services.s3_service import generate_download_presigned_url


class UserMapper:
    @staticmethod
    def model_to_response(model: User) -> UserResponse:
        return UserResponse(
            id=model.id,
            technician_code=model.technician_code,
            full_name=model.full_name,
            phone=model.phone,
            email=model.email,
            role=model.role,
            job_title=model.job_title,
            profile_photo_url=(
                generate_download_presigned_url(model.profile_photo_key)
                if model.profile_photo_key
                else None
            ),
            is_active=model.is_active,
            profile_completed=model.profile_completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )