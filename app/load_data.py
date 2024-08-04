import os
import pandas as pd
from app.database import SessionLocal
from app.models import (
    WineCategories,
    WineSubCategories,
    ProducedWineCategoriesWithQuantity,
    ProducedWineSubCategoriesWithQuantity,
    ComercializedWineCategoriesWithQuantity,
    ComercializedWineSubCategoriesWithQuantity,
    GrapeVarieties,
    GrapeCategories,
    GrapeSubCategories,
    ProcessedGrapes,
    GoodsImportedExported,
    Importacao,
    Exportacao,
)

transformed_data_dir = os.path.join(os.path.dirname(__file__), '../data/transformed_data')

files_to_load = {
    'produced_commercialized_categories.csv': WineCategories,
    'produced_commercialized_subcategories.csv': WineSubCategories,
    'produced_categories_with_quantity.csv': ProducedWineCategoriesWithQuantity,
    'produced_subcategories_with_quantity.csv': ProducedWineSubCategoriesWithQuantity,
    'commercialized_categories_with_quantity.csv': ComercializedWineCategoriesWithQuantity,
    'commercialized_subcategories_with_quantity.csv': ComercializedWineSubCategoriesWithQuantity,
    'grape_varieties.csv': GrapeVarieties,
    'grape_categories.csv': GrapeCategories,
    'grape_subcategories.csv': GrapeSubCategories,
    'processed_grapes.csv': ProcessedGrapes,
    'goods_varieties.csv': GoodsImportedExported,
    'imported_goods.csv': Importacao,
    'exported_goods.csv': Exportacao,
}


def load_data():
    db = SessionLocal()
    try:
        for file, model in files_to_load.items():
            df = pd.read_csv(os.path.join(transformed_data_dir, file))
            df.index.name = 'id'  # Set the index name to 'id'
            df.reset_index(inplace=True)  # Move the index into a column
            df.to_sql(model.__tablename__, db.bind, if_exists='replace', index=False)
        print('Data loaded successfully')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    load_data()
