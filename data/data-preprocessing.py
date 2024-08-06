#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Preprocessing producao, and comercializacao

# In[2]:


# Read the data from the CSV file, as one is needed because they follow the same format

raw_data_path = 'data/raw_data/'
producao_data = pd.read_csv(f'{raw_data_path}Producao.csv', sep=';')
producao_data.head()

# In[3]:


comercio_data = pd.read_csv(f'{raw_data_path}Comercio.csv', sep=';')
comercio_data.head()

# In[4]:


categories_producao = producao_data['control'][producao_data['control'].str.isupper()].reset_index(drop=True).values

categories_producao_df = pd.DataFrame(
    columns=['category'],
    data=categories_producao
)

# In[5]:


comercio_data.rename(columns={'Produto': 'produto'}, inplace=True)
comercio_data['control'] = comercio_data['control'].fillna(comercio_data['produto'])

# In[6]:


categories_comercio = comercio_data['control'][comercio_data['control'].str.isupper()].reset_index(drop=True).values

categories_comercio_df = pd.DataFrame(
    columns=['category'],
    data=categories_comercio
)

# In[7]:


category_df = pd.concat([categories_producao_df, categories_comercio_df], ignore_index=True)
category_df.drop_duplicates(inplace=True)
category_df.reset_index(drop=True, inplace=True)
category_df

# In[8]:


category_df['category_id'] = category_df.index

# In[9]:


category_df


# In[10]:


def categorize_data(producao_data):
    current_category = None
    categories = []

    # Itera sobre as linhas do DataFrame
    for index, row in producao_data.iterrows():
        if row['control'].isupper():
            # Atualiza a categoria atual
            current_category = row['control']
        categories.append(current_category)

    return categories


# In[11]:


def filter_data(producao_data, subcategory_column='produto'):
    filtered_data = producao_data[
        ~(producao_data['control'].str.isupper() & producao_data[subcategory_column].str.isupper())]
    return filtered_data


# In[12]:


def map_categories_to_ids(producao_data, category_df, category_column='category', id_column='category_id',
                          control_column='control'):
    category_to_id = dict(zip(category_df[category_column], category_df[id_column]))
    producao_data[control_column] = producao_data[control_column].map(category_to_id)
    return producao_data


def map_subcategories_to_ids(data, subcategories, subcategory_column='subcategory', id_column='subcategory_id'):
    subcategories_to_id = dict(zip(subcategories[subcategory_column], subcategories[id_column]))
    data.rename(columns={subcategory_column: id_column}, inplace=True)
    data[id_column] = data[id_column].map(subcategories_to_id)
    return data


# In[13]:


category_df

# In[14]:


only_categories_producao = producao_data[producao_data['control'].str.isupper()]
only_categories_producao.rename(columns={'control': 'category'}, inplace=True)
only_categories_producao.drop(columns=['id', 'produto'], inplace=True)
only_categories_producao = only_categories_producao.melt(id_vars=['category'], var_name='year', value_name='value')
only_categories_producao['year'] = only_categories_producao['year'].astype(int)

# In[15]:


only_categories_comercio = comercio_data[comercio_data['control'].str.isupper()]
only_categories_comercio.rename(columns={'control': 'category'}, inplace=True)
only_categories_comercio.drop(columns=['id', 'produto'], inplace=True)
only_categories_comercio = only_categories_comercio.melt(id_vars=['category'], var_name='year', value_name='value')
only_categories_comercio['year'] = only_categories_comercio['year'].astype(int)

# In[16]:


producao_data

# In[17]:


producao_data['control'] = categorize_data(producao_data)
producao_data = filter_data(producao_data)
producao_data = map_categories_to_ids(producao_data, category_df)
producao_data.rename(columns={'control': 'category_id'}, inplace=True)
producao_data.rename(columns={'produto': 'subcategory'}, inplace=True)
producao_data.drop(columns=['id'], inplace=True)
producao_data = producao_data.melt(id_vars=['category_id', 'subcategory'], var_name='year', value_name='value')
producao_data['year'] = producao_data['year'].astype(int)

# In[18]:


products_to_lowercase = ['VINHO FRIZANTE', 'VINHO ORGÂNICO', 'SUCO DE UVAS CONCENTRADO']


