from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CentralOfficeBase(BaseModel):
    prefix: str = Field(max_length=4, examples=["TGZ"])
    name: str = Field(max_length=120, examples=["Central Tuxtla Gutiérrez"])
    city: str = Field(max_length=120, examples=["Tuxtla Gutiérrez"])
    latitude: float = Field(examples=[16.7528])
    longitude: float = Field(examples=[-93.1165])


class CentralOfficeCreate(CentralOfficeBase):
    pass


class CentralOfficeUpdate(BaseModel):
    prefix: str | None = Field(default=None, max_length=4)
    name: str | None = Field(default=None, max_length=120)
    city: str | None = Field(default=None, max_length=120)
    latitude: float | None = None
    longitude: float | None = None


class CentralOfficeRead(CentralOfficeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

from pydantic import BaseModel, ConfigDict, Field


class CentralOfficeBase(BaseModel):
    prefix: str = Field(max_length=4, examples=["TGZ"])
    name: str = Field(max_length=120, examples=["Central Tuxtla Gutiérrez"])
    city: str = Field(max_length=120, examples=["Tuxtla Gutiérrez"])
    latitude: float = Field(examples=[16.7528])
    longitude: float = Field(examples=[-93.1165])


class CentralOfficeCreate(CentralOfficeBase):
    pass


class CentralOfficeUpdate(BaseModel):
    prefix: str | None = Field(default=None, max_length=4)
    name: str | None = Field(default=None, max_length=120)
    city: str | None = Field(default=None, max_length=120)
    latitude: float | None = None
    longitude: float | None = None


class CentralOfficeRead(CentralOfficeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime