from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional

class CriaProdutoSchema(BaseModel):
    codigo_interno: str = Field(..., max_length=50, description="Código interno do produto")
    nome: str = Field(..., max_length=100, description="Nome do produto")
    descricao: Optional[str] = Field(None, max_length=255, description="Descrição do produto")
    preco: float = Field(..., gt=0, description="Preço do produto")
    estoque: Optional[int] = Field(0, ge=0, description="Quantidade em estoque")
    unidade_medida: Optional[str] = Field("un", max_length=20, description="Unidade de medida (un, kg, m, etc.)")
    marca: Optional[str] = Field(None, max_length=50, description="Marca do produto")
    codigo_barras: Optional[str] = Field(None, max_length=50, description="Código de barras")
    ativo: Optional[bool] = Field(True, description="Indica se o produto está ativo")
    fornecedor_id: Optional[int] = Field(None, description="ID do fornecedor associado")

    @validator('preco')
    def preco_decimal(cls, v):
        return round(v, 2)
