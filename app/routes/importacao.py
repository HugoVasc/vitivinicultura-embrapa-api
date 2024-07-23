from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/importacao",
    tags=["importacao"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def importacao():
    """
    Rota Default para /importacao
    """

    return {
        'message': 'OK',
        'env': 'importacao'
    }
