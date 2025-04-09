from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.auth.handler import create_access_token, create_refresh_token, verify_token
from src.core.auth.security import verify_password
from src.schemas.auth.login_schema import LoginSchema
from src.schemas.auth.refresh_schema import RefreshSchema
from src.repositories.pessoa_repository import PessoaRepository


class AuthService:

    @staticmethod
    async def acesso_token(db: AsyncSession, loginSchema: LoginSchema):
        user = await PessoaRepository.get_by_email(db, loginSchema.email)

        if not user or not verify_password(loginSchema.senha, user.senha):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

        # TODO: aqui deve ter ou tem que ter um objeto para ficar como base (um schema)...
        # TODO: deve revisar as informações que são pertinentes ao front 
        token_data = {"sub": user.email, "role": user.role}

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    @staticmethod
    async def refresh_token(refreshSchema: RefreshSchema):
        payload = verify_token(refreshSchema.refresh_token)
        if not payload:
            raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

        new_access_token = create_access_token({
            "sub": payload["sub"],
            "role": payload["role"]
        })

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }