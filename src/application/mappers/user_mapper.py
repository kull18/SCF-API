from src.domain.schemas.User import UserCreateSchema
from src.application.dtos.responses.user_response import UserResponse
from src.domain.models.User import User, UserRole
from src.services.password_service import hash_password


class UserMapper:
    @staticmethod
    def schema_to_model(schema: UserCreateSchema) -> User:
        return User(
            full_name=schema.full_name,
            phone=schema.phone,
            email=schema.email,
            role=UserRole.TECNICO,
            password_hash=hash_password(schema.password),
        )

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
            created_at=model.created_at,
            updated_at=model.updated_at,
        )