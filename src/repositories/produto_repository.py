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
    
    @staticmethod
    async def get_all_filtered(db: AsyncSession, filtros: dict):
        query = select(Produto)
        
        if 'nome' in filtros and filtros['nome']:
            query = query.where(Produto.nome.ilike(f"%{filtros['nome']}%"))
        
        if 'codigo_interno' in filtros and filtros['codigo_interno']:
            query = query.where(Produto.codigo_interno == filtros['codigo_interno'])
        
        if 'codigo_barras' in filtros and filtros['codigo_barras']:
            query = query.where(Produto.codigo_barras == filtros['codigo_barras'])
        
        if 'status' in filtros and filtros['status'] is not None:
            query = query.where(Produto.ativo == filtros['status'])
        
        if 'fornecedor_id' in filtros and filtros['fornecedor_id']:
            query = query.where(Produto.fornecedor_id == filtros['fornecedor_id'])
        
        result = await db.execute(query)
        return result.scalars().all()