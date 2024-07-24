import fastapi
from fastapi import HTTPException
from .routes import producao,comercializacao,processamento,exportacao,importacao
from .models import Base
from scrapy.crawler import CrawlerProcess
from vitivinicultura_spider.vitivinicultura_spider.spiders.spider import (
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
    
app.include_router(producao.router)
app.include_router(comercializacao.router)
app.include_router(exportacao.router)
app.include_router(importacao.router)
app.include_router(processamento.router)