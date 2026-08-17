# SCF (Sistema de Cortes de Fibra)

Sistema de reporte y gestión de cortes de fibra óptica para técnicos de campo. Permite registrar centrales de red, reportar eventos de corte con ubicación geográfica (GPS o manual), calcular distancias automáticamente, y adjuntar evidencia fotográfica.

## Features

- Autenticación de usuarios y control de accesos basados en roles.
- Registro y gestión de usuarios.
- CRUD de centrales de red.
- Reporte y gestión (CRUD) de eventos de corte de fibra.
- Notificaciones en tiempo real integradas con OneSignal.

## Arquitectura

Onion Architecture (3 capas + núcleo transversal):

![Arquitectura](diagrams/arquitectura.jpg)

- **domain/**: `models` (entidades SQLAlchemy) y `schemas` (contratos de entrada, Pydantic). No depende de ninguna otra capa.
- **application/**: `usecases` (lógica de orquestación y reglas de negocio), `dtos` (contratos de salida, Pydantic), `mappers` (Schema → Model, Model → DTO).
- **infrastructure/**: `controllers` (endpoints FastAPI), `repositories` (acceso a datos vía SQLAlchemy).
- **core/**: configuración transversal — base de datos (`base`, `session`, `init_db`), configuración de entorno (`config`) y `middlewares` (autenticación y roles).
- **services/**: utilidades técnicas compartidas entre capas (hashing de contraseñas, JWT, generación de códigos de técnico, cálculo geográfico).

```text
scf/
├── .gitignore
├── README.md
├── main.py
├── diagrams/
│   ├── arquitectura.jpg
│   └── DTO_impl.jpg
└── src/
    ├── domain/
    │   ├── models/
    │   │   ├── CentralOffice.py
    │   │   ├── Event.py
    │   │   ├── EventPhoto.py
    │   │   └── User.py
    │   └── schemas/
    │       ├── AuthSchema.py
    │       ├── CentralOffice.py
    │       ├── Event.py
    │       ├── EventPhoto.py
    │       └── User.py
    │
    ├── application/
    │   ├── dtos/
    │   │   ├── auth_response.py
    │   │   └── responses/
    │   │       ├── central_office_response.py
    │   │       ├── event_response.py
    │   │       ├── event_photo_response.py
    │   │       └── user_response.py
    │   ├── mappers/
    │   │   ├── central_office_mapper.py
    │   │   ├── event_mapper.py
    │   │   ├── event_photo_mapper.py
    │   │   └── user_mapper.py
    │   └── usecases/
    │       ├── LoginUseCase.py
    │       ├── CreateUserUseCase.py
    │       ├── UpdateUserUseCase.py
    │       ├── CreateCentralOfficeUseCase.py
    │       ├── ListCentralOfficesUseCase.py
    │       ├── GetCentralOfficeUseCase.py
    │       ├── UpdateCentralOfficeUseCase.py
    │       ├── DeleteCentralOfficeUseCase.py
    │       ├── CreateEventUseCase.py
    │       ├── ListEventsUseCase.py
    │       ├── UpdateEventUseCase.py
    │       ├── CreateEventPhotoUseCase.py
    │       └── ListEventPhotosUseCase.py
    │
    ├── infrastructure/
    │   ├── controllers/
    │   │   ├── AuthController.py
    │   │   ├── UserController.py
    │   │   ├── CentralOfficeController.py
    │   │   ├── EventController.py
    │   │   └── EventPhotoController.py
    │   └── repositories/
    │       ├── UserRepository.py
    │       ├── CentralOfficeRepository.py
    │       ├── EventRepository.py
    │       └── EventPhotoRepository.py
    │
    ├── core/
    │   ├── base.py
    │   ├── config.py
    │   ├── session.py
    │   ├── init_db.py
    │   └── middlewares/
    │       ├── auth_middleware.py
    │       └── role_middleware.py
    │
    └── services/
        ├── password_service.py
        ├── token_service.py
        ├── technician_code_service.py
        ├── geo.py
        └── events.py
```

**Flujo de una petición (ejemplo: crear evento):**

![Implementación de DTO](diagrams/DTO_impl.jpg)
