# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [Unreleased]

### Added
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
- El autor de un evento ya no se autonotifica de su propio reporte (`NotifyEventCreatedUseCase` excluye `reported_by_id`).
- `domain/schemas/User.py`: se retira la creación individual de usuarios (`UserCreateSchema`) en favor del alta masiva (`BulkUserCreateSchema`).
- `full_name`, `email`, `job_title` y `profile_photo_key` en el modelo `User` son opcionales (`nullable=True`); se completan después del primer login, no en el alta.
- `application/mappers/user_mapper.py`: se retira `schema_to_model`, ya que la creación de usuarios ahora vive en `BulkCreateUsersUseCase`.

### Fixed
- Error `password cannot be longer than 72 bytes` al hashear contraseñas: se reemplazó `passlib` por `bcrypt` directo, con truncado explícito a 72 bytes antes de hashear.
- `Psycopg cannot use the 'ProactorEventLoop'` en Windows: se migró el driver de base de datos de `psycopg` (async) a `asyncpg`.
- `PydanticUserError` por atributo sin anotación de tipo en `Settings`: se corrigió `database_url` con tipo explícito y `SettingsConfigDict`.
- `ValidationError: extra_forbidden` en `Settings` por variables del `.env` (AWS, WhatsApp, OneSignal) no declaradas en la clase de configuración.
- Warning de uvicorn sobre `reload`/`workers` sin string de import: se corrigió `uvicorn.run()` para usar `"main:app"` en vez del objeto `app` directo.

### Security
- Se detectaron credenciales expuestas en texto plano durante el desarrollo (AWS Secret Access Key, OneSignal REST API Key); se recomienda rotación inmediata desde IAM y el dashboard de OneSignal respectivamente.

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