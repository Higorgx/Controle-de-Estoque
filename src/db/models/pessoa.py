from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, CHAR, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.db.models.models import Base  # Importa a Base centralizada

from datetime import datetime

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(Integer, nullable=False)  # Exemplo: 1 = Física, 2 = Jurídica
    sexo = Column(Integer, nullable=True)  # Exemplo: 1 = Masculino, 2 = Feminino
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=True)
    endereco = Column(String(255), nullable=True)
    bairro = Column(String(255), nullable=True)
    cidade = Column(String(255), nullable=True)
    cep = Column(String(20), nullable=True)  # Pode conter traços
    numero = Column(Integer, nullable=True)
    data_nascimento = Column(DateTime, nullable=False)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)  # Não armazenar como número
    rg_ie = Column(String(50), nullable=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    Admin = Column(CHAR(), nullable=True)
