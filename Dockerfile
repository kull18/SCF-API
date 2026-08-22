# ============================================
# Stage 1: build - instala dependencias con las
# herramientas de compilacion necesarias (shapely
# y greenlet compilan extensiones C)
# ============================================
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================
# Stage 2: runtime - imagen final, sin herramientas
# de compilacion, solo lo necesario para correr.
# No requiere libpq: asyncpg es Python puro, a
# diferencia de psycopg (que ya no se usa).
# ============================================
FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
