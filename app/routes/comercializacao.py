from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/comercializacao",
    tags=["comercializacao"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def comercializacao():
    """
    Rota Default para /comercializacao
    """

    return {
        'message': 'OK',
        'env': 'comecializacao'
    }
