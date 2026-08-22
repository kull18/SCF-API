# Despliegue

## Docker

Build multi-stage: una etapa compila dependencias (`build-essential`, necesario para extensiones C de `shapely`/`greenlet`), la etapa final es una imagen `python:3.12-slim` mínima, corriendo como usuario no-root.

`asyncpg` es Python puro — a diferencia de `psycopg`, no requiere `libpq` del sistema operativo, lo que mantiene la imagen final más liviana.

```bash
docker compose up --build
```

`docker-compose.yml` levanta la API junto con `postgis/postgis:16-3.4` (Postgres con PostGIS preinstalado), evitando configurar la extensión manualmente en el host.


## AWS S3 — evidencia fotográfica

Bucket privado (`Block all public access` activado), cifrado SSE-S3, versionado activo, `Bucket owner enforced`. Acceso vía IAM user dedicado con política de mínimo privilegio (`PutObject`, `GetObject`, `DeleteObject` restringido a `arn:aws:s3:::<bucket>/*`).

Las fotos (evidencia de eventos y perfiles de usuario) se suben directo del cliente a S3 mediante URLs prefirmadas — el backend nunca recibe el binario. El nombre del objeto es el **hash SHA-256 del contenido**, calculado en el cliente:

```
events/{event_id}/{sha256_hash}.{ext}
profiles/{user_id}/{sha256_hash}.{ext}
```

Esto da deduplicación automática (dentro del mismo evento/usuario) y verificación de integridad, similar al patrón de content-addressable storage usado por plataformas de mensajería.

## WhatsApp Business API

Requiere: cuenta de Meta Business, número verificado, y un **message template** aprobado por Meta (categoría *Utility*) para poder iniciar conversaciones no solicitadas por el usuario (necesario para el envío de credenciales en el alta masiva).

## OneSignal

Notificaciones push asociadas por `technician_code` como `external_id` (vía `OneSignal.login()` en el cliente Flutter), no por `player_id` directo — simplifica el envío desde el backend sin tener que rastrear tokens de dispositivo por su cuenta.

## Infraestructura recomendada

Dado el volumen esperado (~50 usuarios) y que el proyecto ya usa AWS para S3/IAM: **AWS Lightsail**, corriendo la imagen Docker vía Lightsail Containers o una instancia estándar con `docker compose`. Se descartó AWS ECS/Fargate por ser sobre-ingeniería para esta escala.