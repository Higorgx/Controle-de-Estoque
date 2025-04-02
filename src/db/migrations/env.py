from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
from src.db.models.models import Base, ALL_MODELS
from dotenv import load_dotenv
import os
from src.core.config import Config

# Carregar variáveis do .env
load_dotenv()

# Configuração do logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", Config.DATABASE_URL)

# FORÇAR O REGISTRO DE TODOS OS MODELOS NA METADATA
for model in ALL_MODELS:
    model.__table__  # Isso garante que o modelo seja registrado na metadata

# Metadados dos modelos SQLAlchemy
target_metadata = Base.metadata

def run_migrations_offline():
    """
    Executa as migrations no modo offline.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations(connection):
    """
    Função auxiliar para executar migrações em uma conexão síncrona.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        render_as_batch=True,
        include_schemas=True,  # Incluir todos os esquemas
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """
    Executa as migrations no modo online.
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())