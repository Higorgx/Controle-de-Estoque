# src/db/models/models.py
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Importe TODOS os modelos aqui
from src.db.models.pessoa import Pessoa
from src.db.models.produto import Produto
from src.db.models.fornecedor import Fornecedor

# Lista completa de modelos
ALL_MODELS = [Pessoa, Produto, Fornecedor]