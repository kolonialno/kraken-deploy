FROM python:3.10-alpine AS base

WORKDIR /app

FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.7

RUN apk add --no-cache gcc libffi-dev musl-dev openssl-dev cargo
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

# Build and install dependencies
COPY pyproject.toml poetry.toml poetry.lock ./
RUN poetry install

# Build and install project
COPY kraken ./
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base AS final

RUN apk add --no-cache libffi

# Copy virtualenv from the builder
COPY --from=builder /venv /venv

ENV PATH="/venv/bin:$PATH" \
    VIRTUAL_ENV="/venv"

ENTRYPOINT ["python", "-m", "kraken"]
