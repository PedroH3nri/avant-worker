# syntax=docker/dockerfile:1.7
# O avant-core é privado: o build recebe um token de leitura do GitHub como secret,
# que não fica em nenhuma camada da imagem.
#   docker build --secret id=github_token,env=GITHUB_TOKEN -t ghcr.io/pedroh3nri/avant-worker .
FROM python:3.12-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /usr/local/bin/uv
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN --mount=type=secret,id=github_token \
    git config --global url."https://x-access-token:$(cat /run/secrets/github_token)@github.com/".insteadOf "https://github.com/" \
    && uv sync --frozen --no-dev \
    && git config --global --unset-all url."https://x-access-token:$(cat /run/secrets/github_token)@github.com/".insteadOf

FROM python:3.12-slim
RUN useradd --system --uid 10001 avant
WORKDIR /app
COPY --from=build /app /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
USER avant
# Sem porta: o worker só fala com o RabbitMQ, o Redis e o Postgres. O comando muda no
# compose (worker ou beat).
CMD ["celery", "-A", "avant_worker.app", "worker", "-Q", "default,mail,gam", "-l", "info"]
