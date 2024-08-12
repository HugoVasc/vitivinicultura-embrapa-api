from fastapi import APIRouter, Path
from numpy import integer
from pydantic import BaseModel
from typing import List, Optional
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import SessionLocal, db_dependency

from ..models import GrapeVarieties, GrapeCategories, GrapeSubCategories, ProcessedGrapes

router = APIRouter(
    prefix="/processamento",
    tags=["processamento"],
)


class GrapeVarietyRequest(BaseModel):
    name: str

class GrapeCategoryRequest(BaseModel):
    name: str
    variety_id: int

class GrapeSubCategoryRequest(BaseModel):
    name: str
    category_id: int

class ProcessedGrapesPutDeleteRequest(BaseModel):
    variety_id: int
    category_id: int
    subcategory_id: int
    year: int

class ProcessedGrapesRequest(ProcessedGrapesPutDeleteRequest):
    quantity_in_kg: int

class GrapeVarietyResponse(GrapeVarietyRequest):
    id: int

class GrapeCategoryResponse(GrapeCategoryRequest):
    id: int

class GrapeSubCategoryResponse(GrapeSubCategoryRequest):
    id: int

class ProcessedGrapesResponse(ProcessedGrapesRequest):
    id: int


def format_request_response(result):
    response = {}
    for item in result:
        # Verifica e adiciona a chave para varieties
        if str(item[1].id) not in response:
            response[str(item[1].id)] = {
                "name": item[1].name,
                "categories": {}
            }

        # Verifica e adiciona a chave para categories
        if str(item[2].id) not in response[str(item[1].id)]["categories"]:
            response[str(item[1].id)]["categories"][str(item[2].id)] = {
                "name": item[2].name,
                "subcategories": {}
            }

        # Verifica e adiciona a chave para subcategories
        if str(item[3].id) not in response[str(item[1].id)]["categories"][str(item[2].id)]["subcategories"]:
            response[str(item[1].id)]["categories"][str(item[2].id)]["subcategories"][str(item[3].id)] = {
                "name": item[3].name,
                "processed_grapes_in_kg_by_year": {}
            }

        # Adiciona o ano ou atualiza a quantidade de uvas processadas em kg daquele ano
        response[str(item[1].id)]["categories"][str(item[2].id)]["subcategories"][str(item[3].id)][
            "processed_grapes_in_kg_by_year"][item[0].year] = item[0].quantity_in_kg

    return response


def format_default_response(result, option):

    options = {
        "create": "Objeto criado com sucesso!",
        "update": "Objeto atualizado com sucesso!",
        "delete": "Objeto deletado com sucesso!"
    }

    return {
        "message": options[option],
        "content": result.__dict__
    }

#CREATE
@router.post("/variety", status_code=status.HTTP_201_CREATED)
async def create_grape_variety(grape_variety: GrapeVarietyRequest, db: db_dependency):
    variety = GrapeVarieties(**grape_variety.model_dump())
    db.add(variety)
    db.commit()
    db.refresh(variety)
    return format_default_response(variety, "create")

@router.post("/category", status_code=status.HTTP_201_CREATED)
async def create_grape_category(grape_category: GrapeCategoryRequest, db: db_dependency):
    category = GrapeCategories(**grape_category.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return format_default_response(category, "create")

@router.post("/subcategory", status_code=status.HTTP_201_CREATED)
async def create_grape_subcategory(grape_subcategory: GrapeSubCategoryRequest, db: db_dependency):
    subcategory = GrapeSubCategories(**grape_subcategory.model_dump())
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return format_default_response(subcategory, "create")

@router.post("/processed_grapes", status_code=status.HTTP_201_CREATED)
async def create_processed_grapes(processed_grapes: ProcessedGrapesRequest, db: db_dependency):
    grapes = ProcessedGrapes(**processed_grapes.model_dump())
    db.add(grapes)
    db.commit()
    db.refresh(grapes)
    return format_default_response(grapes, "create")

#READ
@router.get("/{limit}", status_code=status.HTTP_200_OK)
async def processamento(limit: int = Path(..., ge=1)):
    """
    Rota Default para obter todos os dados de processamento
    """
    if not limit:
        limit = 10
    result = SessionLocal().query(
        ProcessedGrapes,
        GrapeVarieties,
        GrapeCategories,
        GrapeSubCategories,
    ).join(
        GrapeVarieties, ProcessedGrapes.variety_id == GrapeVarieties.id
    ).join(
        GrapeCategories, ProcessedGrapes.category_id == GrapeCategories.id
    ).join(
        GrapeSubCategories, ProcessedGrapes.subcategory_id == GrapeSubCategories.id
    ).limit(limit).all()

    return format_request_response(result)

@router.get("/id_categoria/{category_id}", status_code=status.HTTP_200_OK)
async def processamento_by_category_id(category_id: int):
    """
    Rota para obter os dados de processamento por categoria
    """
    result = SessionLocal().query(
        ProcessedGrapes,
        GrapeVarieties,
        GrapeCategories,
        GrapeSubCategories,
    ).join(
        GrapeVarieties, ProcessedGrapes.variety_id == GrapeVarieties.id
    ).join(
        GrapeCategories, ProcessedGrapes.category_id == GrapeCategories.id
    ).join(
        GrapeSubCategories, ProcessedGrapes.subcategory_id == GrapeSubCategories.id
    ).filter(GrapeCategories.id == category_id).all()

    return format_request_response(result)


@router.get("/ano/{year}", status_code=status.HTTP_200_OK)
async def processamento_by_year(year: int = Path(..., ge=1970, le=2050)):
    """
    Rota obtendo os dados de processamento por ano
    """
    result = SessionLocal().query(
        ProcessedGrapes,
        GrapeVarieties,
        GrapeCategories,
        GrapeSubCategories,
    ).join(
        GrapeVarieties, ProcessedGrapes.variety_id == GrapeVarieties.id
    ).join(
        GrapeCategories, ProcessedGrapes.category_id == GrapeCategories.id
    ).join(
        GrapeSubCategories, ProcessedGrapes.subcategory_id == GrapeSubCategories.id
    ).filter(ProcessedGrapes.year == year).all()
    
    return format_request_response(result)


@router.get("/id_categoria/{category_id}/ano/{year}", status_code=status.HTTP_200_OK)
async def processamento_by_category_id_and_year(category_id: int, year: int = Path(..., ge=1970, le=2050)):
    """
    Rota para obter os dados de processamento por categoria e ano
    """
    result = SessionLocal().query(
        ProcessedGrapes,
        GrapeVarieties,
        GrapeCategories,
        GrapeSubCategories,
    ).join(
        GrapeVarieties, ProcessedGrapes.variety_id == GrapeVarieties.id
    ).join(
        GrapeCategories, ProcessedGrapes.category_id == GrapeCategories.id
    ).join(
        GrapeSubCategories, ProcessedGrapes.subcategory_id == GrapeSubCategories.id
    ).filter(GrapeCategories.id == category_id).filter(ProcessedGrapes.year == year).all()

    return format_request_response(result)

#UPDATE

@router.put("/processed_grapes/{processed_grapes_quantity_in_kg}", status_code=status.HTTP_200_OK)
async def update_processed_grapes(processed_grapes_quantity_in_kg: int, processed_grapes: ProcessedGrapesPutDeleteRequest, db: db_dependency):
    grapes = db.query(ProcessedGrapes).filter(
        ProcessedGrapes.variety_id == processed_grapes.variety_id,
        ProcessedGrapes.category_id == processed_grapes.category_id,
        ProcessedGrapes.subcategory_id == processed_grapes.subcategory_id,
        ProcessedGrapes.year == processed_grapes.year
    ).first()
    grapes.quantity_in_kg = processed_grapes_quantity_in_kg
    db.commit()
    db.refresh(grapes)
    return format_default_response(grapes, "update")

#DELETE
@router.delete("/processed_grapes", status_code=status.HTTP_200_OK)
async def delete_processed_grapes(processed_grapes: ProcessedGrapesPutDeleteRequest, db: db_dependency):
    grapes = db.query(ProcessedGrapes).filter(
        ProcessedGrapes.variety_id == processed_grapes.variety_id,
        ProcessedGrapes.category_id == processed_grapes.category_id,
        ProcessedGrapes.subcategory_id == processed_grapes.subcategory_id,
        ProcessedGrapes.year == processed_grapes.year
    ).first()
    db.delete(grapes)
    db.commit()
    return format_default_response(grapes, "delete")