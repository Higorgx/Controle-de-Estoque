from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.produto import Produto
from src.schemas.produto.cria_produto_schema import CriaProdutoSchema
from src.schemas.produto.altera_produto_schema import AlteraProdutoSchema
from datetime import datetime
from sqlalchemy.future import select

class ProdutoRepository:
    @staticmethod
    async def create(db: AsyncSession, produtoSchema: CriaProdutoSchema):
        produto = Produto(**produtoSchema.model_dump())
        db.add(produto)
        await db.commit()
        await db.refresh(produto)
        return produto

    @staticmethod
    async def update(db: AsyncSession, produto: Produto, produtoSchema: AlteraProdutoSchema):
        update_data = produtoSchema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(produto, key, value)
        produto.data_atualizacao = datetime.now()
        await db.commit()
        await db.refresh(produto)
        return produto

    @staticmethod
    async def deactivate(db: AsyncSession, produto: Produto):
        produto.ativo = False
        produto.data_atualizacao = datetime.now()
        await db.commit()
        await db.refresh(produto)
        return produto

    @staticmethod
    async def get_by_id(db: AsyncSession, produto_id: int):
        result = await db.execute(select(Produto).where(Produto.id == produto_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_codigo_interno(db: AsyncSession, codigo_interno: str):
        result = await db.execute(select(Produto).where(Produto.codigo_interno == codigo_interno))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_codigo_barras(db: AsyncSession, codigo_barras: str):
        result = await db.execute(select(Produto).where(Produto.codigo_barras == codigo_barras))
        return result.scalar_one_or_none()