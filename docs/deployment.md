# Despliegue

## Docker

Build multi-stage: una etapa compila dependencias (`build-essential`, necesario para extensiones C de `shapely`/`greenlet`), la etapa final es una imagen `python:3.12-slim` mínima, corriendo como usuario no-root.

`asyncpg` es Python puro — a diferencia de `psycopg`, no requiere `libpq` del sistema operativo, lo que mantiene la imagen final más liviana.

```bash
docker compose up --build
```

`docker-compose.yml` levanta la API junto con `postgis/postgis:16-3.4` (Postgres con PostGIS preinstalado), evitando configurar la extensión manualmente en el host.

## Despliegue en producción (sin clonar el repositorio en el servidor)

El servidor de producción no clona el código fuente — construye la imagen localmente (o en CI) y la distribuye vía Docker Hub, manteniendo el servidor libre de credenciales de Git y del código fuente.

**En la máquina local:**
```bash
docker build -t <usuario>/scf-api:latest .
docker push <usuario>/scf-api:latest
```

**En el servidor**, con un `docker-compose.prod.yml` que referencia la imagen ya construida (`image: <usuario>/scf-api:latest`, sin `build: .`) más el servicio de `db`, y un `.env` propio de producción (contraseñas y `SECRET_KEY` distintos a los de desarrollo):
```bash
docker compose -f docker-compose.prod.yml pull api
docker compose -f docker-compose.prod.yml up -d
```

Para actualizar tras un cambio de código: repetir el build/push local, y en el servidor `pull` + `up -d` sobre el mismo `docker-compose.prod.yml` — el volumen de Postgres persiste sin interrupción, solo se reemplaza el contenedor `api`.

### Reverse proxy y HTTPS

El puerto de la API se expone solo en `127.0.0.1` dentro del servidor (`"127.0.0.1:8000:8000"` en el compose), nunca directo a internet. Nginx corre nativo en el host como reverse proxy hacia ese puerto, y Certbot (Let's Encrypt) gestiona el certificado HTTPS con renovación automática.

### Memoria y PostGIS

Cargar la extensión PostGIS por primera vez es una operación intensiva en memoria — en instancias con poca RAM (por debajo de 2GB) puede activar el OOM Killer del kernel y tumbar el proceso de Postgres a medio arrancar. Si esto ocurre, agregar swap desbloquea el arranque de forma inmediata, pero no sustituye tener RAM física suficiente para operación real con carga de usuarios:
```bash
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
```

## AWS S3 — evidencia fotográfica

Bucket privado (`Block all public access` activado), cifrado