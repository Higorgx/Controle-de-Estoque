import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db

# from src.repositories.pessoa_repository import PessoaRepository
# from src.schemas.pessoa.cria_pessoa_schema import CriaPessoaSchema
# from src.schemas.pessoa.enums.role_enum import RoleEnum
# from src.schemas.pessoa.enums.tipo_enum import TipoEnum

async def seed():
    async for session in get_db():
        await seed_fornecedor(session)
        break

async def seed_fornecedor(session: AsyncSession):
    # # Verifica se já existe
    # existing = await PessoaRepository.get_by_id(session, 1)
    # if not existing:
    #     pessoa_data = CriaPessoaSchema(
    #     )   
    #     await PessoaRepository.create(session, pessoa_data)
    #     print("Pessoa admin criada com sucesso.")
    # else:
    #     print("Pessoa admin já existe.")
    pass

if __name__ == "__main__":
    asyncio.run(seed())
