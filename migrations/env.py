from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from code_war.database import Base
from code_war.settings import Settings

# Interpretar o arquivo de configuração Alembic
config = context.config
fileConfig(config.config_file_name)

# Define a URL do banco diretamente com Settings (substituindo o alembic.ini)
config.set_main_option("sqlalchemy.url", Settings().DATABASE_URL)

# Define o metadata (necessário para autogenerate funcionar)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa as migrações no modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações no modo 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
