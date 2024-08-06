from fastapi import APIRouter
from starlette import status
from ..database import SessionLocal

from ..models import WineCategories, ProducedWineCategoriesWithQuantity, WineSubCategories, ProducedWineSubCategoriesWithQuantity

router = APIRouter(
    prefix="/producao",
    tags=["producao"],
)

def format_response(result):
    response = {}
    for item in result:
        # print(item.id, item.category, item.year, item.quantity_in_l)
        response[str(item[0].id)] = {
            "categoria": item[0].category,
            "ano": item[0].year,
            "quantidade_litros": item[0].quantity_in_l
        }
            
    return response

@router.get("/", status_code=status.HTTP_200_OK)
async def producao():
    """
    Rota Default para /producao
    Soma por categoria
    """

    result = SessionLocal().query(
        ProducedWineCategoriesWithQuantity,
        WineCategories
    # ).join(
    #     WineCategories, ProducedWineCategoriesWithQuantity.category == WineCategories.id
    ).all()
    
    return format_response(result)


@router.get("/categoria", status_code=status.HTTP_200_OK)
async def producao_categoria(categoria: str = "VINHO DE MESA"):
    """
    Rota para /producao/categoria.
    Filtro por categoria
    """
    
    print(categoria)
    
    result = SessionLocal().query(
        ProducedWineCategoriesWithQuantity,
        WineCategories
    # ).join(
    #     WineCategories, ProducedWineCategoriesWithQuantity.category == WineCategories.id
    ).filter(
        ProducedWineCategoriesWithQuantity.category == categoria
    ).all()
    return format_response(result)

@router.get("/categoria/lista", status_code=status.HTTP_200_OK)
async def producao_categoria_lista():
    """
    Rota para /producao/categoria/lista. 
    Lista todas as categorias cadastradas.
    """
    
    result = SessionLocal().query(
        ProducedWineCategoriesWithQuantity,
        WineCategories
    # ).join(
    #     WineCategories, ProducedWineCategoriesWithQuantity.category == WineCategories.id
    ).all()
    
    response = {}
    for item in result:
        # print(item.id, item.category, item.year, item.quantity_in_l)
        response[str(item[1].id)] = {
            "categoria": item[1].category,
        }
            
    return response
    
@router.get("/subcategoria/lista", status_code=status.HTTP_200_OK)
async def producao_subcategoria_lista():
    """
    Rota para /producao/subcategoria/lista. 
    Lista todas as sub-categorias cadastradas.
    """
    
    result = SessionLocal().query(
        WineSubCategories
    ).all()
    
    response = {}
    for item in result:
        # print(item.id, item.category, item.year, item.quantity_in_l)
        response[str(item.id)] = {
            "subcategoria": item.subcategory,
        }
            
    return response

@router.get("/subcategoria", status_code=status.HTTP_200_OK)
async def producao_subcategoria():
    """
    Rota para /producao/subcategoria. 
    Lista todas os itens de cada subcategoria.
    """
    
    result = SessionLocal().query(
        ProducedWineSubCategoriesWithQuantity,
        WineSubCategories
    ).join(
        WineSubCategories, ProducedWineSubCategoriesWithQuantity.subcategory_id == WineSubCategories.id
    ).all()
    
    response = {}
    for item in result:
        # print(item.id, item.category, item.year, item.quantity_in_l)
        response[str(item[0].id)] = {
            "subcategoria": {
                "nome": item[1].subcategory,
                "id": item[0].subcategory_id
            },
            "ano": item[0].year,
            "quantidade_litros": item[0].quantity_in_l
        }
            
    return response
    
@router.get("/subcategoria/tipo", status_code=status.HTTP_200_OK)
async def producao_subcategoria_filtro(subcategoria: str = "Tinto"):
    """
    Rota para /producao/subcategoria/tipo. 
    Lista os items de um sub-categorias especifica
    """
    
    result = SessionLocal().query(
        ProducedWineSubCategoriesWithQuantity,
        WineSubCategories
    ).join(
        WineSubCategories, ProducedWineSubCategoriesWithQuantity.subcategory_id == WineSubCategories.id
    ).filter(
        WineSubCategories.subcategory == subcategoria
    ).all()
    
    response = {}
    for item in result:
        # print(item.id, item.category, item.year, item.quantity_in_l)
        response[str(item[0].id)] = {
            "subcategoria": {
                "nome": item[1].subcategory,
                "id": item[0].subcategory_id
            },
            "ano": item[0].year,
            "quantidade_litros": item[0].quantity_in_l
        }
            
    return response