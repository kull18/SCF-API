from pydantic import BaseModel, Field


class CentralOfficeCreateSchema(BaseModel):
    prefix: str = Field(max_length=4, examples=["TGZ"])
    name: str = Field(max_length=120, examples=["Central Tuxtla Gutiérrez"])
    city: str = Field(max_length=120, examples=["Tuxtla Gutiérrez"])
    latitude: float
    longitude: float


class CentralOfficeUpdateSchema(BaseModel):
    prefix: str | None = Field(default=None, max_length=4)
    name: str | None = Field(default=None, max_length=120)
    city: str | None = Field(default=None, max_length=120)
    latitude: float | None = None
    longitude: float | None = None