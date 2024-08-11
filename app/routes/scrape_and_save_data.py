import os
import subprocess
from fastapi import APIRouter, HTTPException
from scrapy.crawler import CrawlerProcess
from vitivinicultura_spider.vitivinicultura_spider.spiders.spider import VitiviniculturaSpider
from app.load_data import load_data

router = APIRouter(
    prefix="/scrape_and_save_data",
    tags=["scrape_and_save_data"],
)


@router.post("/scrape_and_save")
async def scrape_and_save_data():
    """
    Rota para realizar o scrap, pré-processar e salvar os dados no banco de dados
    """
    try:
        # Scrape the data
        scrape_data()
        # Preprocess the data
        preprocess_data()
        # Load data into the database
        load_data()
        return {"message": "Todas as etapas foram finalizadas com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def scrape_data():
    """
    Função para realizar o scrap dos dados
    """
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "DEBUG",
    })
    process.crawl(VitiviniculturaSpider)
    process.start()


def preprocess_data():
    """
    Função para realizar a pré-processamento dos dados
    """
    try:
        current_dir = os.getcwd()
        print(f"Current working directory: {current_dir}")

        script_path = os.path.join(current_dir, 'data', 'data-preprocessing.py')

        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            check=True,
            cwd=current_dir  # Set the working directory to the current directory
        )
        print("Preprocessing output:", result.stdout)
        print("Preprocessing errors:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error output:", e.stderr)
        raise Exception(f"Erro no pré-processamento dos dados: {e.stderr}")
