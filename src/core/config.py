import os
from pathlib import Path

class Config:
    """
    Classe para gerenciar as configurações do projeto.
    """
    # Diretório base do projeto
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # Diretório para uploads
    UPLOAD_DIR = BASE_DIR / "uploads"

    # Tipos de arquivo permitidos
    ALLOWED_FILE_TYPES = ["image/png", "image/jpeg", "application/pdf"]

    # Tamanho máximo do arquivo em bytes (exemplo: 10 MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    # Banco de Dados
    DATABASE_URL = (
        f"{os.getenv('DB_DRIVER')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    # Configurações de API
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    API_VERSION = "v1"
    API_TITLE = "FastAPI Project"
    API_DESCRIPTION = "Uma aplicação FastAPI com estrutura modular e suporte a CRUD e uploads."
