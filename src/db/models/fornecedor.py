from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.models.models import Base  # Importa a Base centralizada

class Fornecedor(Base):
    __tablename__ = "fornecedores"  # Nome da tabela no banco de dados
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)  # CNPJ sem formatação
    telefone = Column(String(20))
    email = Column(String(100))
    endereco = Column(String(200))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, server_default=func.now())
    data_atualizacao = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relacionamento com Produtos (um fornecedor pode ter muitos produtos)
    produtos = relationship("Produto", back_populates="fornecedor", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Fornecedor {self.nome} (CNPJ: {self.cnpj})>"

    # Método para formatação do CNPJ (opcional)
    @property
    def cnpj_formatado(self):
        if len(self.cnpj) == 14:
            return f"{self.cnpj[:2]}.{self.cnpj[2:5]}.{self.cnpj[5:8]}/{self.cnpj[8:12]}-{self.cnpj[12:]}"
        return self.cnpj