from pydantic import BaseModel, Field, field_validator
import re

PHONE_PATTERN = re.compile(r"^\+?[1-9]\d{7,14}$")  # formato E.164 aproximado

class BulkUserCreateItemSchema(BaseModel):
    phone: str = Field(max_length=20)

    @field_validator("phone")
    @classmethod
    def validate_phone_format(cls, value: str) -> str:
        if not PHONE_PATTERN.match(value):
            raise ValueError("phone must be in international format, e.g. +529611234567")
        return value


class BulkUserCreateSchema(BaseModel):
    users: list[BulkUserCreateItemSchema] = Field(min_length=1, max_length=100)


class CompleteProfileSchema(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    email: str | None = Field(default=None, max_length=150)
    job_title: str | None = Field(default=None, max_length=100)
    profile_photo_key: str | None = Field(default=None, max_length=500)


class UserUpdateSchema(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    is_active: bool | None = None