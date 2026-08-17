import enum
from datetime import datetime

from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, Enum as SAEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.base import Base


class NotificationType(str, enum.Enum):
    EVENT_CREATED = "EVENT_CREATED"
    EVENT_COMMENT = "EVENT_COMMENT"
    EVENT_STATUS_CHANGED = "EVENT_STATUS_CHANGED"


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[NotificationType] = mapped_column(
        SAEnum(NotificationType, name="notification_type"), nullable=False
    )
    related_event_id: Mapped[int | None] = mapped_column(
        ForeignKey("events.id", ondelete="SET NULL"), nullable=True
    )
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user = relationship("User")