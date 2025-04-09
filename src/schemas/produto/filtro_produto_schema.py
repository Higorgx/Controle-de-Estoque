from pydantic import BaseModel, Field
from typing import Optional

class FiltroProdutoSchema(BaseModel):
    nome: Optional[str] = Field(None, max_length=100, description="Filtrar por nome do produto (partial match)")
    codigo_interno: Optional[str] = Field(None, max_length=50, description="Filtrar por código interno exato")
    codigo_barras: Optional[str] = Field(None, max_length=50, description="Filtrar por código de barras exato")
    status: Optional[bool] = Field(None, description="Filtrar por status (True para ativos, False para inativos)")
    fornecedor_id: Optional[int] = Field(None, description="Filtrar por ID do fornecedor")
    
    class Config:
        schema_extra = {
            "example": {
                "nome": "produto",
                "codigo_interno": "PROD001",
                "status": True,
                "fornecedor_id": 1
            }
        }