from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    full_name: str = Field(max_length=150)
    phone: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    role: str | None = Field(default=None, max_length=100)
    password: str = Field(min_length=8)


class UserUpdateSchema(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None