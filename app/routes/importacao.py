from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..database import SessionLocal
from ..models import Importacao, GoodsImportedExported

router = APIRouter(
    prefix="/importacao",
    tags=["importacao"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class ImportacaoRequest(BaseModel):
    country: str
    quantity_in_kg: float
    value_us_dollars: float
    year: int
    goods_id: int


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_importacoes(db: db_dependency, limit: int = Query(default=10, gt=0, lt=100)):
    return db.query(Importacao).limit(limit).all()


@router.get("/{importacao_id}", status_code=status.HTTP_200_OK)
async def read_importacao(db: db_dependency, importacao_id: int = Path(gt=0), ):
    importacao = db.query(Importacao).filter(Importacao.id == importacao_id).first()
    if not importacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Importacao not found.")
    return importacao


@router.get("/goods/{categoria}", status_code=status.HTTP_200_OK)
async def get_importacao_by_categoria(categoria: str, db: db_dependency):
    # Find the goods ID based on the category name
    goods = db.query(GoodsImportedExported).filter(GoodsImportedExported.name == categoria).first()
    if not goods:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria not found.")

    importacoes = db.query(Importacao).filter(Importacao.goods_id == goods.id).all()
    if not importacoes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No importacoes found for this category.")

    return importacoes


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_importacao(importacao_request: ImportacaoRequest, db: db_dependency):
    # Check if the goods_id exists in GoodsImportedExported
    goods = db.query(GoodsImportedExported).filter(GoodsImportedExported.id == importacao_request.goods_id).first()

    if not goods:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Goods ID does not exist.")

    # Create the Importacao entry
    importacao = Importacao(**importacao_request.model_dump())
    db.add(importacao)
    db.commit()
    db.refresh(importacao)

    return importacao


@router.put("/{importacao_id}", status_code=status.HTTP_200_OK)
async def update_importacao(
        importacao_id: int,
        importacao_request: ImportacaoRequest,
        db: db_dependency
):
    # Fetch the existing Importacao entry
    importacao = db.query(Importacao).filter(Importacao.id == importacao_id).first()

    if not importacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Importacao not found.")

    # Check if the goods_id exists in GoodsImportedExported
    goods = db.query(GoodsImportedExported).filter(GoodsImportedExported.id == importacao_request.goods_id).first()

    if not goods:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Goods ID does not exist.")

    # Update the fields of the Importacao entry
    importacao.country = importacao_request.country
    importacao.quantity_in_kg = importacao_request.quantity_in_kg
    importacao.value_us_dollars = importacao_request.value_us_dollars
    importacao.year = importacao_request.year
    importacao.goods_id = importacao_request.goods_id

    # Commit the changes to the database
    db.commit()
    db.refresh(importacao)

    return importacao


@router.delete("/{importacao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_importacao(importacao_id: int, db: db_dependency):
    # Fetch the existing Importacao entry
    importacao = db.query(Importacao).filter(Importacao.id == importacao_id).first()

    if not importacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Importacao not found.")

    # Delete the Importacao entry
    db.delete(importacao)
    db.commit()

    # No content to return, just the status code 204
    return
