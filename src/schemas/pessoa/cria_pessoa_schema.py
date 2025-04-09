from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from src.schemas.pessoa.enums.role_enum import RoleEnum
from src.schemas.pessoa.enums.tipo_enum import TipoEnum

class CriaPessoaSchema(BaseModel):
    tipo: int = Field(..., description="Tipo de pessoa: 1 = Física, 2 = Jurídica")
    sexo: Optional[int] = Field(None, description="Sexo: 1 = Masculino, 2 = Feminino")
    nome: str = Field(..., max_length=255)
    sobrenome: Optional[str] = Field(None, max_length=255)
    endereco: Optional[str] = Field(None, max_length=255)
    bairro: Optional[str] = Field(None, max_length=255)
    cidade: Optional[str] = Field(None, max_length=255)
    cep: Optional[str] = Field(None, max_length=20, description="Pode conter traços")
    numero: Optional[int] = Field(None)
    data_nascimento: datetime = Field(..., description="Data de nascimento")
    cpf_cnpj: str = Field(..., max_length=20, description="CPF ou CNPJ (não armazenar como número)")
    rg_ie: Optional[str] = Field(None, max_length=50)
    legado: Optional[str] = Field('0', max_length=1, description="Padrão 0")

    email: EmailStr = Field(..., description="Email válido")
    senha: str = Field(..., min_length=6)
    role: RoleEnum = Field(..., description="Tipo de papel(role)em numero")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "tipo": TipoEnum.fisica.value,
                "sexo": 1,
                "nome": "João",
                "email": "email@host.com",
                "senha": "senhaSuper",
                "role": RoleEnum.administrador.value,
                "sobrenome": "Silva",
                "endereco": "Rua das Flores",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "cep": "01001-000",
                "numero": 123,
                "data_nascimento": "1990-01-01T00:00:00",
                "cpf_cnpj": "123.456.789-09",
                "rg_ie": "12.345.678-9"
            }
        }