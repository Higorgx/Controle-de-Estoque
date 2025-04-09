from fastapi import APIRouter
from src.api.auth import router as auth_router
from src.api.v1.pessoa import router as pessoa_router
from src.api.v1.produto import router as produto_router

# Cria um roteador principal
api_router = APIRouter()

api_router.include_router(auth_router, prefix="", tags=["auth"])
api_router.include_router(pessoa_router, prefix="/pessoa", tags=["pessoa"])

# TODO: deve adicionar a autenticação para as rotas que precisar quando não tiver mais em teste
# from src.core.auth.role_checker import RoleChecker
# exemplo de uso
# api_router.include_router(
#     pessoa_router,
#     prefix="/pessoa",
#     tags=["pessoa"],
#     dependencies=[Depends(RoleChecker(["1"]))]
# )

api_router.include_router(produto_router, prefix="/produto", tags=["produto"])
