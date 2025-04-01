from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional

class AlteraPessoaSchema(BaseModel):
    """
    Schema para alteração de dados de pessoa (física ou jurídica)
    """
    tipo: int = Field(
        ...,
        ge=1,
        le=2,
        description="Tipo de pessoa: 1 = Física, 2 = Jurídica"
    )
    sexo: Optional[int] = Field(
        None,
        ge=1,
        le=2,
        description="Sexo: 1 = Masculino, 2 = Feminino"
    )
    nome: str = Field(
        ...,
        max_length=255,
        description="Nome completo ou razão social"
    )
    sobrenome: Optional[str] = Field(
        None,
        max_length=255,
        description="Sobrenome (para pessoa física)"
    )
    endereco: Optional[str] = Field(
        None,
        max_length=255,
        description="Logradouro completo"
    )
    bairro: Optional[str] = Field(
        None,
        max_length=255,
        description="Bairro"
    )
    cidade: Optional[str] = Field(
        None,
        max_length=255,
        description="Cidade"
    )
    cep: Optional[str] = Field(
        None,
        max_length=20,
        pattern=r'^\d{5}-?\d{3}$',
        description="CEP (com ou sem traço)"
    )
    numero: Optional[int] = Field(
        None,
        ge=0,
        description="Número do endereço"
    )
    data_nascimento: datetime = Field(
        ...,
        description="Data de nascimento (para pessoa física) ou fundação (para PJ)"
    )
    cpf_cnpj: str = Field(
        ...,
        max_length=20,
        description="CPF (11 dígitos) ou CNPJ (14 dígitos), sem formatação"
    )
    rg_ie: Optional[str] = Field(
        None,
        max_length=50,
        description="RG (PF) ou Inscrição Estadual (PJ)"
    )
    admin: str = Field(
        '0',
        max_length=1,
        pattern='^[01]$',
        description="Flag de administrador: 0 = Não, 1 = Sim"
    )

    @validator('cpf_cnpj')
    def validate_cpf_cnpj(cls, v, values):
        if 'tipo' in values:
            if values['tipo'] == 1 and len(v) != 11:  # CPF
                raise ValueError('CPF deve ter 11 dígitos')
            elif values['tipo'] == 2 and len(v) != 14:  # CNPJ
                raise ValueError('CNPJ deve ter 14 dígitos')
        return v

    @validator('data_nascimento')
    def validate_data_nascimento(cls, v, values):
        if v > datetime.now():
            raise ValueError('Data não pode ser futura')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "tipo": 1,
                "sexo": 1,
                "nome": "João",
                "sobrenome": "Silva",
                "endereco": "Rua das Flores",
                "bairro": "Centro",
                "cidade": "São Paulo",
                "cep": "01001-000",
                "numero": 123,
                "data_nascimento": "1990-01-01T00:00:00",
                "cpf_cnpj": "12345678901",
                "rg_ie": "123456789",
                "admin": "0"
            }
        }