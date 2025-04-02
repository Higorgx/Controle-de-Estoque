from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class AlteraProdutoSchema(BaseModel):
    """
    Schema para alteração de dados de produto
    """
    codigo_interno: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Código interno do produto (único)"
    )
    nome: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Nome do produto"
    )
    descricao: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Descrição detalhada do produto"
    )
    preco: Optional[float] = Field(
        default=None,
        gt=0,
        description="Preço de venda (maior que zero)"
    )
    estoque: Optional[int] = Field(
        default=0,
        ge=0,
        description="Quantidade em estoque (não negativo)"
    )
    unidade_medida: Optional[str] = Field(
        default="un",
        max_length=20,
        description="Unidade de medida (un, kg, m, l, etc.)"
    )
    marca: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Marca/fabricante do produto"
    )
    codigo_barras: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Código de barras (EAN, UPC, etc.)"
    )
    ativo: Optional[bool] = Field(
        default=True,
        description="Status do produto (True = ativo, False = inativo)"
    )
    fornecedor_id: Optional[int] = Field(
        default=None,
        description="ID do fornecedor associado"
    )

    @field_validator('preco')
    @classmethod
    def arredondar_preco(cls, v: float | None) -> float | None:
        """Arredonda o preço para 2 casas decimais"""
        if v is not None:
            return round(v, 2)
        return v

    @field_validator('codigo_interno', 'codigo_barras')
    @classmethod
    def validar_codigos_unicos(cls, v: str | None, info) -> str | None:
        """Valida se os códigos não estão vazios"""
        if v is not None and len(v.strip()) == 0:
            field_name = info.field_name
            raise ValueError(f"{field_name} não pode ser vazio")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "codigo_interno": "PROD-001",
                "nome": "Smartphone Premium",
                "descricao": "Smartphone com câmera de 108MP e 256GB de armazenamento",
                "preco": 4599.99,
                "estoque": 50,
                "unidade_medida": "un",
                "marca": "TechBrand",
                "codigo_barras": "7891234567890",
                "ativo": True,
                "fornecedor_id": 1
            }
        }