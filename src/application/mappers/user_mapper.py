from src.domain.schemas.User import CompleteProfileSchema
from src.application.dtos.responses.user_response import UserResponse
from src.domain.models.User import User


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
            is_active=model.is_active,
            profile_completed=model.profile_completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )