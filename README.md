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

FastAPI · SQLAlchemy (async) · PostgreSQL + PostGIS · JWT · AWS S3 · WhatsApp Business API · OneSignal

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

## Features

- [x] Alta masiva de técnicos por administrador, con credenciales enviadas por WhatsApp
- [x] Autenticación JWT con revocación y cambio de contraseña obligatorio en primer acceso
- [x] CRUD de centrales de red
- [x] Reporte de eventos de corte de fibra con cálculo automático de distancias (PostGIS)
- [x] Evidencia fotográfica y foto de perfil (S3, direccionado por contenido)
- [x] Comentarios en eventos
- [x] Notificaciones in-app y push (OneSignal)
- [ ] Migraciones formales (Alembic)
- [ ] Tests

## Contribuir

Ver [docs/development.md](docs/development.md) para convenciones de ramas, commits y estructura de PRs.