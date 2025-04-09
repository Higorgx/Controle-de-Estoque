import logging
from fastapi import APIRouter, Depends, HTTPException, status, responses
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from src.db.database import get_db

from src.services.auth_service import AuthService
from src.schemas.auth.login_schema import LoginSchema
from src.schemas.auth.refresh_schema import RefreshSchema

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/login", summary="Retorna token de acesso e refresh", status_code=status.HTTP_200_OK)
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    
    return await AuthService.acesso_token(db, data)

@router.post("/refresh", summary="Retorna token de refresh", status_code=status.HTTP_200_OK)
async def refresh_token(data: RefreshSchema):
    
    return await AuthService.refresh_token(data)