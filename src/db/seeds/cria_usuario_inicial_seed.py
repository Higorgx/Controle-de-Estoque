import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.repositories.pessoa_repository import PessoaRepository
from src.schemas.pessoa.cria_pessoa_schema import CriaPessoaSchema
from src.schemas.pessoa.enums.role_enum import RoleEnum
from src.schemas.pessoa.enums.tipo_enum import TipoEnum

async def seed():
    async for session in get_db():
        await seed_pessoas(session)
        break

async def seed_pessoas(session: AsyncSession):
    # Verifica se já existe
    existing = await PessoaRepository.get_by_id(session, 1)
    if not existing:
        pessoa_data = CriaPessoaSchema(
            nome="Admin",
            tipo=TipoEnum.fisica.value,
            cpf_cnpj="12345678900",
            data_nascimento="1990-01-01 00:00:00",
            email="admin@example.com",
            senha="1231231",
            role= RoleEnum.administrador.value
        )   
        await PessoaRepository.create(session, pessoa_data)
        print("Pessoa admin criada com sucesso.")
    else:
        print("Pessoa admin já existe.")

if __name__ == "__main__":
    asyncio.run(seed())
