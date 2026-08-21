from src.application.strategies.credential_sender import CredentialSender


class CredentialSenderContext:
    """El contexto mantiene una referencia a una estrategia concreta,
    pero solo la conoce a traves de la interfaz CredentialSender.
    No sabe (ni le importa) si por debajo hay WhatsApp via Meta,
    Twilio, o cualquier otro canal futuro."""

    def __init__(self, strategy: CredentialSender):
        self._strategy = strategy

    def set_strategy(self, strategy: CredentialSender) -> None:
        """Permite cambiar la estrategia en tiempo de ejecucion."""
        self._strategy = strategy

    async def send_credentials(
        self, phone: str, technician_code: str, temp_password: str
    ) -> bool:
        """Delega el trabajo real a la estrategia actual."""
        return await self._strategy.send_credentials(phone, technician_code, temp_password)