import fastapi
from fastapi import HTTPException
from scrapy.crawler import CrawlerProcess
from utils.scrap import VitiviniculturaSpider
from utils.producao_v2 import Producao

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
async def producao_id(id: int = 0):
    """
    Rota para informações sobre Produção. Filtro por id do item.
    """
    prod = Producao('data/Producao.csv')
    data = prod.get_id(id)
    return data

@app.get("/producao/ano")
async def producao_id_ano(id: int = 0,ano = 1970):
    """
    Rota para informações sobre Produção. Filtro por id do item e ano.
    """
    print(f'Id: {id}, Ano: {ano}')
    prod = Producao('data/Producao.csv')
    data = prod.get_id_ano(id,ano)
    return data
    
@app.get("/producao/categoria")
async def producao_soma_categoria(categoria: str = 'SUCO'):
    """
    Rota para informações sobre Produção. Soma por Categoria
    """
    print(f'Categoria: {categoria}')
    prod = Producao('data/Producao.csv')
    data = prod.get_soma_categoria(categoria)
    return data
    
@app.get("/producao/itens")
async def producao_itens_categoria(categoria: str = 'SUCO'):
    """
    Rota para informações sobre Produção. Items por Categoria
    """
    print(f'Categoria: {categoria}')
    prod = Producao('data/Producao.csv')
    data = prod.get_items_categoria(categoria)
    return data

@app.get("/producao/itens/ano/{ano}")
async def producao_itens_categoria_ano(categoria: str = 'SUCO',ano: int = 1970):
    """
    Rota para informações sobre Produção. Items por Categoria, filtro por ano
    """
    print(f'Categoria: {categoria}')
    prod = Producao('data/Producao.csv')
    data = prod.get_items_categoria_ano(categoria,ano)
    return data