import asyncio
from logging.config import fileConfig
import os
from dotenv import load_dotenv

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config  # <-- PENTING: Import engine Async

from alembic import context

# --- IMPORT MODEL ANDA ---
from app.infrastructure.db.base import Base
from app.infrastructure.db import models

# Load environment variables dari file .env
load_dotenv()

config = context.config

# Set URL database dari .env agar Alembic tahu mau kemana
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """
    Fungsi helper (Sinkron) yang akan dipanggil oleh engine Async.
    Di sinilah proses migrasi yang sebenarnya terjadi.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """
    Fungsi Async untuk membuat koneksi database.
    """
    # Menggunakan async_engine_from_config (Bukan engine_from_config biasa)
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # PENTING: run_sync menjembatani driver Async dengan fungsi migrasi Sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Menjalankan fungsi async di dalam event loop
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
