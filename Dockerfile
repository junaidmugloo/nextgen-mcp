# Use a specialized uv image for fast builds
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a separate volume
ENV UV_LINK_MODE=copy

# Install the project into /app
WORKDIR /app

# Copy dependency files first (for caching)
COPY uv.lock pyproject.toml /app/

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the source code
COPY . /app

# Install the project
RUN uv sync --frozen --no-dev

# Final image
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy the environment from the builder
COPY --from=builder /app /app

# Place executable on path
ENV PATH="/app/.venv/bin:$PATH"

# Environment variables (can be overridden on Railway)
ENV MCP_TRANSPORT=sse
ENV PORT=8000
ENV HOST=0.0.0.0

# Expose the port
EXPOSE 8000

# Run the application
CMD ["nextgen-mcp"]
