from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from pathlib import Path
from src.db.models.models import Base  # Importa a Base centralizada com as models
from src.core.config import Config
import os
import logging

# Carrega as variáveis do arquivo .env
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Configuração do logger
logger = logging.getLogger(__name__)

# Configuração do engine para conexões assíncronas
engine = create_async_engine(
    Config.DATABASE_URL,
    echo=False,  # Mude para True para exibir as queries SQL no log
    future=True,
)

# Configuração do sessionmaker para criar sessões do banco de dados
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)

async def init_db():
    """
    Inicializa o banco de dados e verifica a conexão.
    """
    try:
        logger.info("Iniciando conexão com o banco de dados...")
        # async with engine.begin() as conn:
        #     # Cria as tabelas no banco de dados, caso elas não existam
        #     await conn.run_sync(Base.metadata.create_all)
        logger.info("Conexão com o banco de dados estabelecida com sucesso.")
    except SQLAlchemyError as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao inicializar o banco de dados: {e}")
        raise

# Dependência para injetar o banco de dados em endpoints
async def get_db():
    """
    Fornece uma sessão de banco de dados para ser usada nos endpoints.
    """
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
