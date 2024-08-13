from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class WineCategories(Base):
    __tablename__ = "wine_categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String, nullable=False)
    subcategories = relationship("WineSubCategories", back_populates="category")
    produced_wine = relationship("ProducedWineCategoriesWithQuantity", back_populates="category")
    comercialized_wine = relationship("ComercializedWineCategoriesWithQuantity", back_populates="category")


class WineSubCategories(Base):
    __tablename__ = "wine_sub_categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subcategory = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("wine_categories.id"))
    category = relationship("WineCategories", back_populates="subcategories")
    produced_wine = relationship("ProducedWineSubCategoriesWithQuantity", back_populates="subcategory")
    comercialized_wine = relationship("ComercializedWineSubCategoriesWithQuantity", back_populates="subcategory")


class ProducedWineCategoriesWithQuantity(Base):
    __tablename__ = "wine_categories_with_quantity"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("wine_categories.id"))
    year = Column(Integer, nullable=False)
    quantity_in_l = Column(Integer, nullable=False)
    category = relationship("WineCategories", back_populates="produced_wine")


class ProducedWineSubCategoriesWithQuantity(Base):
    __tablename__ = "wine_sub_categories_with_quantity"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subcategory_id = Column(Integer, ForeignKey("wine_sub_categories.id"))
    year = Column(Integer, nullable=False)
    quantity_in_l = Column(Integer, nullable=False)
    subcategory = relationship("WineSubCategories", back_populates="produced_wine")


class ComercializedWineCategoriesWithQuantity(Base):
    __tablename__ = "comercialized_wine_categories_with_quantity"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("wine_categories.id"))
    year = Column(Integer, nullable=False)
    quantity_in_l = Column(Integer, nullable=False)
    category = relationship("WineCategories", back_populates="comercialized_wine")


class ComercializedWineSubCategoriesWithQuantity(Base):
    __tablename__ = "comercialized_wine_sub_categories_with_quantity"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subcategory_id = Column(Integer, ForeignKey("wine_sub_categories.id"))
    year = Column(Integer, nullable=False)
    quantity_in_l = Column(Integer, nullable=False)
    subcategory = relationship("WineSubCategories", back_populates="comercialized_wine")


class GrapeVarieties(Base):
    __tablename__ = "grape_varieties"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    categories = relationship("GrapeCategories", back_populates="variety")


class GrapeCategories(Base):
    __tablename__ = "grape_categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    variety_id = Column(Integer, ForeignKey("grape_varieties.id"))
    variety = relationship("GrapeVarieties", back_populates="categories")
    subcategories = relationship("GrapeSubCategories", back_populates="category")


class GrapeSubCategories(Base):
    __tablename__ = "grape_sub_categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("grape_categories.id"))
    category = relationship("GrapeCategories", back_populates="subcategories")


class ProcessedGrapes(Base):
    __tablename__ = "processed_grapes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("grape_categories.id"))
    subcategory_id = Column(Integer, ForeignKey("grape_sub_categories.id"))
    variety_id = Column(Integer, ForeignKey("grape_varieties.id"))
    year = Column(Integer, nullable=False)
    quantity_in_kg = Column(Integer, nullable=False)
    category = relationship("GrapeCategories")
    subcategory = relationship("GrapeSubCategories")
    variety = relationship("GrapeVarieties")


class GoodsImportedExported(Base):
    __tablename__ = "goods_imported_exported"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    imported = Column(Boolean, nullable=False, default=False)
    exported = Column(Boolean, nullable=False, default=False)
    importacao = relationship("Importacao", back_populates="goods")
    exportacao = relationship("Exportacao", back_populates="goods")


class CommonColumnsImportExport(Base):
    __abstract__ = True  # This is an abstract base class
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    country = Column(String, nullable=False)
    quantity_in_kg = Column(Integer, nullable=False)
    value_us_dollars = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)
    goods_id = Column(Integer, ForeignKey("goods_imported_exported.id"))


class Importacao(CommonColumnsImportExport):
    __tablename__ = "importacao"
    # Additional columns specific to Importacao can be added here
    goods = relationship("GoodsImportedExported", back_populates="importacao")


class Exportacao(CommonColumnsImportExport):
    __tablename__ = "exportacao"
    # Additional columns specific to Exportacao can be added here
    goods = relationship("GoodsImportedExported", back_populates="exportacao")
