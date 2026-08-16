from datetime import datetime

from pydantic import BaseModel

from src.domain.models.User import UserRole


class UserResponse(BaseModel):
    id: int
    technician_code: str
    full_name: str
    phone: str | None
    email: str | None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime