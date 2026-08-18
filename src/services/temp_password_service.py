import secrets
import string


def generate_temp_password(length: int = 8) -> str:
    """Genera una contraseña temporal legible (sin caracteres ambiguos como 0/O, 1/l)."""
    alphabet = "".join(c for c in string.ascii_letters + string.digits if c not in "0O1lI")
    return "".join(secrets.choice(alphabet) for _ in range(length))