def fix_products_names(comercio_data):
    for product in products_to_lowercase:
        comercio_data['produto'] = comercio_data['produto'].str.replace(product, product.capitalize())
        comercio_data['produto'] = comercio_data['produto'].str.strip()
    return comercio_data


comercio_data = fix_products_names(comercio_data)

# In[18]:


# In[19]:


comercio_data

# In[20]:


comercio_data['control'] = categorize_data(comercio_data)
comercio_data = filter_data(comercio_data)
comercio_data = map_categories_to_ids(comercio_data, category_df)
comercio_data.rename(columns={'control': 'category_id'}, inplace=True)
comercio_data.rename(columns={'produto': 'subcategory'}, inplace=True)
comercio_data.drop(columns=['id'], inplace=True)
comercio_data = comercio_data.melt(id_vars=['category_id', 'subcategory'], var_name='year', value_name='value')
comercio_data['year'] = comercio_data['year'].astype(int)

# In[21]:


subcategories_producao = producao_data.loc[:, ['category_id', 'subcategory']].drop_duplicates().reset_index(drop=True)
subcategories_producao

# In[22]:


subcategories_comercio = comercio_data.loc[:, ['category_id', 'subcategory']].drop_duplicates().reset_index(drop=True)
subcategories_comercio

# In[23]:


# Merge the subcategories from both datasets
subcategories = pd.concat([subcategories_producao, subcategories_comercio], ignore_index=True)
subcategories.drop_duplicates(inplace=True)
subcategories.reset_index(drop=True, inplace=True)
subcategories['subcategory_id'] = subcategories.index
subcategories

# In[24]:


producao_data_subcategory = producao_data.drop(columns=['category_id'])
producao_data_subcategory = map_subcategories_to_ids(producao_data_subcategory, subcategories)

# In[25]:


comercio_data_subcategory = comercio_data.drop(columns=['category_id'])
comercio_data_subcategory = map_subcategories_to_ids(comercio_data_subcategory, subcategories)

# Preprocessing the processamento related datasets -> grape varieties

# In[26]:


# loading json file

import json

with open(f'{raw_data_path}opt_03_sub_buttons.json') as f:
    data = json.load(f)

# In[27]:


# creating a dataframe with the grape varieties
grape_varieties = [button['text'] for button in data['sub_buttons']]
grapes_varieties_df = pd.DataFrame(
    columns=['grapes_variety'],
    data=grape_varieties
)

# In[28]:


viniferas_table = pd.read_csv(f'{raw_data_path}ProcessaViniferas.csv', sep=';')
viniferas_table['variety_id'] = \
    grapes_varieties_df[grapes_varieties_df['grapes_variety'].str.contains('Viníferas')].index[0]
viniferas_table.head()

# In[29]:


viniferas_table['control'].replace('BRANCASEROSADAS', 'BRANCAS E ROSADAS', inplace=True)
viniferas_grape_categories_df = viniferas_table.loc[:, ['control', 'variety_id']][
    viniferas_table['control'].str.isupper()].reset_index(drop=True)

# In[30]:


americanas_table = pd.read_csv(f'{raw_data_path}ProcessaAmericanas.csv', sep='\\t', engine='python')
americanas_table['variety_id'] = \
    grapes_varieties_df[grapes_varieties_df['grapes_variety'].str.contains('Americanas')].index[0]
americanas_table.head()

# In[31]:


americanas_table['control'].replace('BRANCASEROSADAS', 'BRANCAS E ROSADAS', inplace=True)
americanas_table_categories_df = americanas_table.loc[:, ['control', 'variety_id']][
    americanas_table['control'].str.isupper()].reset_index(drop=True)

# In[32]:


mesa_table = pd.read_csv(f'{raw_data_path}ProcessaMesa.csv', sep='\\t', engine='python')
mesa_table['variety_id'] = grapes_varieties_df[grapes_varieties_df['grapes_variety'] == 'Uvas de mesa'].index[0]
mesa_table.head()

# In[33]:


mesa_table_categories_df = mesa_table.loc[:, ['control', 'variety_id']][
    mesa_table['control'].str.isupper()].reset_index(drop=True)

# In[34]:


