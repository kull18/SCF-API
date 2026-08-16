from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    technician_code: str
    full_name: str
    phone: str | None
    email: str | None
    role: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime