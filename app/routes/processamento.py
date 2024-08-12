from fastapi import APIRouter, Path
from numpy import integer
from pydantic import BaseModel
from typing import List
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import SessionLocal, db_dependency

from ..models import GrapeVarieties, GrapeCategories, GrapeSubCategories, ProcessedGrapes

class GrapeVarietyRequest(BaseModel):
    name: str

class GrapeCategoryRequest(BaseModel):
    name: str
    variety_id: int

class GrapeSubCategoryRequest(BaseModel):
    name: str
    category_id: int

class ProcessedGrapesRequest(BaseModel):
    variety_id: int
    category_id: int
    subcategory_id: int
    year: int
    quantity_in_kg: int


router = APIRouter(
    prefix="/processamento",
    tags=["processamento"],
)

def format_request_response(result):
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
                            "processed_grapes_in_kg_by_year": {
                                item[3].year: item[3].quantity_kg
                            }
                        }
                    }
                }
            }
        }
    return response

def format_create_response(result):
    return {
        "message": "Objeto criado com sucesso",
        "content": result
    }

#CREATE
@router.post("/variety", status_code=status.HTTP_201_CREATED)
async def create_grape_variety(grape_variety: GrapeVarietyRequest, db: db_dependency):
    variety = GrapeVarieties(**grape_variety.model_dump())
    db.add(variety)
    db.commit()
    db.refresh(variety)
    return format_create_response(variety)

@router.post("/category", status_code=status.HTTP_201_CREATED)
async def create_grape_category(grape_category: GrapeCategoryRequest, db: db_dependency):
    category = GrapeCategories(**grape_category.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return format_create_response(category)

@router.post("/subcategory", status_code=status.HTTP_201_CREATED)
async def create_grape_subcategory(grape_subcategory: GrapeSubCategoryRequest, db: db_dependency):
    subcategory = GrapeSubCategories(**grape_subcategory.model_dump())
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return format_create_response(subcategory)

@router.post("/processed_grapes", status_code=status.HTTP_201_CREATED)
async def create_processed_grapes(processed_grapes: ProcessedGrapesRequest, db: db_dependency):
    grapes = ProcessedGrapes(**processed_grapes.model_dump())
    db.add(grapes)
    db.commit()
    db.refresh(grapes)
    return format_create_response(grapes)

#READ
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

    return format_request_response(result)

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

    return format_request_response(result)


@router.get("/ano/{year}", status_code=status.HTTP_200_OK)
async def processamento_by_year(year: int = Path(..., ge=1970, le=2023)):
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
    
    return format_request_response(result)


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

    return format_request_response(result)

