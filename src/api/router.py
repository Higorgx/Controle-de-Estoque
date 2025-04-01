from fastapi import APIRouter
from src.api.v1.pessoa import router as pessoa_router

# Cria um roteador principal
api_router = APIRouter()

api_router.include_router(pessoa_router, prefix="/pessoa", tags=["pessoa"])
