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

def format_response(result):
    response = {}
    for item in result:
        response[str(item[0].id)] ={
            "name": item[0].name,
            "description": item[0].description,
            "categories": {
                str(item[1].id): {
                    "name": item[1].name,
                    "description": item[1].description,
                    "subcategories": {
                        str(item[2].id): {
                            "name": item[2].name,
                            "description": item[2].description,
                            "processed_grapes_by_year": {
                                item[3].year: {
                                    "quantity_kg": item[3].quantity_kg
                                },
                            }
                        }
                    }
                }
            }
        }
    return response


@router.get("/", status_code=status.HTTP_200_OK)
async def processamento():
    """
    Rota Default para obter todos os dados de processamento
    """
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

    return format_response(result)

@router.get("/id_categoria/{category_id}", status_code=status.HTTP_200_OK)
async def processamento_by_category_id(category_id: int):
    """
    Rota para obter os dados de processamento por categoria
    """
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
    ).filter(GrapeCategories.id == category_id).all()

    return format_response(result)


@router.get("/ano/{year}", status_code=status.HTTP_200_OK)
async def processamento_by_year(year: int):
    """
    Rota obtendo os dados de processamento por ano
    """
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
    ).filter(ProcessedGrapes.year == year).all()
    
    return format_response(result)


@router.get("/id_categoria/{category_id}/ano/{year}", status_code=status.HTTP_200_OK)
async def processamento_by_category_id_and_year(category_id: int, year: int):
    """
    Rota para obter os dados de processamento por categoria e ano
    """
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
    ).filter(GrapeCategories.id == category_id).filter(ProcessedGrapes.year == year).all()

    return format_response(result)