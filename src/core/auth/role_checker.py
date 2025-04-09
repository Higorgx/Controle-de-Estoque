from fastapi import Depends, HTTPException, status
from src.core.auth.bearer import JWTBearer

def RoleChecker(allowed_roles: list[str]):
    async def verify_role(token_data=Depends(JWTBearer())):
        role = token_data.get("role")
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar esse recurso"
            )
        return token_data
    return verify_role
