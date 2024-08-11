import os
import pandas as pd
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import (
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
    db: Session = SessionLocal()
    try:
        for file, model in files_to_load.items():
            file_path = os.path.join(transformed_data_dir, file)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                # Drop rows with any null values
                df.dropna(inplace=True)
                df_records = df.to_dict(orient='records')

                for record in df_records:
                    db.add(model(**record))
                db.commit()
                print(f'Data from {file} loaded successfully into {model.__tablename__}.')
            else:
                print(f'File {file} does not exist.')
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    load_data()
