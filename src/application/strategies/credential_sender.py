from abc import ABC, abstractmethod


class CredentialSender(ABC):
    """La interfaz estrategia: declara la operacion comun a todas
    las versiones soportadas de envio de credenciales."""

    @abstractmethod
    async def send_credentials(
        self, phone: str, technician_code: str, temp_password: str
    ) -> bool:
        ...