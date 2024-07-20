from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/producao",
    tags=["producao"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def producao():
    """
    Rota Default para /producao
    """

    return {
        'message': 'OK',
        'env': 'producao'
    }
