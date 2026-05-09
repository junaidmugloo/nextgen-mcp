# Stage 1: Builder
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files first (layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies only (not the project itself)
RUN uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY src/ ./src/

# Copy any other needed files
COPY README.md ./

# Install the project itself
RUN uv sync --frozen --no-dev

# Stage 2: Final image
FROM python:3.12-slim-bookworm

WORKDIR /app

# Ensure logs are printed immediately
ENV PYTHONUNBUFFERED=1

# Copy the entire built app from builder
COPY --from=builder /app /app

# Put the venv binaries on PATH
ENV PATH="/app/.venv/bin:$PATH"

# MCP server config
ENV MCP_TRANSPORT=sse
ENV HOST=0.0.0.0
ENV PORT=8000

EXPOSE 8000

# Use full path to avoid any PATH resolution issues
CMD ["/app/.venv/bin/nextgen-mcp"]