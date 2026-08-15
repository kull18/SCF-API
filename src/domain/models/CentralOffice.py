from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.base import Base

class CentralOffice(Base):
    """Section 4 of the design document."""

    __tablename__ = "central_offices"

    id: Mapped[int] = mapped_column(primary_key=True)
    prefix: Mapped[str] = mapped_column(String(4), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)

    location: Mapped[str] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    events_as_origin = relationship(
        "Event",
        back_populates="origin_office",
        foreign_keys="Event.origin_office_id",
    )
    events_as_destination = relationship(
        "Event",
        back_populates="destination_office",
        foreign_keys="Event.destination_office_id",
    )