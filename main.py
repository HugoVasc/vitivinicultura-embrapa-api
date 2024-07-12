import fastapi
from fastapi import HTTPException
from scrapy.crawler import CrawlerProcess
from utils.scrap import VitiviniculturaSpider
from utils.producao import Producao

app = fastapi.FastAPI()


@app.get("/")
async def root():
    """
    Rota default
    """
    return {"message": "Hello World"}

@app.get("/scrap")
async def scrap_data():
    """
    Rota para realizar o scrap dos dados
    """
    try:
        process = CrawlerProcess()
        process.crawl(VitiviniculturaSpider)
        process.start()
        return {"message": "Scrap finalizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
        
@app.get("/producao/id/{id}")
async def producao(id: int = 0, ano: int = 0):

    prod = Producao(id,'data/producao.json',ano)
    # print(itiro)
    data = prod.listar_por_id_ano()
    return data