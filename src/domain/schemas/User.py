from pydantic import BaseModel, Field


class BulkUserCreateItemSchema(BaseModel):
    phone: str = Field(max_length=20, description="Numero para WhatsApp/SMS, ej. +529611234567")


class BulkUserCreateSchema(BaseModel):
    users: list[BulkUserCreateItemSchema] = Field(min_length=1, max_length=100)


class CompleteProfileSchema(BaseModel):
    full_name: str = Field(max_length=150)
    email: str | None = None


class UserUpdateSchema(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    is_active: bool | None = None