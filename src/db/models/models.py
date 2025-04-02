from sqlalchemy.ext.declarative import declarative_base

# Base central para todas as models
Base = declarative_base()

# Models
from src.db.models.pessoa import Pessoa
from src.db.models.produto import Produto
from src.db.models.fornecedor import Fornecedor

ALL_MODELS = [Pessoa,Produto, Fornecedor]
