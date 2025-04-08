import logging
from fastapi import APIRouter, Depends, HTTPException, status, responses
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from src.db.database import get_db
from src.schemas.produto.cria_produto_schema import CriaProdutoSchema
from src.schemas.produto.altera_produto_schema import AlteraProdutoSchema
from src.services.produto_service import ProdutoService

router = APIRouter(tags=["produto"])
logger = logging.getLogger(__name__)


@router.post("/", summary="Cadastra novo produto", status_code=status.HTTP_201_CREATED)
async def cria_produto(produtoSchema: CriaProdutoSchema, db: AsyncSession = Depends(get_db)):
    produto = await ProdutoService.criar_produto(db, produtoSchema)

    response_data = {
        "status": "success",
        "message": "Produto criado com sucesso",
        "data": jsonable_encoder(produto)
    }

    return responses.JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)


@router.put("/{produto_id}", summary="Atualiza informações do produto", status_code=status.HTTP_200_OK)
async def altera_produto(produto_id: int, produtoSchema: AlteraProdutoSchema, db: AsyncSession = Depends(get_db)):
    produto = await ProdutoService.atualizar_produto(produto_id, db, produtoSchema)

    response_data = {
        "status": "success",
        "message": "Produto atualizado com sucesso",
        "data": jsonable_encoder(produto)
    }

    return responses.JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@router.patch("/{produto_id}", summary="Desativa um produto", status_code=status.HTTP_200_OK)
async def deleta_produto(produto_id: int, db: AsyncSession = Depends(get_db)):
    produto = await ProdutoService.desativar_produto(produto_id, db)

    response_data = {
        "status": "success",
        "message": "Produto desativado com sucesso",
        "data": jsonable_encoder(produto)
    }

    return responses.JSONResponse(content=response_data, status_code=status.HTTP_200_OK)