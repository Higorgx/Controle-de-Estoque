from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from src.db.models.models import Base  # Importa a Base centralizada

Base = declarative_base()

class Fornecedor(Base):
    __tablename__ = "fornecedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True)
    telefone = Column(String(20))
    email = Column(String(100))
    endereco = Column(String(200))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    produtos = relationship("Produto", back_populates="fornecedor")
    
    def __repr__(self):
        return f"<Fornecedor {self.nome} - CNPJ: {self.cnpj}>"