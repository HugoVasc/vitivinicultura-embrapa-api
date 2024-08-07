import fastapi

from .database import engine
from .models import Base
from .routes import scrape_and_save_data, producao, comercializacao, processamento, exportacao, importacao

app = fastapi.FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """
    Rota default
    """
    return {"message": "Hello World"}


app.include_router(scrape_and_save_data.router)
app.include_router(producao.router)
app.include_router(comercializacao.router)
app.include_router(exportacao.router)
app.include_router(importacao.router)
app.include_router(processamento.router)
