import logging
from fastapi import APIRouter, Depends, HTTPException, status, responses
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from src.db.database import get_db
from src.schemas.pessoa.cria_pessoa_schema import CriaPessoaSchema
from src.schemas.pessoa.altera_pessoa_schema import AlteraPessoaSchema
from src.services.pessoa_service import PessoaService

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/", summary="Registra pessoa", status_code=status.HTTP_201_CREATED)
async def cria_pessoa(pessoaSchema: CriaPessoaSchema, db: AsyncSession = Depends(get_db)):
    pessoa = await PessoaService.criar_pessoa(db, pessoaSchema)

    response_data = {
        "status": "success",
        "message": "Pessoa criada com sucesso",
        "data": jsonable_encoder(pessoa)
    }
    return responses.JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)


@router.put("/{pessoa_id}", summary="Altera informação do pessoa", status_code=status.HTTP_200_OK)
async def altera_pessoa(pessoa_id: int, pessoaSchema: AlteraPessoaSchema, db: AsyncSession = Depends(get_db)):
    pessoa = await PessoaService.alterar_pessoa(pessoa_id, db, pessoaSchema)

    response_data = {
        "status": "success",
        "message": "Pessoa atualizada com sucesso",
        "data": jsonable_encoder(pessoa)
    }
    return responses.JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.patch("/{pessoa_id}", summary="Deleta o pessoa (Demissão)", status_code=status.HTTP_200_OK)
async def deleta_pessoa(pessoa_id: int, db: AsyncSession = Depends(get_db)):
    pessoa = await PessoaService.deletar_pessoa(pessoa_id, db)

    response_data = {
        "status": "success",
        "message": "Pessoa deletada com sucesso",
        "data": jsonable_encoder(pessoa)
    }
    return responses.JSONResponse(content=response_data, status_code=status.HTTP_200_OK)
