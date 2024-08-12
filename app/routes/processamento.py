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

class GrapeVarietyResponse(GrapeVarietyRequest):
    id: int

class GrapeCategoryResponse(GrapeCategoryRequest):
    id: int

class GrapeSubCategoryResponse(GrapeSubCategoryRequest):
    id: int

class ProcessedGrapesResponse(ProcessedGrapesRequest):
    id: int


router = APIRouter(
    prefix="/processamento",
    tags=["processamento"],
)


def format_request_response(result):
    response = {}
    for item in result:
        print([x.__dict__ for x in item])

        # Verifica e adiciona a chave do item[1]
        if str(item[1].id) not in response:
            response[str(item[1].id)] = {
                "name": item[1].name,
                "categories": {}
            }

        # Verifica e adiciona a chave do item[2]
        if str(item[2].id) not in response[str(item[1].id)]["categories"]:
            response[str(item[1].id)]["categories"][str(item[2].id)] = {
                "name": item[2].name,
                "subcategories": {}
            }

        # Verifica e adiciona a chave do item[3]
        if str(item[3].id) not in response[str(item[1].id)]["categories"][str(item[2].id)]["subcategories"]:
            response[str(item[1].id)]["categories"][str(item[2].id)]["subcategories"][str(item[3].id)] = {
                "name": item[3].name,
                "processed_grapes_in_kg_by_year": {}
            }

        # Adiciona ou atualiza o ano e a quantidade de uvas processadas
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
        "content": result
    }

#CREATE
@router.post("/variety", status_code=status.HTTP_201_CREATED)
async def create_grape_variety(grape_variety: GrapeVarietyRequest, db: db_dependency) -> GrapeVarietyResponse:
    variety = GrapeVarieties(**grape_variety.model_dump())
    db.add(variety)
    db.commit()
    db.refresh(variety)
    return format_default_response(variety, "create")

@router.post("/category", status_code=status.HTTP_201_CREATED)
async def create_grape_category(grape_category: GrapeCategoryRequest, db: db_dependency) -> GrapeCategoryResponse:
    category = GrapeCategories(**grape_category.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return format_default_response(category, "create")

@router.post("/subcategory", status_code=status.HTTP_201_CREATED)
async def create_grape_subcategory(grape_subcategory: GrapeSubCategoryRequest, db: db_dependency) -> GrapeSubCategoryResponse:
    subcategory = GrapeSubCategories(**grape_subcategory.model_dump())
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return format_default_response(subcategory, "create")

@router.post("/processed_grapes", status_code=status.HTTP_201_CREATED)
async def create_processed_grapes(processed_grapes: ProcessedGrapesRequest, db: db_dependency) -> ProcessedGrapesResponse:
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

@router.put("/processed_grapes/{processed_grapes_id}", status_code=status.HTTP_200_OK)
async def update_processed_grapes(processed_grapes_id: int, processed_grapes: ProcessedGrapesRequest, db: db_dependency) -> ProcessedGrapesResponse:
    grapes = db.query(ProcessedGrapes).filter(ProcessedGrapes.id == processed_grapes_id).first()
    grapes.variety_id = processed_grapes.variety_id
    grapes.category_id = processed_grapes.category_id
    grapes.subcategory_id = processed_grapes.subcategory_id
    grapes.year = processed_grapes.year
    grapes.quantity_in_kg = processed_grapes.quantity_in_kg
    db.commit()
    db.refresh(grapes)
    return format_default_response(grapes, "update")

#DELETE
@router.delete("/processed_grapes/{processed_grapes_id}", status_code=status.HTTP_200_OK)
async def delete_processed_grapes(processed_grapes_id: int, db: db_dependency) -> ProcessedGrapesResponse:
    grapes = db.query(ProcessedGrapes).filter(ProcessedGrapes.id == processed_grapes_id).first()
    db.delete(grapes)
    db.commit()
    return format_default_response(grapes, "delete")