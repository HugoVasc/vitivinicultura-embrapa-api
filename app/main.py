import fastapi
from fastapi import HTTPException
from .models import Base
from scrapy.crawler import CrawlerProcess
from ..vitivinicultura_spider.vitivinicultura_spider.spiders.spider import (
    VitiviniculturaSpider,
)
from .database import engine

app = fastapi.FastAPI()

Base.metadata.create_all(bind=engine)


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
    