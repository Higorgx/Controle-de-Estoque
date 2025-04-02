import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status, responses
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.schemas.produto.cria_produto_schema import CriaProdutoSchema
from src.schemas.produto.altera_produto_schema import AlteraProdutoSchema
from src.schemas.produto.response_produto_schema import ProdutoResponseSchema
from src.repositories.produto_repository import ProdutoRepository
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["produto"])
logger = logging.getLogger(__name__)

# Rota para cadastrar novo produto
@router.post("/", summary="Cadastra novo produto", status_code=status.HTTP_201_CREATED)
async def cria_produto(produtoSchema: CriaProdutoSchema, db: AsyncSession = Depends(get_db)):
    # Verifica se código interno já existe
    existing_produto = await ProdutoRepository.get_by_codigo_interno(db, produtoSchema.codigo_interno)
    if existing_produto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto com este código interno já existe"
        )
    
    # Verifica se código de barras já existe
    if produtoSchema.codigo_barras:
        existing_barras = await ProdutoRepository.get_by_codigo_barras(db, produtoSchema.codigo_barras)
        if existing_barras:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de barras já está em uso por outro produto"
            )
    
    # Cria novo produto
    produto = await ProdutoRepository.create(db, produtoSchema)
    
    response_data = {
        "status": "success",
        "message": "Produto criado com sucesso",
        "data": jsonable_encoder(produto)
    }
    
    return responses.JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)

# Rota para alterar informações do produto
@router.put("/{produto_id}", summary="Atualiza informações do produto", status_code=status.HTTP_200_OK)
async def altera_produto(produto_id: int, produtoSchema: AlteraProdutoSchema, db: AsyncSession = Depends(get_db)):
    existing_produto = await ProdutoRepository.get_by_id(db, produto_id)
    if not existing_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não existe produto cadastrado com esse ID"
        )
    
    # Verifica se novos códigos já existem
    if produtoSchema.codigo_interno:
        existing_codigo = await ProdutoRepository.get_by_codigo_interno(db, produtoSchema.codigo_interno)
        if existing_codigo and existing_codigo.id != produto_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código interno já está em uso por outro produto"
            )
    
    if produtoSchema.codigo_barras:
        existing_barras = await ProdutoRepository.get_by_codigo_barras(db, produtoSchema.codigo_barras)
        if existing_barras and existing_barras.id != produto_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de barras já está em uso por outro produto"
            )
    
    # Atualiza produto
    produto = await ProdutoRepository.update(db, existing_produto, produtoSchema)
    
    response_data = {
        "status": "success",
        "message": "Produto atualizado com sucesso",
        "data": jsonable_encoder(produto)
    }
    
    return responses.JSONResponse(content=response_data, status_code=status.HTTP_200_OK)

# Rota para desativar produto (remoção lógica)
@router.patch("/{produto_id}", summary="Desativa um produto", status_code=status.HTTP_200_OK)
async def deleta_produto(produto_id: int, db: AsyncSession = Depends(get_db)):
    existing_produto = await ProdutoRepository.get_by_id(db, produto_id)
    if not existing_produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não existe produto cadastrado com esse ID"
        )
    
    # Realiza a desativação (remoção lógica)
    produto = await ProdutoRepository.deactivate(db, existing_produto)
    
    response_data = {
        "status": "success",
        "message": "Produto desativado com sucesso",
        "data": jsonable_encoder(produto)
    }
    
    return responses.JSONResponse(content=response_data, status_code=status.HTTP_200_OK)