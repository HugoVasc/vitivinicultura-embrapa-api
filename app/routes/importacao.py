from fastapi import APIRouter
from starlette import status
import sqlite3

router = APIRouter(
    prefix="/importacao",
    tags=["importacao"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def importacao():
    """
    Rota Default para /importacao
    """

    return {
        'message': 'OK',
        'env': 'importacao'
    }

@router.get("/categoria/", status_code=status.HTTP_200_OK)
def get_importacao_categoria(categoria: str):
    """
    Rota Importacao / dados por categoria
    """
    #Banco de Dados
    try:
        conn = sqlite3.connect('vitiVinicultura.db')
        cur = conn.cursor()
    except:
        print("Erro na conexão com o banco de dados")    
    
    control = 'NA'
    produto = 'NA'

    # Pegar o ID da Categoria
    ret = []
    goods_id = 0
    try:
        cur.execute(f"SELECT id FROM goods_imported_exported WHERE name='{categoria}'")
        rows = cur.fetchall()
        if len(rows) == 0:
            ret.append({
                'msg_goods': 'categoria nao encontrada'
            })
        else:
            for row in rows:
               goods_id = row[0]
    except:
        print("Erro na consulta goods_imported_exported")
    
    
    # Conslulta na tabela importacao
    try:
        cur.execute(f"SELECT id,countries,quantity_kg,value_usdolars,year,goods_id FROM importacao WHERE goods_id='{goods_id}'")
        rows = cur.fetchall()

        if len(rows) == 0:
            ret.append({
                'msg_importacao': 'nenhum item encontrado'
            })
        else:
            for row in rows:
                country = row[1]
                quantity_kg = row[2]
                value_usdolars = row[3]
                year = row[4]
                goods_id = row[5]
               
                ret.append({ 
                    'pais': country,
                    'quantity_kg' : quantity_kg,
                    'value_usdolars': value_usdolars,
                    'categoria': categoria,
                    'id_categoria': goods_id
                })

    except:
        print("Erro na consulta goods_imported_exported")    
    
    
    return ret
    