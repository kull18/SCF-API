# Contribuir a SCF

Guía de convenciones para trabajar sobre este repositorio.

## Requisitos previos

- Python 3.11+
- PostgreSQL con extensión PostGIS habilitada
- Cuenta de AWS (S3), Meta for Developers (WhatsApp Business API) y OneSignal, si vas a trabajar en features que dependan de esos servicios

## Configuración del entorno

```bash
git clone <url-del-repo>
cd scf
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
cp .env.example .env        # completa tus credenciales locales
python .\main.py
```

La API queda en `http://localhost:8000/docs`.

## Convención de ramas

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `feature/` | Nueva funcionalidad | `feature/event-comments` |
| `fix/` | Corrección de bug | `fix/password-hash-truncation` |
| `docs/` | Solo documentación, sin código | `docs/update-readme` |
| `refactor/` | Cambios internos sin alterar comportamiento | `refactor/dependency-injection` |
| `chore/` | Tareas de mantenimiento (dependencias, config) | `chore/upgrade-sqlalchemy` |

Reglas:
- Una rama por feature/fix, no mezclar temas distintos en una sola rama.
- Crea la rama siempre desde la última versión de la rama base (`main` o `develop`, según el flujo del equipo).
- El README se actualiza en la misma rama donde vive el cambio que documenta. Si es un ajuste de documentación sin código asociado, usa `docs/`.

## Convención de commits

Formato: `tipo(alcance opcional): descripción corta en imperativo`

```
feat(events): add distance calculation on event creation
fix(auth): correct bcrypt 72-byte truncation
docs: update README with notifications and comments features
refactor(users): move password hashing to dedicated service
chore(deps): add boto3 for S3 integration
```

Tipos permitidos: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`.

## Estructura de un Pull Request

1. Título siguiendo la misma convención de commits.
2. Descripción breve: qué problema resuelve o qué feature agrega.
3. Si el cambio afecta el esquema de base de datos, indícalo explícitamente (columnas nuevas, tablas nuevas, si requiere recrear tablas en desarrollo).
4. Si el cambio requiere nuevas variables de entorno, actualiza `.env.example` en el mismo PR.

## Arquitectura: dónde va cada cosa

Este proyecto sigue Onion Architecture. Antes de agregar código nuevo, ubica la capa correcta:

- **`domain/models/`** — únicamente modelos SQLAlchemy (persistencia). No debe saber nada de HTTP ni de otras capas.
- **`domain/schemas/`** — contratos de entrada (Pydantic), lo que la API recibe.
- **`application/dtos/`** — contratos de salida (Pydantic), lo que la API responde.
- **`application/mappers/`** — conversión Schema → Model y Model → DTO. Ningún otro lugar debe hacer esta conversión.
- **`application/usecases/`** — reglas de negocio y orquestación. Aquí van las validaciones que no son de formato (esas van en el Schema) sino de lógica (ej. "el código de técnico debe ser único").
- **`infrastructure/repositories/`** — acceso a datos vía SQLAlchemy. Sin lógica de negocio.
- **`infrastructure/controllers/`** — parsing del request, llamada al UseCase, nada de lógica de negocio aquí tampoco.
- **`core/`** — configuración, sesión de base de datos, middlewares transversales (auth, roles).
- **`services/`** — utilidades técnicas reutilizables entre capas (hashing, JWT, S3, WhatsApp, OneSignal, cálculo geográfico).

Regla de dependencia: las capas externas conocen a las internas, nunca al revés. Si un archivo en `domain/` necesita importar algo de `infrastructure/`, es una señal de que algo está en la capa equivocada.

## Reglas de estilo específicas del proyecto

- Los repositories reciben y devuelven directamente el `Model` de SQLAlchemy — no hay una capa de interfaces/ABC para repositorios en este proyecto (decisión deliberada para reducir ceremonia).
- Los DTOs de respuesta (`application/dtos`) nunca exponen el modelo completo de base de datos — se decide explícitamente qué campos salen.
- El `technician_code` y las contraseñas nunca se aceptan como input libre del cliente en el alta de usuarios — se generan en el backend (`services/technician_code_service.py`, `services/temp_password_service.py`).
