from fastapi import APIRouter
from starlette import status

router = APIRouter(
    prefix="/processamento",
    tags=["processamento"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def processamento():
    """
    Rota Default para /processamento
    """

    return {
        'message': 'OK',
        'env': 'processamento'
    }
