import json

class Producao:

    # Construtor
    def __init__(self,id: int,arquivo,ano: int,categoria: str):
        self.id = id
        self.ano = ano
        self.arquivo = arquivo
        self.categoria = categoria

    def __str__(self):
        return f'Categoria: {self.categoria}, Ano: {self.ano}, Arquivo: {self.arquivo}, Id: {self.id}'
    
    # Método para retornar as informações do ID com filtro por ano
    def listar_por_id_ano(self):
        """
        Rota Produção / ID
        """
        print(f'Rota Produção / ID -> Ano: {self.ano}, Id: {self.id}, Arquivo: {self.arquivo}')
        # Load the JSON file
        try:
            with open(self.arquivo, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f"Erro na leitura do arquivo. {e}")

        #iterate over data to find out the id
        ret_item = {}
        for item in data:
            if item['id'] == self.id:
                # print(item)
                ret_item = item
                # print(ret_item)
                if self.ano == 0:
                    ret_item = item
                    break
                else:
                    ret_item = item
                    anos = item['anos']
                    ret_item.pop('anos')
                    for a in anos:
                        for key in a:
                            if key == str(self.ano):
                                d = {}
                                d[key] = a[key]
                                # print(d)
                                ret_item['anos'] = []
                                ret_item['anos'].append(d)
                                break
                    break
                    
        return ret_item
        
    def soma_por_categoria(self,ano,categoria):
        """
        Rota Produção / Categoria
        """
        print(f'Rota Produção / Categoria -> Id: {self.id}, Ano: {ano}, Arquivo: {self.arquivo}, Categoria: {categoria}')
        # Load the JSON file
        try:
            with open(self.arquivo, 'r') as file:
                data = json.load(file)
        except Exception as e:
            print(f"Erro na leitura do arquivo. {e}")
            return 0
            
        #iterate over data to sum the annual values
        ret = {}
        soma = 0
        for item in data:
            if item['categoria'] == categoria:
                # print(f"Control: {item['control']}")
                for a in item['anos']:
                    for key in a:
                        if key == str(ano):
                            # print(a[key])
                            soma += a[key]
                            print(soma)
        
        # print(soma)
        ret['categoria'] = categoria
        ret['ano'] = ano
        ret['total'] = soma
        # print(ret)
        
        return ret
    





# itiro = Producao(2,'../data/producao.json',2023,'VINHO DE MESA')
# # print(itiro)
# # teste = itiro.listar_por_id_ano()
# teste = itiro.soma_por_categoria('VINHO DE MESA',2023)
# print(teste)