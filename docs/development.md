# Desarrollo

## Requisitos

- Python 3.12+
- PostgreSQL con PostGIS (o Docker, ver `deployment.md`)
- Cuentas de AWS, Meta for Developers y OneSignal si se trabaja en features que dependan de esos servicios

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

```
tipo(alcance opcional): descripción corta en imperativo
```

Ejemplos: `feat(events): add distance calculation on event creation`, `fix(auth): correct bcrypt 72-byte truncation`, `refactor(usecases): replace ValueError with typed exceptions`.

## Dónde va cada cosa (ver `architecture.md` para el detalle completo)

- Regla de negocio nueva → `application/usecases/`
- Excepción de negocio nueva → hereda de `AppError` en `core/exceptions.py`, con su handler en `core/exception_handlers.py`
- Campo nuevo que el cliente envía → `domain/schemas/`
- Campo nuevo que el cliente recibe → `application/dtos/responses/`
- Conversión entre ambos → `application/mappers/`
- Query nueva a la base de datos → `infrastructure/repositories/` (sin validaciones de negocio ahí)
- Utilidad técnica sin estado de negocio (ej. un nuevo proveedor de SMS) → `services/`