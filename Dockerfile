FROM python:3.12-slim as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY src/ ./src/
COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-dev

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /bin/uv /bin/uv

COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src/
COPY pyproject.toml uv.lock README.md ./

EXPOSE 8000

CMD ["uv", "run", "-m", "mcengine"]

