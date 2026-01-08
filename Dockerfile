FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Salin file dependensi
COPY pyproject.toml uv.lock ./

# Install dependensi Python
RUN uv sync --frozen --no-dev

# Salin kode aplikasi
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
