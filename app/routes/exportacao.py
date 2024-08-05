from fastapi import APIRouter
from starlette import status
from ..database import SessionLocal

from ..models import Exportacao,GoodsImportedExported

router = APIRouter(
    prefix="/exportacao",
    tags=["exportacao"],
)

def format_response(result):
    response = {}
    country = ""
    countries = []
    country_id = 0
    category_name = ""
    category_description = ""

    response["categoria"] = result[0][1]
    response["descrição"] = result[0][2]
    response["countries"] = []
    
    for item in result:
        if item[3] == country:
            response["countries"][country_id-1]["anos"].append({
                    "ano": item[4],
                    "quantity": item[5],
                    "valor": item[6]
            })
        else:
            country = item[3]
            # print(f"Mudou de País {country}")
            response["countries"].append({
                "country_id": country_id,
                "nome": country,
                "anos": [{
                    "ano": item[4],
                    "quantity": item[5],
                    "valor": item[6]
                }]
            })
            country_id += 1
    
        if str(item[3]) not in countries:
            # print(f"Não Encontrado {str(item[3])}")
            countries.append(str(item[3]))
        # else:
        #     print(f"Encontrado {str(item[3])}")
    
    # print(f"{countries}")
    # print(response)

    return response

@router.get("/", status_code=status.HTTP_200_OK)
async def exportacao(category_id: int = 1):
    """
    Rota Default para /exportacao
    """
    try:
        result = SessionLocal().query(
            Exportacao
        ).with_entities(
            Exportacao.goods_id,
            GoodsImportedExported.name,
            GoodsImportedExported.description,
            Exportacao.countries,
            Exportacao.year,
            Exportacao.quantity_kg,
            Exportacao.value_usdolars,
            GoodsImportedExported.id,
            Exportacao.id
        ).join(
            GoodsImportedExported, Exportacao.goods_id == GoodsImportedExported.id
        ).filter(
            Exportacao.goods_id == str(category_id)
        )
        return format_response(result)
    except:    
        msg = "Categoria não encontrada"
        print(msg)
        return msg
    