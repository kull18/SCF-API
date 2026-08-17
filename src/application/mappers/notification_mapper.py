from src.application.dtos.responses.notification_response import NotificationResponse
from src.domain.models.Notification import Notification


class NotificationMapper:
    @staticmethod
    def model_to_response(model: Notification) -> NotificationResponse:
        return NotificationResponse(
            id=model.id,
            title=model.title,
            body=model.body,
            type=model.type,
            related_event_id=model.related_event_id,
            is_read=model.is_read,
            created_at=model.created_at,
        )