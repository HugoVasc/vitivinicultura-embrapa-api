
# Vitivinicultura Embrapa

API Pública para consulta de dados de produção, processamento, comercialização, importação e exportação de vitivinicultura da Embrapa.

## Colaboradores:

- Euclides Freire - RM357398
- Hugo Vasconcelos - RM358003
- Itiro - RM357371
- João Dias - RM357713

## Iniciar o App
```bash
#1.Clonar este repositório
git clone https://github.com/HugoVasc/vitivinicultura-embrapa-api

#2.Criar o virtual env
cd vitivinicultura-embrapa-api/
python3 -m venv venv
source venv/bin/activate

#3.Instalar os pré-requisitos
pip3 install -r requirements.txt

#4.Inicializar o fastapi
uvicorn app.main:app --reload --host 0.0.0.0
```

## Documentação da API

### Realiza o **SCRAP** dos dados da Embrapa, ETL e gravação no Banco de Dados

```http
  GET /scrape_and_save_data/scrape_and_save
```

### API para consulta aos dados de **PRODUCAO**

```http
  GET /producao
  GET /producao/categoria
  GET /producao/categoria/lista
  GET /producao/subcategoria
  GET /producao/subcategoria/lista
  GET /producao/subcategoria/tipo
```

### API para consulta aos dados de **PROCESSAMENTO**

```http
  GET /processamento
  GET /processamento/id_categoria/{category_id}
  GET /processamento/ano/{year}
  GET /processamento/id_categoria/{category_id}/ano/{year}
```

### API para consulta aos dados de **COMERCIALIZACAO**

```http
  GET /comercializacao
```

### API para consulta aos dados de **IMPORTACAO**

```http
  GET /importacao
```

### API para consulta aos dados de **EXPORTACAO**

```http
  GET /exportacao
```