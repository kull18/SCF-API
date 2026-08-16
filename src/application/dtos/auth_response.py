from pydantic import BaseModel

from src.application.dtos.responses.user_response import UserResponse


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse