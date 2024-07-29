from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class WineCategories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class WineSubCategories(Base):
    __tablename__ = "sub_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))


class ProducedWineCategoriesWithQuantity(Base):
    __tablename__ = "categories_with_quantity"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    year = Column(Integer, nullable=False)
    quantity_l = Column(Integer, nullable=False)


class ProducedWineSubCategoriesWithQuantity(Base):
    __tablename__ = "sub_categories_with_quantity"
    id = Column(Integer, primary_key=True, index=True)
    subcategory_id = Column(Integer, ForeignKey("sub_categories.id"))
    year = Column(Integer, nullable=False)
    quantity_l = Column(Integer, nullable=False)


class ComercializedWineCategoriesWithQuantity(Base):
    __tablename__ = "comercialized_categories_with_quantity"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    year = Column(Integer, nullable=False)
    quantity_l = Column(Integer, nullable=False)


class ComercializedWineSubCategoriesWithQuantity(Base):
    __tablename__ = "comercialized_sub_categories_with_quantity"
    id = Column(Integer, primary_key=True, index=True)
    subcategory_id = Column(Integer, ForeignKey("sub_categories.id"))
    year = Column(Integer, nullable=False)
    quantity_l = Column(Integer, nullable=False)


class GrapeVarieties(Base):
    __tablename__ = "grape_varieties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class GrapeCategories(Base):
    __tablename__ = "grape_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    variety_id = Column(Integer, ForeignKey("grape_varieties.id"))
    description = Column(String, nullable=False)


class GrapeSubCategories(Base):
    __tablename__ = "grape_sub_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("grape_categories.id"))


class ProcessedGrapes(Base):
    __tablename__ = "processed_grapes"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("grape_categories.id"))
    subcategory_id = Column(Integer, ForeignKey("grape_sub_categories.id"))
    year = Column(Integer, nullable=False)
    quantity_kg = Column(Integer, nullable=False)


class GoodsImportedExported(Base):
    __tablename__ = "goods_imported_exported"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class CommonColumnsImportExport(Base):
    __abstract__ = True  # This is an abstract base class
    id = Column(Integer, primary_key=True, index=True)
    countries = Column(String, nullable=False)
    quantity_kg = Column(Integer, nullable=False)
    value_usdolars = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)
    goods_id = Column(Integer, ForeignKey("goods_imported_exported.id"))


class Importacao(CommonColumnsImportExport):
    __tablename__ = "importacao"
    # Additional columns specific to Importacao can be added here


class Exportacao(CommonColumnsImportExport):
    __tablename__ = "exportacao"
    # Additional columns specific to Exportacao can be added here
