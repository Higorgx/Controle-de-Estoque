import logging
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import List, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import Optional



from src.db.models.pessoa import Pessoa
from src.schemas.pessoa.cria_pessoa_schema import CriaPessoaSchema
from src.schemas.pessoa.altera_pessoa_schema import AlteraPessoaSchema

logger = logging.getLogger(__name__)

class PessoaRepository():
    """docstring for PessoaRepository."""

    async def get_all(self, db: AsyncSession) -> List:

        pessoas = await db.execute(select(Pessoa))
        return pessoas.scalars().all()

    async def get_by_id(db: AsyncSession, pessoa_id: int) -> Optional[Pessoa]:
        return await db.get(Pessoa, pessoa_id)

    @staticmethod
    async def create(db: AsyncSession, pessoa_data: CriaPessoaSchema) -> Pessoa:
        db_pessoa = Pessoa(**pessoa_data.dict())
        db.add(db_pessoa)
        await db.commit()
        await db.refresh(db_pessoa)
        return {
        "id": db_pessoa.id,
        "nome": db_pessoa.nome,
        # outros campos
    } 

    @staticmethod
    async def get_by_cpf_cnpj(db: AsyncSession, cpf_cnpj: str) -> Optional[Pessoa]:
        query = select(Pessoa).where(Pessoa.cpf_cnpj == cpf_cnpj)
        result = await db.execute(query)
        return result.scalars().first()  # Returns None if not found

    async def delete(self, db: AsyncSession, pessoa_id: int) -> bool:
        pessoa = await self.get_by_id(db, pessoa_id)
        if not pessoa:
            return False

        await db.delete(pessoa)
        await db.commit()
        return True
    
    @staticmethod
    async def update(db: AsyncSession, existing_pessoa : Pessoa, pessoa_data: AlteraPessoaSchema) -> Optional[Pessoa]:
        try:
            # Update fields
            update_data = pessoa_data.model_dump(exclude_unset=True)
            hoje = func.now()
            for field, value in update_data.items():
                # Skip fields that shouldn't be updated directly
                if field in ['cpf_cnpj', 'data_criacao']:  # Add other protected fields if needed
                    continue
                    
                if hasattr(existing_pessoa, field):
                    setattr(existing_pessoa, field, value)

            # Always update the modification date
            existing_pessoa.data_atualizacao = hoje

            # Validate business rules
            if pessoa_data.tipo == 1:  # Pessoa Física
                if not pessoa_data.sobrenome:
                    raise ValueError("Sobrenome é obrigatório para pessoa física")
            
            # Verify CPF/CNPJ uniqueness if being changed
            if 'cpf_cnpj' in update_data:
                existing = await PessoaRepository.get_by_cpf_cnpj(db, pessoa_data.cpf_cnpj)
                if existing and existing.id != existing_pessoa.id:
                    raise ValueError("Já existe uma pessoa com este CPF/CNPJ")

            await db.commit()
            await db.refresh(existing_pessoa)
            return existing_pessoa

        except NoResultFound as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ValueError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar pessoa: {str(e)}"
            )
