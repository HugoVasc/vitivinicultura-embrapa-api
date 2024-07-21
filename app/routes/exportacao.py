from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/exportacao",
    tags=["exportacao"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def exportacao():
    """
    Rota Default para /exportacao
    """

    return {
        'message': 'OK',
        'env': 'exportacao'
    }
