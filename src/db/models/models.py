from sqlalchemy.ext.declarative import declarative_base

# Base central para todas as models
Base = declarative_base()

# Models
from src.db.models.pessoa import Pessoa

ALL_MODELS = [Pessoa]
