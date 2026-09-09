# Arquitectura

SCF sigue **Onion Architecture**, organizada en tres capas concéntricas más dos módulos transversales.

## Diagrama de arquitectura

![Diagrama de arquitectura](diagrams/arquitectura.jpg)

## Capas

### `domain/`
La capa más interna. No depende de ninguna otra capa del proyecto.

- **`models/`**: entidades SQLAlchemy (persistencia). Definen la estructura real de las tablas.
- **`schemas/`**: contratos de entrada (Pydantic). Validan lo que la API recibe antes de que llegue a cualquier lógica de negocio.

### `application/`
Depende únicamente de `domain/`.

- **`usecases/`**: orquestación y reglas de negocio. Cada caso de uso es una clase con un único método `execute()`. Aquí viven las validaciones que no son de formato (ej. "el prefijo de una central debe ser único"), a diferencia de las validaciones de formato, que viven en los `schemas`.
- **`dtos/`**: contratos de salida (Pydantic). Definen exactamente qué campos se exponen al cliente — nunca se devuelve un `model` de SQLAlchemy directamente.
- **`mappers/`**: la única capa que traduce entre `Schema → Model` (al recibir) y `Model → DTO` (al responder). Ningún otro lugar del código hace esta conversión. Cuando un objeto de respuesta requiere datos de relaciones (por ejemplo, un evento necesita los datos de sus centrales de origen/destino y del técnico que lo reportó), el `Mapper` recibe esos objetos ya resueltos como parámetros adicionales — nunca los busca por su cuenta.

### `infrastructure/`
La capa más externa. Depende de `application/` y `domain/`.

- **`controllers/`**: endpoints FastAPI. Su única responsabilidad es parsear el request, instanciar el `Repository` y el `UseCase` correspondiente, y devolver la respuesta mapeada. No contienen lógica de negocio ni manejo de errores explícito (ver `authentication.md` y la sección de manejo de errores más abajo).
- **`repositories/`**: acceso a datos vía SQLAlchemy. Reciben y devuelven directamente el `Model` — no hay una capa de interfaces/ABC para repositorios en este proyecto (ver [ADR 002](decisions/002-clean-architecture.md)). No contienen reglas de negocio: si un registro no existe, el `Repository` regresa `None`; es el `UseCase` quien decide que eso es un `NotFoundError`. Las relaciones que un `Mapper` necesita (centrales, autor de un evento, autor de un comentario) se cargan explícitamente con `selectinload` en las queries del `Repository`, para evitar N+1 queries.

## Módulos transversales

### `core/`
Configuración e infraestructura compartida por toda la aplicación:
- `config.py`: variables de entorno (Pydantic Settings).
- `session.py` / `init_db.py`: conexión a base de datos y creación automática de tablas al arrancar.
- `middlewares/`: `auth_middleware.py` (JWT), `role_middleware.py` (autorización por rol).
- `exceptions.py` / `exception_handlers.py`: jerarquía de excepciones de negocio y su mapeo centralizado a códigos HTTP.
- `rate_limiter.py`: configuración de `slowapi`.
- `scheduler.py`: configuración de `APScheduler`, corriendo dentro del mismo proceso de FastAPI (vía `lifespan`) para tareas periódicas como el cierre automático de eventos atendidos.

### `services/`
Utilidades técnicas reutilizables entre capas, sin estado de negocio: hashing de contraseñas, JWT, generación de códigos de técnico y contraseñas temporales, cálculo geográfico, S3 (incluyendo direccionamiento por hash de contenido), WhatsApp (Meta directo y Twilio como estrategias intercambiables), OneSignal.

## Implementación del patrón DTO

![Diagrama de implementación DTO](diagrams/DTO_impl.jpg)

El request entra como `Schema` (validación de formato), el `Mapper` lo convierte a `Model` para que el `UseCase` opere sobre él, y al responder el mismo `Mapper` convierte el `Model` resultante a `DTO` — así el cliente nunca recibe la fila completa de la base de datos, solo los campos que el `DTO` define explícitamente.

## Patrón Strategy (envío de credenciales)

El envío de credenciales por WhatsApp está implementado con el patrón Strategy clásico (GoF), usando `ABC` en vez de `typing.Protocol` — decisión deliberada para tener verificación en tiempo de ejecución de que cada implementación concreta cumple el contrato:

- **Interfaz** (`CredentialSender`, ABC): declara `send_credentials(...)`.
- **Estrategias concretas**: `WhatsAppCredentialSender` (Meta Cloud API) y `TwilioWhatsAppCredentialSender` (Twilio como BSP alternativo).
- **Context** (`CredentialSenderContext`): mantiene la referencia a la estrategia activa y delega el trabajo — el `UseCase` que lo consume nunca conoce la implementación concreta.
- **Cliente**: `credential_sender_factory.py`, que lee `CREDENTIAL_SENDER_PROVIDER` del entorno y arma el `Context` con la estrategia correspondiente.

Cambiar de proveedor es una sola variable de entorno, sin tocar ningún `UseCase`.

## Manejo de errores

- `core/exceptions.py` define `AppError` y sus subclases (`NotFoundError`, `ConflictError`, `ForbiddenError`, `ValidationError`).
- `core/exception_handlers.py` mapea cada excepción a su código HTTP correspondiente, registrado globalmente en `main.py`.
- `ErrorHandlingMiddleware` captura cualquier excepción no prevista (fuera del ciclo normal de FastAPI) y responde `500` sin exponer detalles internos al cliente, mientras registra el traceback en logs.
- Excepción deliberada: `InvalidCredentialsError` (login) no hereda de `AppError` porque un 401 de credenciales inválidas es semánticamente distinto de los errores de negocio genéricos. De igual forma, restricciones de propiedad (por ejemplo, que solo el autor de un evento pueda cambiar su estado, o solo el autor de un comentario pueda eliminarlo) se expresan como `ForbiddenError`, resultando en un `403` consistente en toda la API.