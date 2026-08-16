from datetime import datetime

from pydantic import BaseModel

from src.domain.models.Event import EventType, LocationMethod, EventStatus
from src.application.dtos.responses.event_photo_response import EventPhotoResponse


class CentralOfficeSummaryResponse(BaseModel):
    id: int
    prefix: str
    name: str


class EventResponse(BaseModel):
    id: int
    type: EventType
    origin_office_id: int
    destination_office_id: int
    latitude: float
    longitude: float
    location_method: LocationMethod
    accuracy: float | None
    distance_to_origin: float
    distance_to_destination: float
    field_reference: str | None
    description: str
    status: EventStatus
    reported_by_id: int
    reported_at: datetime
    photos: list[EventPhotoResponse] = []