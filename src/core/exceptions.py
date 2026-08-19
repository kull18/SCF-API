class AppError(Exception):
    """Base para todas las excepciones de negocio de la aplicacion."""


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class ForbiddenError(AppError):
    pass


class ValidationError(AppError):
    """Para reglas de negocio invalidas que no son de formato (esas las cubre Pydantic)."""
    pass