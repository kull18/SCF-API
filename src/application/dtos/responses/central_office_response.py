from datetime import datetime

from pydantic import BaseModel


class CentralOfficeResponse(BaseModel):
    id: int
    prefix: str
    name: str
    city: str
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime