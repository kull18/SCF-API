# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Unreleased]

### Added
- Documentación dividida en `docs/` (`architecture.md`, `api.md`, `database.md`, `authentication.md`, `deployment.md`, `development.md`) y `docs/decisions/` con ADRs (001: uso de PostgreSQL+PostGIS, 002: elección de Onion Architecture). El README pasa a ser un punto de entrada que enlaza a cada documento.
- Diagramas de arquitectura, DTO y entidad-relación de base de datos importados en la documentación correspondiente.
- Manejo de errores centralizado: jerarquía de excepciones de negocio (`AppError`, `NotFoundError`, `ConflictError`, `ForbiddenError`, `ValidationError`) en `core/exceptions.py`, con handlers registrados globalmente (`core/exception_handlers.py`) que eliminan el `try/except HTTPException` repetido en cada controller.
- `ErrorHandlingMiddleware` como red de seguridad para excepciones no previstas (500), con logging del traceback sin exponer detalles al cliente.
- Revocación de JWT vía blacklist (`revoked_tokens`): cada token incluye un `jti` único; `POST /auth/logout` lo invalida antes de su expiración natural. Verificado en `auth_middleware` en cada request autenticado.
- Rate limiting en endpoints sensibles con `slowapi`: `POST /auth/login` (10/minuto por IP) y `POST /users/bulk` (3/hora).
- Límite de tamaño de request (`BodySizeLimitMiddleware`, 2 MB).
- CORS configurado explícitamente (`CORSMiddleware`), con `allowed_origins` vacío por defecto dado que no hay cliente web todavía.
- Validación de rangos geográficos (`latitude`, `longitude`, `accuracy`) y `max_length` en campos de texto libre de los schemas de entrada (`Event`, `EventComment`, `User`).
- Validación de formato de número telefónico (E.164 aproximado) en el alta masiva de usuarios.
- `Dockerfile` multi-stage (build liviano sin herramientas de compilación en la imagen final, usuario no-root) y `docker-compose.yml` con PostGIS preinstalado para desarrollo local.
- `requirements.txt` con versiones fijas del entorno real del proyecto.
- Script de seed (`scripts/seed_admin.py`) para crear el primer usuario `ADMIN`, necesario para poder usar `POST /users/bulk` por primera vez.
- Almacenamiento de archivos en S3 direccionado por contenido: el nombre del objeto es el hash SHA-256 del archivo (calculado en el cliente), con deduplicación automática por evento/usuario y verificación de existencia previa (`object_exists`) antes de generar una URL de subida.
- Foto de perfil de usuario (`profile_photo_key`), con el mismo flujo de URLs prefirmadas usado para fotos de eventos.
- Puesto de trabajo (`job_title`) como campo opcional del perfil de usuario.
- Filtro de técnicos activos en `UserRepository.list_active()`, usado por `NotifyEventCreatedUseCase` para no notificar a usuarios inactivos.
- Conexión real de `NotifyEventCreatedUseCase` dentro de `CreateEventUseCase`: cada evento creado dispara notificación in-app y push automáticamente.
- Notificaciones push vía OneSignal, disparadas al crear un evento.
- Historial de notificaciones in-app con contador de no leídas (`GET /notifications`, `GET /notifications/unread-count`).
- Registro de dispositivo para push (`POST /notifications/device-token`).
- Feature de comentarios en eventos (`EventComment`): crear, listar por evento y eliminar (solo el autor).
- Envío automático de credenciales de acceso por WhatsApp Business API tras el alta masiva de técnicos.
- Alta masiva de usuarios por administrador (`POST /users/bulk`): solo requiere teléfono, genera `technician_code` y contraseña temporal automáticamente.
- Flujo de completar perfil tras el primer login (`PATCH /users/me/complete-profile`).
- Cambio de contraseña obligatorio en el primer inicio de sesión (`must_change_password`, `POST /auth/change-password`).
- Rol `ADMIN`, además del rol `TECNICO` existente.

