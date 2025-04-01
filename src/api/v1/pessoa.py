import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status, responses
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.schemas.pessoa.cria_pessoa_schema import CriaPessoaSchema
from src.schemas.pessoa.altera_pessoa_schema import AlteraPessoaSchema
from src.schemas.pessoa.response_pessoa_schema import PessoaResponseSchema
from src.schemas.pessoa.response_pessoa_schema import AlteraPessoaResponseSchema
from src.repositories.pessoa_repository import PessoaRepository 
from fastapi.encoders import jsonable_encoder

router = APIRouter()

logger = logging.getLogger(__name__)

# Deve registrar um pessoa
@router.post("/", summary="Registra pessoa", status_code=status.HTTP_201_CREATED)
async def cria_pessoa(pessoaSchema: CriaPessoaSchema,db: AsyncSession = Depends(get_db)):
    existing_pessoa = await PessoaRepository.get_by_cpf_cnpj(db, pessoaSchema.cpf_cnpj)
    if existing_pessoa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pessoa com este CPF já existe"
        )
    # Create new person
    pessoa = await PessoaRepository.create(db, pessoaSchema)
    response_data = {
        "status": "success",
        "message": "Pessoa criada com sucesso",
        "data":  jsonable_encoder(pessoa)
    }
    
    return responses.JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)

# Deve alterar informações do pessoa
@router.put("/{pessoa_id}", summary="Altera informação do pessoa", status_code=status.HTTP_200_OK)
async def altera_pessoa(pessoa_id: int, pessoaSchema: AlteraPessoaSchema, db: AsyncSession = Depends(get_db)):
    existing_pessoa = await PessoaRepository.get_by_id(db, pessoa_id)
    if not existing_pessoa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não existe pessoa cadastrada com esse ID"
        )
    
    pessoa = await PessoaRepository.update(db, existing_pessoa, pessoaSchema)
    response_data = {
        "status": "success",
        "message": "Pessoa atualizado com sucesso",
        "data":  jsonable_encoder(pessoa)
    }
    
    return responses.JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)

# Deve remover o pessoa (remoção simples)
@router.patch("/{pessoa_id}", summary="Deleta o pessoa (Demissão)", status_code=status.HTTP_200_OK)
async def deleta_pessoa(pessoa_id: int, db: AsyncSession = Depends(get_db)):
    """
    Remove o pessoa (soft delete).
    """
    pass
