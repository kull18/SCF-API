from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    technician_code: str = Field(examples=["FT-8942"])
    password: str


class ChangePasswordSchema(BaseModel):
    new_password: str = Field(min_length=8, max_length=72)