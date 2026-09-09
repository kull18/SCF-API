# Base de datos

PostgreSQL + PostGIS.

## Diagrama entidad-relación

![Diagrama de base de datos](diagrams/BD_scf.jpg)

## Tablas principales

Además de `central_offices`, `users` y `events` (visibles en el diagrama), el esquema incluye:

- **`event_photos`**: evidencia fotográfica, referenciando el `object_key` de S3 (direccionado por hash de contenido), no una URL directa.
- **`event_comments`**: hilo de comentarios por evento, con relación a `users` para identificar al autor.
- **`notifications`**: historial in-app de notificaciones (creación de eventos, comentarios, cambios de estado), con estado leído/no leído y referencia opcional al evento relacionado.
- **`revoked_tokens`**: blacklist de JWT revocados (logout), identificados por el `jti` único de cada token emitido.
- **`device_tokens`**: tokens opacos de larga duración para login biométrico, independientes de la contraseña real del usuario y revocables individualmente.

La tabla `users` incluye campos opcionales que se completan después del alta inicial (`full_name`, `email`, `job_title`, `profile_photo_key`), más los flags `must_change_password` y `profile_completed` que gobiernan el flujo de onboarding del técnico. El enum `event_status` tiene tres valores: `ACTIVE`, `RESOLVED`, `CLOSED`.

## Creación de tablas

Las tablas se crean automáticamente al levantar la API, dentro del `lifespan` de FastAPI (`core/init_db.py`):

```python
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        await conn.run_sync(Base.metadata.create_all)
```

**Limitación conocida:** `create_all` solo crea tablas/columnas que no existen; no altera columnas de tablas ya creadas. Cambios de esquema sobre tablas existentes requieren recrearlas manualmente en desarrollo (`DROP TABLE ... CASCADE`) hasta que se incorpore un sistema de migraciones formal (Alembic, pendiente).

**Nota práctica:** agregar un modelo nuevo (por ejemplo, `DeviceToken`) requiere registrarlo explícitamente en el import de `core/init_db.py` — si un modelo no se importa ahí, `create_all` nunca genera su tabla, aunque el archivo del modelo exista en el proyecto. Lo mismo aplica para que SQLAlchemy resuelva correctamente relaciones declaradas por nombre de string entre modelos (por ejemplo, `Event.comments` apuntando a `"EventComment"`): todos los modelos relacionados deben estar importados en el mismo punto de entrada antes de que cualquier instancia se cree, o SQLAlchemy falla con `InvalidRequestError` al no poder resolver el nombre.

## Cálculo de distancias

Las distancias entre un evento y sus centrales de origen/destino se calculan en el momento de creación, vía PostGIS:

```sql
SELECT ST_Distance(location, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)) / 1000.0
FROM central_offices WHERE id = :office_id;
```

Es distancia geográfica en línea recta (no ruta física de fibra). Ver decisión original en la sección 11 del documento de diseño inicial del proyecto.

## Carga de relaciones (eager loading)

Los endpoints que devuelven eventos (`GET /events`, `GET /events/{id}`) incluyen objetos anidados con datos de las centrales de origen/destino y del técnico que reportó el evento, en vez de solo sus IDs. Esto se resuelve con `selectinload` en las queries del `EventRepository` (`origin_office`, `destination_office`, `reported_by`, `photos`), evitando el problema de N+1 queries que ocurriría si cada relación se cargara de forma perezosa por fila.

## Automatización

Un job programado (`core/scheduler.py`, vía `APScheduler`) corre diariamente y cierra automáticamente los eventos en estado `RESOLVED` que llevan más de 24 horas sin cambios, pasándolos a `CLOSED`. Existe también un endpoint manual (`POST /events/close-resolved-now`, solo `ADMIN`) para disparar el mismo proceso sin esperar al ciclo programado, útil en pruebas.

## Pendientes

- Migraciones formales con Alembic.
- Limpieza periódica de `revoked_tokens` (método `purge_expired()` ya existe en el repository, sin scheduler conectado).