from pydantic import BaseModel, Field


class RegisterDeviceTokenSchema(BaseModel):
    device_label: str | None = Field(default=None, max_length=100)


class DeviceLoginSchema(BaseModel):
    device_token: str