from fastapi import APIRouter
from typing import List
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import SessionLocal

from ..models import GrapeVarieties, GrapeCategories, GrapeSubCategories, ProcessedGrapes

router = APIRouter(
    prefix="/processamento",
    tags=["processamento"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def processamento():
    """
    Rota Default para /processamento
    """
    # JOIN com GrapeVarieties, GrapeCategories e GrapeSubCategories e ProcessedGrapes
    result = SessionLocal().query(
        GrapeVarieties,
        GrapeCategories,
        GrapeSubCategories,
        ProcessedGrapes
    ).join(
        GrapeCategories, GrapeVarieties.id == GrapeCategories.variety_id
    ).join(
        GrapeSubCategories, GrapeCategories.id == GrapeSubCategories.category_id
    ).join(
        ProcessedGrapes, GrapeSubCategories.id == ProcessedGrapes.subcategory_id
    ).all()
    result_list = []
    for item in result:
        result_dict = {
            "GrapeVarieties": item[0].__dict__,
            "GrapeCategories": item[1].__dict__,
            "GrapeSubCategories": item[2].__dict__,
            "ProcessedGrapes": item[3].__dict__,
        }
        # Removendo '_sa_instance_state' de cada dicionário
        for key in result_dict:
            result_dict[key].pop('_sa_instance_state', None)
        result_list.append(result_dict)

    return result_list


