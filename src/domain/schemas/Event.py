from pydantic import BaseModel, Field, model_validator

from src.domain.models.Event import LocationMethod


class EventCreateSchema(BaseModel):
    origin_office_id: int
    destination_office_id: int
    latitude: float
    longitude: float
    location_method: LocationMethod
    accuracy: float | None = Field(default=None, description="Meters, required if GPS")
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


class EventUpdateSchema(BaseModel):
    status: str | None = None
    description: str | None = None
    field_reference: str | None = None