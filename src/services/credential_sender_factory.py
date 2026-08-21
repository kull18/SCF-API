from src.core.config import settings
from src.application.strategies.credential_sender_context import CredentialSenderContext
from src.services.whatsapp_service import WhatsAppCredentialSender
from src.services.twilio_whatsapp_service import TwilioWhatsAppCredentialSender


def get_credential_sender_context() -> CredentialSenderContext:
    """El cliente: lee la configuracion, elige la estrategia concreta,
    y la inyecta en un Context listo para usar."""
    if settings.credential_sender_provider == "twilio":
        strategy = TwilioWhatsAppCredentialSender()
    else:
        strategy = WhatsAppCredentialSender()

    return CredentialSenderContext(strategy)