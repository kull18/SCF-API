from datetime import datetime

from pydantic import BaseModel

from src.domain.models.Event import EventType, LocationMethod, EventStatus
from src.application.dtos.responses.event_photo_response import EventPhotoResponse


class CentralOfficeSummaryResponse(BaseModel):
    id: int
    prefix: str
    name: str
    city: str


class ReportedByResponse(BaseModel):
    id: int
    technician_code: str
    full_name: str | None


class EventResponse(BaseModel):
    id: int
    type: EventType
    origin_office: CentralOfficeSummaryResponse
    destination_office: CentralOfficeSummaryResponse
    latitude: float
    longitude: float
    location_method: LocationMethod
    accuracy: float | None
    distance_to_origin: float
    distance_to_destination: float
    field_reference: str | None
    description: str
    status: EventStatus
    reported_by: ReportedByResponse
    reported_at: datetime
    photos: list[EventPhotoResponse] = []