FROM python:3.11-slim

WORKDIR /app

# Copiar solo archivos necesarios para la instalación
COPY pyproject.toml ./
COPY api_normalizer/ ./api_normalizer/

# Instalar el paquete sin cache
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir .

# Limpiar cache de pip
RUN rm -rf /root/.cache/pip

# Configurar punto de entrada
ENTRYPOINT ["api-normalizer"]
