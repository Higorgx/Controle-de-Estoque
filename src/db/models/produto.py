# src/db/models/produto.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.models.models import Base

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_interno = Column(String(50), unique=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    unidade_medida = Column(String(20), default="un")  
    marca = Column(String(50))
    codigo_barras = Column(String(50), unique=True)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Corrigido para "fornecedores.id" (deve bater com __tablename__ do Fornecedor)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
    fornecedor = relationship("Fornecedor", back_populates="produtos")
    
    def __repr__(self):
        return f"<Produto {self.nome} - R${self.preco}>"