
# Vitivinicultura Embrapa

API Pública para consulta de dados de produção, processamento, comercialização, importação e exportação de vitivinicultura da Embrapa.

## Colaboradores:

- Euclides Freire - RM357398
- Hugo Vasconcelos - RM358003
- Itiro - RM357371
- João Dias - RM357713
- Rodrigo Souza - RM357944

## Iniciar o App

'''
uvicorn app.main:app --reload --host 0.0.0.0
'''

## Documentação da API

### Realiza o scrap dos dados

```http
  GET /api/scrap
```
