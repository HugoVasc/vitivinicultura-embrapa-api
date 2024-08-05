from fastapi import APIRouter
from starlette import status
import sqlite3

router = APIRouter(
    prefix="/producao",
    tags=["producao"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def producao():
    """
    Rota Default para /producao
    """

    return {
        'message': 'OK',
        'env': 'producao'
    }

@router.get("/id/{id}", status_code=status.HTTP_200_OK)
def get_id_ano(id: int):
    """
    Rota Produção / Detalhes de um item (by ID e ano)
    """
    #Banco de Dados
    try:
        conn = sqlite3.connect('vitiVinicultura.db')
        cur = conn.cursor()
    except:
        print("Erro na conexão com o banco de dados")    
    
    # cur.execute(f'SELECT sub_categories.id,sub_categories.control,sub_categories.produto,sub_categories_with_quantity.year,sub_categories_with_quantity.quantity_l FROM sub_categories INNER JOIN sub_categories_with_quantity ON sub_categories.id = sub_categories_with_quantity.sub_category_id WHERE sub_categories.id={id}')
    control = 'NA'
    produto = 'NA'
    try:
        cur.execute(f'SELECT name,description FROM sub_categories WHERE id={id}')
        rows = cur.fetchall()
        for row in rows:
           control = row[0]
           produto = row[1]
    except:
        print("Erro na consulta sub_categories")

    quantity_l = 0
    year_array = []
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT year,quantity_l FROM sub_categories_with_quantity WHERE sub_category_id={id} ORDER BY year')
        rows = cur.fetchall()
        for row in rows:
            year = row[0]
            quantity_l = row[1]
            # print(f'{year} {quantity_l}')
            
            item = {}
            # ano = year
            item[str(year)] = quantity_l
            year_array.append(item)
    except:
        print("Erro na consulta sub_categories_with_quantity")

    conn.close()
    
    return { 
        'id': id,
        'control': control,
        'produto': produto,
        'litros' : year_array
    }
    
@router.get("/ano/{ano}", status_code=status.HTTP_200_OK)
def get_ano(id: int, ano: int):
    """
    Rota Produção / Detalhes de um item (by ID e ano)
    """
    #Banco de Dados
    try:
        conn = sqlite3.connect('vitiVinicultura.db')
        cur = conn.cursor()
    except:
        print("Erro na conexão com o banco de dados")    
    
    # cur.execute(f'SELECT sub_categories.id,sub_categories.control,sub_categories.produto,sub_categories_with_quantity.year,sub_categories_with_quantity.quantity_l FROM sub_categories INNER JOIN sub_categories_with_quantity ON sub_categories.id = sub_categories_with_quantity.sub_category_id WHERE sub_categories.id={id}')
    control = 'NA'
    produto = 'NA'
    try:
        cur.execute(f'SELECT name,description FROM sub_categories WHERE id={id}')
        rows = cur.fetchall()
        for row in rows:
           control = row[0]
           produto = row[1]
    except:
        print("Erro na consulta sub_categories")

    quantity_l = 0
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT quantity_l FROM sub_categories_with_quantity WHERE sub_category_id={id} AND year={ano}')
        rows = cur.fetchall()
        for row in rows:
            quantity_l = row[0]
    except:
        print("Erro na consulta sub_categories_with_quantity")

    conn.close()
    
    return { 
        'id': id,
        'control': control,
        'produto': produto,
        'ano': ano,
        'litros': quantity_l
    }