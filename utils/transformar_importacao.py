import pandas as pd
import sqlite3

def main():
    # Variáveis
    arquivoDB = '../vitiVinicultura.db'
    
    # Prepara a lista de arquivos para processamento
    arrayItens = []

    Item1 = { 
        'goods': 'vinhos de mesa',
        'goods_description': 'Importação e Exportação do item vinhos de mesa',
        'arquivoCSV' : '../data/ImpVinhos.csv'
    }
    arrayItens.append(Item1)

    Item2 = { 
        'goods': 'espumantes',
        'goods_description': 'Importação e Exportação do item espumante',
        'arquivoCSV' : '../data/ImpEspumantes.csv'
    }
    arrayItens.append(Item2)

    Item3 = { 
        'goods': 'uvas frescas',
        'goods_description': 'Importação e Exportação do item uvas frescas',
        'arquivoCSV' : '../data/ImpFrescas.csv'
    }
    arrayItens.append(Item3)

    Item4 = { 
        'goods': 'uvas passa',
        'goods_description': 'Importação e Exportação do item uvas pass',
        'arquivoCSV' : '../data/ImpPassas.csv'
    }
    arrayItens.append(Item4)

    Item5 = { 
        'goods': 'suco',
        'goods_description': 'Importação e Exportação do item suco',
        'arquivoCSV' : '../data/ImpSuco.csv'
    }
    arrayItens.append(Item5)

    # print(arrayItens)
    
    for item in arrayItens:
        print(f"{item['goods']} - {item['goods_description']} - {item['arquivoCSV']}")
        goods = item['goods']
        goods_description = item['goods_description']
        arquivoCSV = item['arquivoCSV']
        
        #Banco de Dados -> goods_imported_exported
        try:
            conn = sqlite3.connect(arquivoDB)
        except:
            print("Erro na conexão com o banco de dados")
    
        cur = conn.cursor()
        cur.execute(f"SELECT id,name,description FROM goods_imported_exported WHERE name='{goods}'")
        rows = cur.fetchall()
        # print(len(rows))
    
        if len(rows) == 0:
            try:
                conn.execute(f"INSERT INTO goods_imported_exported (name,description) VALUES ('{goods}','{goods_description}');")
                conn.commit()
                cur.execute(f"SELECT id,name,description FROM goods_imported_exported WHERE name='{goods}'")
                rows = cur.fetchall()
                goods_id = rows[0][0]
            except:
                print("Erro na inserção no banco de dados")
        else:
            print("Registro existente")
            goods_id = rows[0][0]
    
        print(goods_id)
        
        #Read the CSV file
        df = pd.read_csv(arquivoCSV,sep=';')
        df = df.fillna(0)
        print(df)
        
        for index, row in df.iterrows():
            # print(int(row['Id']), row['País'], row['1970'], row['1970'])
            country = row['País']
            quantity_kg = row['1970']
            
            for ano in range(1970,2024):
                quantity_kg = row[str(ano)]
                value_usdolars = row[str(ano) + '.1']
                print(country, ano, quantity_kg, value_usdolars)        
                # conn.execute(f"INSERT INTO sub_categories_with_quantity (sub_category_id, year, quantity_l) VALUES ({id},'{str(ano)}','{quantity_l}')")
                # conn.commit()
                #print(f"{id} {ano} {quantity_l}")
                conn.execute(f"INSERT INTO importacao (countries, quantity_kg, value_usdolars, year, goods_id) VALUES ('{country}',{quantity_kg},{value_usdolars},{ano},{goods_id})")
                conn.commit()
        
        # #close DB connect 
        conn.close()    
    
    
if __name__ == "__main__":
    main()