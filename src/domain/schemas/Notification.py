from pydantic import BaseModel


class DeviceTokenSchema(BaseModel):
    player_id: str