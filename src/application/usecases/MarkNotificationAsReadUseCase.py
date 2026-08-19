from src.domain.models.Notification import Notification
from src.infrastructure.repositories.NotificationRepository import NotificationRepository
from src.core.exceptions import NotFoundError


class MarkNotificationAsReadUseCase:
    def __init__(self, repository: NotificationRepository):
        self._repository = repository

    async def execute(self, notification_id: int) -> Notification:
        notification = await self._repository.get_by_id(notification_id)
        if notification is None:
            raise NotFoundError(f"Notification with id={notification_id} not found")

        notification.is_read = True
        return await self._repository.update(notification)