from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.produto_repository import ProdutoRepository
from src.schemas.produto.cria_produto_schema import CriaProdutoSchema
from src.schemas.produto.altera_produto_schema import AlteraProdutoSchema


class ProdutoService:

    @staticmethod
    async def criar_produto(db: AsyncSession, produtoSchema: CriaProdutoSchema):
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
        return await ProdutoRepository.create(db, produtoSchema)

    @staticmethod
    async def atualizar_produto(produto_id: int, db: AsyncSession, produtoSchema: AlteraProdutoSchema):
        existing_produto = await ProdutoRepository.get_by_id(db, produto_id)
        if not existing_produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não existe produto cadastrado com esse ID"
            )

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

        return await ProdutoRepository.update(db, existing_produto, produtoSchema)

    @staticmethod
    async def desativar_produto(produto_id: int, db: AsyncSession):
        existing_produto = await ProdutoRepository.get_by_id(db, produto_id)
        if not existing_produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não existe produto cadastrado com esse ID"
            )

        return await ProdutoRepository.deactivate(db, existing_produto)