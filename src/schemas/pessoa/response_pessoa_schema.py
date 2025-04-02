from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class PessoaResponseSchema(BaseModel):
    id: int
    nome: str

class AlteraPessoaResponseSchema(BaseModel):
    id: int
    nome: str
    sexo: Optional[int] 
    sobrenome: Optional[str] 
    endereco: Optional[str]
    bairro: Optional[str] 
    cidade: Optional[str] 
    cep: Optional[str] 
    numero: Optional[int]
    data_nascimento: Optional[datetime]
    cpf_cnpj: Optional[str] 
    rg_ie: Optional[str]
    Admin: Optional[str]
    legado: Optional[str]