from src.domain.models.Notification import Notification, NotificationType
from src.domain.models.Event import Event
from src.infrastructure.repositories.NotificationRepository import NotificationRepository
from src.infrastructure.repositories.UserRepository import UserRepository
from src.services.onesignal_service import send_push_notification


class NotifyEventCreatedUseCase:
    def __init__(
        self,
        notification_repository: NotificationRepository,
        user_repository: UserRepository,
    ):
        self._notification_repository = notification_repository
        self._user_repository = user_repository

    async def execute(self, event: Event) -> None:
        # TODO: definir a quiénes se notifica (ej. todos los técnicos activos,
        # o solo los de la central involucrada). Por ahora, ejemplo con todos.
        users = await self._user_repository.list()

        title = "Nuevo corte de fibra reportado"
        body = f"Tramo {event.origin_office_id} → {event.destination_office_id}"

        for user in users:
            notification = Notification(
                user_id=user.id,
                title=title,
                body=body,
                type=NotificationType.EVENT_CREATED,
                related_event_id=event.id,
            )
            await self._notification_repository.create(notification)
            await send_push_notification(user.technician_code, title, body)