from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from ..database import SessionLocal
from ..models import Exportacao, GoodsImportedExported

router = APIRouter(
    prefix="/exportacao",
    tags=["exportacao"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class GoodsImportedExportedRequest(BaseModel):
    name: str


class ExportacaoRequest(BaseModel):
    country: str
    quantity_in_kg: float
    value_us_dollars: float
    year: int
    goods_id: int


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, limit: int = Query(default=10, gt=0, lt=100)):
    return db.query(Exportacao).limit(limit).all()


@router.get("/exported_goods", status_code=status.HTTP_200_OK)
async def read_exported_goods(db: db_dependency, ):
    exported_goods = db.query(GoodsImportedExported).filter(
        GoodsImportedExported.exported == True
    ).all()
    if exported_goods:
        result = [
            {
                "id": goods.id,
                "name": goods.name,
                "exported": goods.exported,
            }
            for goods in exported_goods
        ]
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exported goods not found.")


@router.get("/{exportacao_id}", status_code=status.HTTP_200_OK)
async def read_exportacao(db: db_dependency, exportacao_id: int = Path(gt=0), ):
    exportacao = db.query(Exportacao).filter(Exportacao.id == exportacao_id).first()
    if exportacao is not None:
        return exportacao
    raise HTTPException(status_code=404, detail="Exportacao not found.")


@router.get("/country/{country}", status_code=status.HTTP_200_OK)
async def read_exportacao(db: db_dependency, country: str):
    exportacao = db.query(Exportacao).filter(Exportacao.country == country).all()
    if exportacao is not None:
        return exportacao
    raise HTTPException(status_code=404, detail="Exportacao not found.")


@router.get("/year/{year}", status_code=status.HTTP_200_OK)
async def read_exportacao(db: db_dependency, year: int = Path(..., ge=1970, le=2023)):
    exportacao = db.query(Exportacao).filter(Exportacao.year == year).all()
    if exportacao is not None:
        return exportacao
    raise HTTPException(status_code=404, detail="Exportacao not found.")


@router.post("/new_exported_goods", status_code=status.HTTP_201_CREATED)
async def create_exported_good(exported_good: GoodsImportedExportedRequest, db: db_dependency):
    goods = GoodsImportedExported(**exported_good.model_dump(), exported=True)
    db.add(goods)
    db.commit()
    return goods


@router.post("/new_exportacao", status_code=status.HTTP_201_CREATED)
async def create_exportacao(exportacao: ExportacaoRequest, db: db_dependency):
    goods = db.query(GoodsImportedExported).filter(GoodsImportedExported.id == exportacao.goods_id).first()
    if goods is None:
        raise HTTPException(status_code=404, detail="Goods not found.")
    exportacao = Exportacao(**exportacao.model_dump())
    db.add(exportacao)
    db.commit()
    return exportacao


@router.put("/{exportacao_id}", status_code=status.HTTP_200_OK)
async def update_exportacao(
        exportacao_id: int,
        exportacao_request: ExportacaoRequest,
        db: db_dependency
):
    # Fetch the existing Exportacao entry
    exportacao = db.query(Exportacao).filter(Exportacao.id == exportacao_id).first()

    if not exportacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exportacao not found.")

    # Check if the goods_id exists in GoodsImportedExported
    goods = db.query(GoodsImportedExported).filter(GoodsImportedExported.id == exportacao_request.goods_id).first()

    if not goods:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Goods ID does not exist.")

    # Update the fields of the Exportacao entry
    exportacao.country = exportacao_request.country
    exportacao.quantity_in_kg = exportacao_request.quantity_in_kg
    exportacao.value_us_dollars = exportacao_request.value_us_dollars
    exportacao.year = exportacao_request.year
    exportacao.goods_id = exportacao_request.goods_id

    # Commit the changes to the database
    db.commit()
    db.refresh(exportacao)

    return exportacao


@router.delete("/{exportacao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exportacao(exportacao_id: int, db: db_dependency):
    # Fetch the existing Exportacao entry
    exportacao = db.query(Exportacao).filter(Exportacao.id == exportacao_id).first()

    if not exportacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exportacao not found.")

    # Delete the Exportacao entry
    db.delete(exportacao)
    db.commit()

    # No content to return, just the status code 204
    return
