import httpx

from src.core.config import settings
from src.application.strategies.credential_sender import CredentialSender


class WhatsAppCredentialSender(CredentialSender):
    """ConcreteStrategy: envia credenciales via Meta Cloud API."""

    WHATSAPP_API_URL = (
        f"https://graph.facebook.com/v21.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    )

    async def send_credentials(
        self, phone: str, technician_code: str, temp_password: str
    ) -> bool:
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "template",
            "template": {
                "name": settings.WHATSAPP_TEMPLATE_NAME,
                "language": {"code": settings.WHATSAPP_TEMPLATE_LANGUAGE},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": technician_code},
                            {"type": "text", "text": temp_password},
                        ],
                    }
                ],
            },
        }
        headers = {"Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(self.WHATSAPP_API_URL, json=payload, headers=headers)
                response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False