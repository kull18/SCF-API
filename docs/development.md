# Desarrollo

## Requisitos

- Python 3.12+
- PostgreSQL con PostGIS (o Docker, ver `deployment.md`)
- Cuentas de AWS, Meta for Developers, Twilio (opcional, proveedor alternativo de WhatsApp) y OneSignal si se trabaja en features que dependan de esos servicios

## Setup local

```bash
git clone <url-del-repo>
cd scf
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
copy .env.example .env      # completar credenciales locales
python .\main.py
```

API disponible en `http://localhost:8000/docs`.

### Primer arranque: crear el usuario administrador

`POST /users/bulk` requiere rol `ADMIN`, y no hay forma de crear uno sin ya serlo — por eso el primer admin se crea con un script standalone, no vía API:

```bash
python seed_admin.py
```

También existe `seed_technician.py`, útil para generar cuentas de técnico de prueba (por ejemplo, para credenciales de revisión de Google Play/App Store) sin pasar por el flujo real de WhatsApp.

### Cambios de esquema durante desarrollo

Como `create_all` no altera columnas de tablas existentes (ver `database.md`), agregar o modificar un campo en un modelo requiere recrear esa tabla manualmente mientras no exista Alembic:

```bash
docker compose exec db psql -U postgres -d scf -c "DROP TABLE IF EXISTS <tabla> CASCADE;"
```

El `CASCADE` elimina foreign keys que otras tablas tengan hacia la que se borra (esas tablas no se pierden, solo la constraint) — al reiniciar el servidor, `init_db()` recrea todo con el esquema actual.

## Convención de ramas

| Prefijo | Uso |
|---|---|
| `feature/` | Nueva funcionalidad |
| `fix/` | Corrección de bug |
| `docs/` | Solo documentación |
| `refactor/` | Cambios internos sin alterar comportamiento externo |
| `chore/` | Mantenimiento, dependencias, infraestructura |
| `security/` | Medidas de seguridad (rate limiting, CORS, revocación de tokens, etc.) |

Una rama por feature/fix. El README/docs se actualiza en la misma rama donde vive el cambio que documenta.

## Convención de commits