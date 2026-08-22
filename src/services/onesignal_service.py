import httpx

from src.core.config import settings

ONESIGNAL_API_URL = "https://onesignal.com/api/v1/notifications"


async def send_push_notification(
    external_user_id: str, title: str, body: str
) -> None:
    payload = {
        "app_id": settings.ONESIGNAL_APP_ID,
        "include_aliases": {"external_id": [external_user_id]},
        "target_channel": "push",
        "headings": {"en": title},
        "contents": {"en": body},
    }
    headers = {
        "Authorization": f"Basic {settings.ONESIGNAL_REST_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(ONESIGNAL_API_URL, json=payload, headers=headers)
        response.raise_for_status()