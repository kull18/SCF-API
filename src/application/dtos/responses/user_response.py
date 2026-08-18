from datetime import datetime

from pydantic import BaseModel

from src.domain.models.User import UserRole


class UserResponse(BaseModel):
    id: int
    technician_code: str
    full_name: str | None
    phone: str
    email: str | None
    role: UserRole
    is_active: bool
    profile_completed: bool
    created_at: datetime
    updated_at: datetime


class BulkUserCreatedResponse(BaseModel):
    id: int
    technician_code: str
    phone: str
    temp_password: str
    whatsapp_sent: bool