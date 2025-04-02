from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ProdutoResponseSchema(BaseModel):
    id: int
    nome: str

class AlteraProdutoResponseSchema(BaseModel):
    id: int
    codigo_interno: Optional[str]
    nome: Optional[str]
    descricao: Optional[str]
    preco: Optional[float]
    estoque: Optional[int]
    unidade_medida: Optional[str]
    marca: Optional[str]
    codigo_barras: Optional[str]
    ativo: Optional[bool]
    fornecedor_id: Optional[int]
    data_criacao: Optional[datetime]
    data_atualizacao: Optional[datetime]

    class Config:
        from_attributes = True  # Equivalente ao antigo orm_mode = True no Pydantic v2