sem_classed_table = pd.read_csv(f'{raw_data_path}ProcessaSemclass.csv', sep='\\t', engine='python')
sem_classed_table['variety_id'] = \
    grapes_varieties_df[grapes_varieties_df['grapes_variety'] == 'Sem classificação'].index[0]
sem_classed_table.head()

# In[35]:


sem_classed_table_categories_df = sem_classed_table.loc[:, ['control', 'variety_id']]

# In[36]:


grape_categories = pd.concat([viniferas_grape_categories_df, americanas_table_categories_df, mesa_table_categories_df,
                              sem_classed_table_categories_df], ignore_index=True)
grape_categories.rename(columns={'control': 'grapes_categories'}, inplace=True)
grape_categories.drop_duplicates(inplace=True)
grape_categories.reset_index(drop=True, inplace=True)
grape_categories

# In[37]:


viniferas_table

# In[38]:


viniferas_table['control'] = categorize_data(viniferas_table)
viniferas_table = filter_data(viniferas_table, subcategory_column='cultivar')
viniferas_table = map_categories_to_ids(viniferas_table, grape_categories, category_column='grapes_categories',
                                        control_column='control', id_column='variety_id')
viniferas_table.rename(columns={'control': 'category_id'}, inplace=True)
viniferas_table.rename(columns={'cultivar': 'subcategory'}, inplace=True)
viniferas_table.drop(columns=['id'], inplace=True)
viniferas_table = viniferas_table.melt(id_vars=['category_id', 'subcategory', 'variety_id'], var_name='year',
                                       value_name='value')
viniferas_table['year'].replace('2023an', '2023', inplace=True)
viniferas_table['year'] = viniferas_table['year'].astype(int)


# In[39]:


def treat_numbers(value):
    # Ensure the input is a string
    value = str(value)
    # Swap comma for dot
    value = value.replace(',', '.')
    # Remove spaces
    value = value.replace(' ', '')

    try:
        # Try converting to float
        return float(value)
    except ValueError:
        # Return original value if conversion fails
        return value


# In[40]:


def fill_values_with_nan(data):
    data['value'] = data['value'].apply(treat_numbers)
    data['value'] = pd.to_numeric(data['value'], errors='coerce')
    data.fillna(0, inplace=True)
    return data


# In[41]:


viniferas_table = fill_values_with_nan(viniferas_table)

# In[42]:


americanas_table['control'] = categorize_data(americanas_table)
americanas_table = filter_data(americanas_table, subcategory_column='cultivar')
americanas_table = map_categories_to_ids(americanas_table, grape_categories, category_column='grapes_categories',
                                         control_column='control', id_column='variety_id')
americanas_table.rename(columns={'control': 'category_id', 'cultivar': 'subcategory'}, inplace=True)
americanas_table.drop(columns=['id'], inplace=True)
americanas_table = americanas_table.melt(id_vars=['category_id', 'subcategory', 'variety_id'], var_name='year',
                                         value_name='value')
americanas_table['year'] = americanas_table['year'].astype(int)

# In[43]:


americanas_table = fill_values_with_nan(americanas_table)

# In[44]:


mesa_table['control'] = categorize_data(mesa_table)
mesa_table = filter_data(mesa_table, subcategory_column='cultivar')
mesa_table = map_categories_to_ids(mesa_table, grape_categories, category_column='grapes_categories',
                                   control_column='control', id_column='variety_id')
mesa_table.rename(columns={'control': 'category_id', 'cultivar': 'subcategory'}, inplace=True)
mesa_table.drop(columns=['id'], inplace=True)
mesa_table = mesa_table.melt(id_vars=['category_id', 'subcategory', 'variety_id'], var_name='year', value_name='value')
mesa_table['year'] = mesa_table['year'].astype(int)

# In[45]:


mesa_table = fill_values_with_nan(mesa_table)

# In[46]:


sem_classed_table.rename(columns={'control': 'category_id', 'cultivar': 'subcategory'}, inplace=True)
sem_classed_table.drop(columns=['id'], inplace=True)
sem_classed_table = sem_classed_table.melt(id_vars=['category_id', 'subcategory', 'variety_id'], var_name='year',
                                           value_name='value')
sem_classed_table['year'] = sem_classed_table['year'].astype(int)

