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


class ProdutoListResponseSchema(BaseModel):
    id: int
    codigo_interno: str
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: Optional[int] = None
    unidade_medida: Optional[str] = None
    marca: Optional[str] = None
    codigo_barras: Optional[str] = None
    ativo: bool
    fornecedor_id: Optional[int] = None
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True       