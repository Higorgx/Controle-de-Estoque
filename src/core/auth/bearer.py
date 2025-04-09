from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN
from src.core.auth.handler import verify_token


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            token = credentials.credentials
            payload = verify_token(token)
            if payload:
                return payload
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Token inválido ou ausente")