# In[47]:


sem_classed_table

# In[48]:


sem_classed_table = fill_values_with_nan(sem_classed_table)

# In[49]:


processed_grapes = pd.concat([viniferas_table, americanas_table, mesa_table, sem_classed_table], ignore_index=True)
processed_grapes['year'] = processed_grapes['year'].astype(int)

# In[50]:


grape_subcategories = processed_grapes.loc[:, ['category_id', 'subcategory']].drop_duplicates().reset_index(drop=True)
grape_subcategories['subcategory_id'] = grape_subcategories.index

# In[51]:


processed_grapes = map_subcategories_to_ids(processed_grapes, grape_subcategories)

# Preprocessing imported and exported related datasets

# In[52]:


with open(f'{raw_data_path}opt_05_sub_buttons.json') as f:
    imported_goods = json.load(f)

with open(f'{raw_data_path}opt_06_sub_buttons.json') as f:
    exported_goods = json.load(f)

# In[53]:


imported_goods_varieties = [button['text'] for button in imported_goods['sub_buttons']]
imported_goods_varieties_df = pd.DataFrame(
    columns=['imported_goods'],
    data=imported_goods_varieties
)

# In[54]:


exported_goods_varieties = [button['text'] for button in exported_goods['sub_buttons']]
exported_goods_varieties_df = pd.DataFrame(
    columns=['exported_goods'],
    data=exported_goods_varieties
)

# In[55]:


all_goods = set(imported_goods_varieties).union(set(exported_goods_varieties))

# In[56]:


goods_varieties = pd.DataFrame(
    columns=['goods'],
    data=all_goods
)
goods_varieties['goods_id'] = goods_varieties.index
# Initialize the imported and exported columns with 0
goods_varieties['imported'] = 0
goods_varieties['exported'] = 0

# Set imported column to 1 for imported goods
for good in imported_goods_varieties_df['imported_goods']:
    goods_varieties.loc[goods_varieties['goods'] == good, 'imported'] = 1

# Set exported column to 1 for exported goods
for good in exported_goods_varieties_df['exported_goods']:
    goods_varieties.loc[goods_varieties['goods'] == good, 'exported'] = 1


# In[57]:


def process_wine_data(file_path, sep, goods_varieties, search_term, id_col, drop_cols, rename_map, imported=True):
    # Read the CSV file
    df = pd.read_csv(file_path, sep=sep)

    # Extract the goods_id based on the search term
    if imported:
        goods_id = \
            goods_varieties[goods_varieties['goods'].str.contains(search_term) & (goods_varieties['imported'] == 1)][
                'goods_id'].values[0]
    else:
        goods_id = \
            goods_varieties[goods_varieties['goods'].str.contains(search_term) & (goods_varieties['exported'] == 1)][
                'goods_id'].values[0]

    # Add the goods_id to the dataframe
    df[id_col] = goods_id

    # Drop the specified columns
    df.drop(columns=drop_cols, inplace=True)

    # Rename the specified columns
    df.rename(columns=rename_map, inplace=True)

    # Melt the dataframe
    df = df.melt(id_vars=[id_col, 'country'], var_name='year', value_name='value')

    # Fill missing values with NaN
    df = fill_values_with_nan(df)

    # Separate the year and the value type (kg or dollars)
    df['year'] = df['year'].astype(str)
    df['value_type'] = df['year'].apply(lambda x: 'quantity_in_kg' if '.' not in x else 'value_us_dollars')
    df['year'] = df['year'].apply(lambda x: x.split('.')[0])

    # Pivot the dataframe to have separate columns for 'quantity_in_kg' and 'value_us_dollars'
    df = df.pivot_table(index=[id_col, 'country', 'year'], columns='value_type', values='value',
                        aggfunc='first').reset_index()

    return df


# In[58]:


imported_wines = process_wine_data(f'{raw_data_path}ImpVinhos.csv', ';', goods_varieties, 'Vinhos', 'goods_id', ['Id'],
                                   {'País': 'country'})

# In[59]:


imported_suco = process_wine_data(f'{raw_data_path}ImpSuco.csv', ';', goods_varieties, 'Suco', 'goods_id', ['Id'],
                                  {'País': 'country'})

# In[60]:


