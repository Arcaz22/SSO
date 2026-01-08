FROM python:3.12-slim

WORKDIR /app

# Install uv sistem-wide
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 1. Copy file dependency dulu (supaya kalau cuma ganti code, step ini di-skip/cache)
COPY pyproject.toml uv.lock ./

# 2. Install dependencies
# --frozen: pastikan install persis sesuai uv.lock (aman untuk prod)
# --no-dev: jangan install library testing/dev
RUN uv sync --frozen --no-dev

# 3. Baru copy sisa kodenya
COPY . .

# Pastikan path environment variable terbaca
ENV PATH="/app/.venv/bin:$PATH"

# Jalankan langsung uvicorn (tanpa 'uv run' di depannya agar lebih ringan di runtime, opsional)
# Tapi pakai 'uv run' seperti Anda juga TIDAK SALAH dan lebih aman.
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

