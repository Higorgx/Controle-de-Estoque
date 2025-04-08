from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.pessoa.cria_pessoa_schema import CriaPessoaSchema
from src.schemas.pessoa.altera_pessoa_schema import AlteraPessoaSchema
from src.repositories.pessoa_repository import PessoaRepository


class PessoaService:

    @staticmethod
    async def criar_pessoa(db: AsyncSession, pessoaSchema: CriaPessoaSchema):
        legado = await PessoaRepository.get_by_id(db, '1')
        
        if legado and legado.legado == '1':
            pessoaSchema.Admin = '1'

        existing_pessoa = await PessoaRepository.get_by_cpf_cnpj(db, pessoaSchema.cpf_cnpj)
        if existing_pessoa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pessoa com este CPF já existe"
            )

        pessoa = await PessoaRepository.create(db, pessoaSchema)

        if legado:
            await PessoaRepository.delete(db, legado)

        return pessoa

    @staticmethod
    async def alterar_pessoa(pessoa_id: int, db: AsyncSession, pessoaSchema: AlteraPessoaSchema):
        existing_pessoa = await PessoaRepository.get_by_id(db, pessoa_id)
        if not existing_pessoa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não existe pessoa cadastrada com esse ID"
            )

        return await PessoaRepository.update(db, existing_pessoa, pessoaSchema)

    @staticmethod
    async def deletar_pessoa(pessoa_id: int, db: AsyncSession):
        existing_pessoa = await PessoaRepository.get_by_id(db, pessoa_id)
        if not existing_pessoa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não existe pessoa cadastrada com esse ID"
            )

        await PessoaRepository.delete(db, existing_pessoa)
        return existing_pessoa