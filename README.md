# SCF (Sistema de Cortes de Fibra)

Sistema de reporte y gestión de cortes de fibra óptica para técnicos de campo. Permite registrar centrales de red, reportar eventos de corte con ubicación geográfica (GPS o manual), calcular distancias automáticamente, adjuntar evidencia fotográfica, comentar eventos y recibir notificaciones push.

## Documentación

| Documento | Contenido |
|---|---|
| [Arquitectura](docs/architecture.md) | Capas de Onion Architecture, regla de dependencia, flujo de una petición, manejo de errores |
| [Base de datos](docs/database.md) | Esquema de tablas, PostGIS, cálculo de distancias |
| [Despliegue](docs/deployment.md) | Docker, variables de entorno, AWS S3, WhatsApp, OneSignal |
| [Desarrollo](docs/development.md) | Setup local, convenciones de ramas y commits |

## Stack

FastAPI · SQLAlchemy (async) · PostgreSQL + PostGIS · JWT · AWS S3 · WhatsApp Business API (con Twilio como estrategia alternativa) · OneSignal · APScheduler

## Levantar el proyecto

```bash
git clone <url-del-repo>
cd scf
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
copy .env.example .env      # completa tus credenciales
python .\main.py
```

Alternativa con Docker:

```bash
docker compose up --build
```

Para crear el primer usuario administrador (necesario antes de poder usar `POST /users/bulk`), corre el script de seed:

```bash
python seed_admin.py
```

También hay un `seed_technician.py` disponible para generar técnicos de prueba (útil, por ejemplo, para credenciales de revisión de Google Play/App Store).

## Features

- [x] Alta masiva de técnicos por administrador, con credenciales enviadas por WhatsApp
- [x] Autenticación JWT con revocación y cambio de contraseña obligatorio en primer acceso
- [x] Login biométrico vía device-token opaco y revocable (sin exponer la contraseña real)
- [x] Recuperación de contraseña sin enumeración de usuarios
- [x] CRUD de centrales de red
- [x] Reporte de eventos de corte de fibra con cálculo automático de distancias (PostGIS)
- [x] Consulta de eventos individual (`GET /events/{id}`) con objetos anidados de centrales y técnico que reportó
- [x] Evidencia fotográfica y foto de perfil (S3, direccionado por contenido)
- [x] Comentarios en eventos, incluyendo foto de perfil del autor
- [x] Restricción de propiedad: solo quien reportó un evento puede cambiar su estado
- [x] Cierre automático de eventos atendidos tras 24 horas (job programado diario)
- [x] Notificaciones in-app y push (OneSignal)
- [x] Seguridad: rate limiting, CORS, límite de tamaño de request, manejo de errores centralizado
- [ ] Migraciones formales (Alembic)
- [ ] Tests

## Contribuir

Ver [docs/development.md](docs/development.md) para convenciones de ramas, commits y estructura de PRs.