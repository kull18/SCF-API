from twilio.rest import Client

from src.core.config import settings
from src.application.strategies.credential_sender import CredentialSender


class TwilioWhatsAppCredentialSender(CredentialSender):
    """ConcreteStrategy: envia credenciales via Twilio (BSP)."""

    def __init__(self):
        self._client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    async def send_credentials(
        self, phone: str, technician_code: str, temp_password: str
    ) -> bool:
        try:
            self._client.messages.create(
                from_=settings.TWILIO_WHATSAPP_FROM,
                to=f"whatsapp:{phone}",
                content_sid=settings.TWILIO_CONTENT_SID,
                content_variables=f'{{"1":"{technician_code}","2":"{temp_password}"}}',
            )
            return True
        except Exception:
            return False