### Changed
- Todos los `UseCase` migrados de `raise ValueError` / `raise PermissionError` a las excepciones tipadas (`NotFoundError`, `ConflictError`, `ForbiddenError`), eliminando la responsabilidad de mapeo a código HTTP de los controllers.
- Las validaciones de existencia (ej. antes de eliminar) se movieron de los `Repository` a los `UseCase` correspondientes; los repositorios quedan sin lógica de negocio, solo acceso a datos.
- `MarkNotificationAsReadUseCase` creado para mover la lógica de "marcar como leída" del controller (que llamaba directo al repository) a la capa de aplicación, corrigiendo además un bug de condición invertida (`if notification is not None: raise ...`) que existía en esa validación.
- El autor de un evento ya no se autonotifica de su propio reporte (`NotifyEventCreatedUseCase` excluye `reported_by_id`).
- `domain/schemas/User.py`: se retira la creación individual de usuarios (`UserCreateSchema`) en favor del alta masiva (`BulkUserCreateSchema`).
- `full_name`, `email`, `job_title` y `profile_photo_key` en el modelo `User` son opcionales (`nullable=True`); se completan después del primer login, no en el alta.
- `application/mappers/user_mapper.py`: se retira `schema_to_model`, ya que la creación de usuarios ahora vive en `BulkCreateUsersUseCase`.

### Fixed
- Bug de import en `NotificationController` y `EventPhotoController`: `get_current_user` se importaba erróneamente desde `core.middlewares.role_middleware` en vez de `core.middlewares.auth_middleware`.
- `EventPhotoController` seguía usando `build_event_photo_key` (sin deduplicación por hash) en vez de `build_content_addressed_key`; actualizado para incluir `content_hash` en el endpoint de upload-url.
- Error `password cannot be longer than 72 bytes` al hashear contraseñas: se reemplazó `passlib` por `bcrypt` directo, con truncado explícito a 72 bytes antes de hashear.
- `Psycopg cannot use the 'ProactorEventLoop'` en Windows: se migró el driver de base de datos de `psycopg` (async) a `asyncpg`.
- `PydanticUserError` por atributo sin anotación de tipo en `Settings`: se corrigió `database_url` con tipo explícito y `SettingsConfigDict`.
- `ValidationError: extra_forbidden` en `Settings` por variables del `.env` (AWS, WhatsApp, OneSignal, `DB_PASSWORD` de Docker Compose) no declaradas en la clase de configuración.
- Warning de uvicorn sobre `reload`/`workers` sin string de import: se corrigió `uvicorn.run()` para usar `"main:app"` en vez del objeto `app` directo.

### Removed
- Dependencias muertas del entorno de desarrollo: `psycopg` / `psycopg-binary` (reemplazadas por `asyncpg`) y `passlib` (reemplazado por `bcrypt` directo).
- `CreateUserUseCase.py`, reemplazado por completo por `BulkCreateUsersUseCase` (ya no hay alta individual de usuarios).

### Security
- Se detectaron credenciales expuestas en texto plano durante el desarrollo (AWS Secret Access Key, OneSignal REST API Key); se recomienda rotación inmediata desde IAM y el dashboard de OneSignal respectivamente.

### Known limitations / Pending
- `revoked_tokens` no tiene limpieza automática de registros expirados (`RevokedTokenRepository.purge_expired()` existe pero no está conectado a ningún scheduler). Bajo prioridad mientras el volumen de usuarios sea pequeño.
- La blacklist de JWT revoca por token individual (`jti`), no por usuario — un admin no puede forzar el cierre de sesión de un técnico sin conocer su token actual; la mitigación disponible hoy es desactivar la cuenta (`is_active = false`).
- Sin migraciones formales (Alembic): cambios de esquema en tablas existentes requieren recreación manual en desarrollo.
- Sin tests (unitarios ni de integración) en ningún punto del proyecto.

## [0.2.0]

### Added
- Autenticación JWT (`POST /auth/login`) con `technician_code` + contraseña.
- `auth_middleware` y `role_middleware` para proteger rutas por autenticación y rol.
- Hashing de contraseñas con `bcrypt`.
- Generación automática de `technician_code` (`services/technician_code_service.py`).
- CRUD completo de centrales de red (`CentralOffice`).
- Reporte y consulta de eventos de corte de fibra (`Event`), con cálculo automático de distancia a centrales vía PostGIS (`ST_Distance`).
- Evidencia fotográfica de eventos (`EventPhoto`), primera versión con URL directa (previo a la integración con S3).
- Onion Architecture: separación en `domain` (models, schemas), `application` (usecases, dtos, mappers) e `infrastructure` (controllers, repositories).

## [0.1.0]

### Added
- Modelo de base de datos inicial en PostgreSQL + PostGIS: `centrales`, `usuarios`, `eventos`, `evento_fotos`.
- Configuración de creación automática de tablas al levantar la API (`init_db()` en el `lifespan` de FastAPI).
- Estructura inicial del proyecto FastAPI + SQLAlchemy async.