import fastapi
from fastapi import HTTPException
from scrapy.crawler import CrawlerProcess
from utils.scrap import VitiviniculturaSpider

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