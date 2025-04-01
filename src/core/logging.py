import logging
import logging.config
from pathlib import Path

def setup_logging():
    """
    Configura o sistema de logging.
    """
    log_dir = "/tmp/logs"
    # log_dir.mkdir(parents=True, exist_ok=True)  # Cria o diretório de logs, se não existir

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "detailed",  # Usando o formato detalhado
            },
            "file": {
                "class": "logging.FileHandler",
                "formatter": "detailed",
                "filename": log_dir+"/app.log",
                "mode": "a",
            },
            "error_file": {
                "class": "logging.FileHandler",
                "formatter": "detailed",
                "filename": log_dir+"/error.log",
                "mode": "a",
                "level": "ERROR",  # Apenas erros serão gravados neste arquivo
            },
        },
        "root": {
            "level": "INFO",  # Nível global de log
            "handlers": ["console", "file", "error_file"],
        },
        "loggers": {
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
            "fastapi": {
                "level": "INFO",
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(log_config)
