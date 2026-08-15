from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.domain.schemas.EventPhoto import EventPhotoRead


class EventType(str, Enum):
    FIBER_CUT = "FIBER_CUT"


class LocationMethod(str, Enum):
    GPS = "GPS"
    MAP = "MAP"


class EventStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"


class EventCreate(BaseModel):
    """Payload sent from the mobile app when reporting a fiber cut (section 14)."""

    origin_office_id: int
    destination_office_id: int

    latitude: float
    longitude: float
    location_method: LocationMethod
    accuracy: float | None = Field(
        default=None, description="Meters. Required if location_method is GPS."
    )

    field_reference: str | None = None
    description: str

    @model_validator(mode="after")
    def check_offices_differ(self):
        if self.origin_office_id == self.destination_office_id:
            raise ValueError("origin_office_id and destination_office_id must differ")
        return self

    @model_validator(mode="after")
    def check_accuracy_matches_method(self):
        if self.location_method == LocationMethod.GPS and self.accuracy is None:
            raise ValueError("accuracy is required when location_method is GPS")
        if self.location_method == LocationMethod.MAP and self.accuracy is not None:
            raise ValueError("accuracy must be omitted when location_method is MAP")
        return self


class EventUpdate(BaseModel):
    status: EventStatus | None = None
    description: str | None = None
    field_reference: str | None = None


class CentralOfficeSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    prefix: str
    name: str


class EventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: EventType

    origin_office: CentralOfficeSummary
    destination_office: CentralOfficeSummary

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

    photos: list[EventPhotoRead] = []

    created_at: datetime
    updated_at: datetime