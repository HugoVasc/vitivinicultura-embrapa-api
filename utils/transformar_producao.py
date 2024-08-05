import pandas as pd
import sqlite3

#Read the CSV file
df = pd.read_csv('../data/Producao.csv',sep=';')

#Banco de Dados
try:
    conn = sqlite3.connect('../vitiVinicultura.db')
except:
    print("Erro na conexão com o banco de dados")

#modificar as linhas com 'control' em letras maiusculas
newdf = df.mask(df['control'].str[0].str.isupper())

#remove todas as linhas com NaN
newdf = newdf.dropna()
#print(newdf)

for index, row in newdf.iterrows():
    #print(int(row['id']), row['control'], row['produto'])
    id = int(row['id'])
    control = row['control']
    produto = row['produto']
    conn.execute(f"INSERT INTO sub_categories (name, description) VALUES ('{control}','{produto}')")
    conn.commit()
    
    for ano in range(1970,2024):
        quantity_l = row[str(ano)]
        conn.execute(f"INSERT INTO sub_categories_with_quantity (subcategory_id, year, quantity_l) VALUES ({id},'{str(ano)}','{quantity_l}')")
        conn.commit()
        #print(f"{id} {ano} {quantity_l}")

#close DB connect 
conn.close()