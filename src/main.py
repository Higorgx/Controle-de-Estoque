import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import api_router
from src.db.database import init_db
from src.core.logging import setup_logging
from src.core.config import Config

# Configurar logs
setup_logging()
logger = logging.getLogger(__name__)  # Logger global para o módulo

# Instância da aplicação FastAPI
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION,
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modifique para os domínios permitidos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialização do banco de dados
@app.on_event("startup")
async def startup_event():
    """
    Configurações iniciais do sistema, como inicializar o banco de dados.
    """
    logger.info("Iniciando o sistema...")
    await init_db()
    logger.info("Sistema iniciado com sucesso.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Limpeza ao finalizar a aplicação, se necessário.
    """
    logger.info("Encerrando o sistema...")

# Registro das rotas da API
app.include_router(api_router)

# Teste de saúde da aplicação
@app.get("/", tags=["Health"])
async def health_check():
    """
    Verifica se o servidor está funcionando corretamente.
    """
    logger.info("Rota '/': Verificação de saúde")
    return {"status": "ok", "message": "FastAPI Base Project is running!"}