imported_passas = process_wine_data(f'{raw_data_path}ImpPassas.csv', ';', goods_varieties, 'passas', 'goods_id', ['Id'],
                                    {'País': 'country'})

# In[61]:


imported_espumantes = process_wine_data(f'{raw_data_path}ImpEspumantes.csv', ';', goods_varieties, 'Espumantes', 'goods_id',
                                        ['Id'], {'País': 'country'})

# In[62]:


imported_goods = pd.concat([imported_wines, imported_suco, imported_passas, imported_espumantes], ignore_index=True)

# In[63]:


exported_wines = process_wine_data(f'{raw_data_path}ExpVinho.csv', ';', goods_varieties, 'Vinhos', 'goods_id', ['Id'],
                                   {'País': 'country'}, imported=False)

# In[64]:


exported_suco = process_wine_data(f'{raw_data_path}ExpSuco.csv', ';', goods_varieties, 'Suco', 'goods_id', ['Id'],
                                  {'País': 'country'}, imported=False)

# In[65]:


goods_varieties[goods_varieties['exported'] == 1]

# In[66]:


exported_frescas = process_wine_data(f'{raw_data_path}ExpUva.csv', ';', goods_varieties, 'frescas', 'goods_id', ['Id'],
                                     {'País': 'country'}, imported=False)

# In[67]:


exported_espumantes = process_wine_data(f'{raw_data_path}ExpEspumantes.csv', ';', goods_varieties, 'Espumantes', 'goods_id',
                                        ['Id'], {'País': 'country'}, imported=False)

# In[68]:


exported_goods = pd.concat([exported_wines, exported_suco, exported_frescas, exported_espumantes], ignore_index=True)

# In[ ]:


# create a directory named transformed_data
import os

transformed_data_path = 'data/transformed_data'
if not os.path.exists(transformed_data_path):
    os.makedirs(transformed_data_path)

# In[70]:


category_df.drop(columns=['category_id'], inplace=True)
category_df.to_csv(f'{transformed_data_path}/produced_commercialized_categories.csv', index=False)

# In[71]:


only_categories_producao.rename(columns={'value': 'quantity_in_l'}, inplace=True)
only_categories_producao.to_csv(f'{transformed_data_path}/produced_categories_with_quantity.csv', index=False)

# In[72]:


only_categories_comercio.rename(columns={'value': 'quantity_in_l'}, inplace=True)
only_categories_comercio.to_csv(f'{transformed_data_path}/commercialized_categories_with_quantity.csv', index=False)

# In[73]:


subcategories.drop(columns=['subcategory_id'], inplace=True)
subcategories.to_csv(f'{transformed_data_path}/produced_commercialized_subcategories.csv', index=False)

# In[74]:


producao_data_subcategory.rename(columns={'value': 'quantity_in_l'}, inplace=True)
producao_data_subcategory.to_csv(f'{transformed_data_path}/produced_subcategories_with_quantity.csv', index=False)

# In[75]:


producao_data_subcategory.rename(columns={'value': 'quantity_in_kg'}, inplace=True)
comercio_data_subcategory.to_csv(f'{transformed_data_path}/commercialized_subcategories_with_quantity.csv', index=False)

# In[76]:


grapes_varieties_df.to_csv(f'{transformed_data_path}/grape_varieties.csv', index=False)

# In[77]:


grape_categories.to_csv(f'{transformed_data_path}/grape_categories.csv', index=False)

# In[78]:


grape_subcategories.drop(columns=['subcategory_id'], inplace=True)
grape_subcategories.to_csv(f'{transformed_data_path}/grape_subcategories.csv', index=False)

# In[79]:


processed_grapes.rename(columns={'value': 'quantity_in_kg'}, inplace=True)
processed_grapes.to_csv(f'{transformed_data_path}/processed_grapes.csv', index=False)

# In[80]:


goods_varieties.drop(columns=['goods_id'], inplace=True)
goods_varieties.to_csv(f'{transformed_data_path}/goods_varieties.csv', index=False)

# In[81]:


imported_goods.to_csv(f'{transformed_data_path}/imported_goods.csv', index=False)

# In[82]:


exported_goods.to_csv(f'{transformed_data_path}/exported_goods.csv', index=False)
