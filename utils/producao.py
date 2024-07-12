import json

class Producao:

    # Construtor
    def __init__(self,id,arquivo,ano: int):
        self.id = id
        self.ano = ano
        self.arquivo = arquivo

    def __str__(self):
        return f'Categoria: {self.categoria}, Ano: {self.ano}, Arquivo: {self.arquivo}, Id: {self.id}'
    
    # Método para retornar as informações do ID com filtro por ano
    def listar_por_id_ano(self):
        """
        Rota Produção
        """
        print(f'Ano: {self.ano}, Id: {self.id}, Arquivo: {self.arquivo}')
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

# itiro = producao(2,'../data/producao.json',2023,'VINHO DE MESA')
# # print(itiro)
# teste = itiro.listar_por_id_ano()
# print(teste)