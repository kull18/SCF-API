from pydantic import BaseModel, Field


class LoginSchema(BaseModel):
    technician_code: str = Field(examples=["FT-8942"])
    password: str