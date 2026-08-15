import enum
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import (
    Text,
    Numeric,
    ForeignKey,
    DateTime,
    Enum as SAEnum,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base

class EventType(str, enum.Enum):
    FIBER_CUT = "FIBER_CUT"


class LocationMethod(str, enum.Enum):
    GPS = "GPS"
    MAP = "MAP"


class EventStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"


class Event(Base):
    """Sections 13 and 14 of the design document."""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    type: Mapped[EventType] = mapped_column(
        SAEnum(EventType, name="event_type"),
        default=EventType.FIBER_CUT,
        nullable=False,
    )

    origin_office_id: Mapped[int] = mapped_column(
        ForeignKey("central_offices.id"), nullable=False
    )
    destination_office_id: Mapped[int] = mapped_column(
        ForeignKey("central_offices.id"), nullable=False
    )

    location: Mapped[str] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=False
    )
    location_method: Mapped[LocationMethod] = mapped_column(
        SAEnum(LocationMethod, name="location_method"),
        nullable=False,
    )
    accuracy: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)

    distance_to_origin: Mapped[float] = mapped_column(Numeric(8, 3), nullable=False)
    distance_to_destination: Mapped[float] = mapped_column(Numeric(8, 3), nullable=False)

    field_reference: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[EventStatus] = mapped_column(
        SAEnum(EventStatus, name="event_status"),
        default=EventStatus.ACTIVE,
        nullable=False,
    )

    reported_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    origin_office = relationship(
        "CentralOffice",
        back_populates="events_as_origin",
        foreign_keys=[origin_office_id],
    )
    destination_office = relationship(
        "CentralOffice",
        back_populates="events_as_destination",
        foreign_keys=[destination_office_id],
    )
    reported_by = relationship("User", back_populates="events")
    photos = relationship(
        "EventPhoto", back_populates="event", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "origin_office_id <> destination_office_id",
            name="chk_different_offices",
        ),
        CheckConstraint(
            "(location_method = 'GPS' AND accuracy IS NOT NULL) OR "
            "(location_method = 'MAP' AND accuracy IS NULL)",
            name="chk_accuracy_only_for_gps",
        ),
    )