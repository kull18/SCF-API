from pydantic import BaseModel


class DeviceTokenResponse(BaseModel):
    device_token: str
    expires_in_days: int