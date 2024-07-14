import json
import pandas as pd

class Producao:

    # VINHO DE MESA = vm_
    # VINHO FINO DE MESA (VINIFERA) = vv_
    # SUCO = su
    # DERIVADOS = de_
    

    # Construtor
    def __init__(self,arquivo: str):
        self.arquivo = arquivo
        self.codigos = { "VINHO DE MESA":"vm_", "VINHO FINO DE MESA (VINIFERA)":"vv_", "SUCO":"su_", "DERIVADOS":"de_"}

    def __str__(self):
        return f'Arquivo: {self.arquivo}'
    
    # Método para retornar as informações do ID com todos os dados dos anos
    def get_id(self, id: int):
        """
        Rota Produção / Detalhes de um item (by ID)
        """
        # Load the JSON file
        try:
            df = pd.read_csv(self.arquivo,sep=';')
            # print(df)
            ds = df.loc[df['id']==id]
            ds_to_json = ds.to_json(orient="records")
            return ds_to_json
        except Exception as e:
            return f"Erro na leitura do arquivo. {e}"

    # Método para retornar as informações do ID com detalhes de um ano específico
    def get_id_ano(self, id: int, ano: int):
        """
        Rota Produção / Detalhes de um item (by ID e ano)
        """
        # Load the JSON file
        try:
            df = pd.read_csv(self.arquivo,sep=';')
            # print(df)
            ds = df.loc[df['id']==id,['id','control','produto',str(ano)]]
            ds_to_json = ds.to_json(orient="records")
            return ds_to_json
        except Exception as e:
            return f"Erro na leitura do arquivo. {e}"
    
    # Método para retornar as informações das categorias
    def get_soma_categoria(self, categoria: str):
        """
        Rota Produção / Soma por Categoria
        """
        # Load the JSON file
        try:
            df = pd.read_csv(self.arquivo,sep=';')
            # print(df)
            ds = df.loc[df['control']==categoria]
            ds_to_json = ds.to_json(orient="records")
            return ds_to_json
        except Exception as e:
            return f"Erro na leitura do arquivo. {e}"
            
    # Método que retorna todos os items por categoria
    def get_items_categoria(self, categoria: str):   
        """
        Rota Produção / Lista todos os itens por categoria
        """
        # Load the JSON file
        try:
            df = pd.read_csv(self.arquivo,sep=';')
            # print(df)
            ds = df.loc[df['control'].str.contains(self.codigos[categoria])]
            print(ds)
            ds_to_json = ds.to_json(orient="records")
            return ds_to_json
        except Exception as e:
            return f"Erro na leitura do arquivo. {e}"

    # Método que retorna todos os items por categoria
    def get_items_categoria_ano(self, categoria: str, ano: int):   
        """
        Rota Produção / Lista todos os itens por categoria filtro por ano
        """
        # Load the JSON file
        try:
            df = pd.read_csv(self.arquivo,sep=';')
            # print(df)
            ds = df.loc[df['control'].str.contains(self.codigos[categoria]),['id','control','produto',str(ano)]]
            
            print(ds)
            ds_to_json = ds.to_json(orient="records")
            return ds_to_json
        except Exception as e:
            return f"Erro na leitura do arquivo. {e}"



# itiro = Producao('../data/Producao.csv')
# # print(itiro)
# teste = itiro.get_categoria("SUCO")
# print(teste)
# teste1 = itiro.get_categoria_ano("SUCO",1970)
# print(teste1)
