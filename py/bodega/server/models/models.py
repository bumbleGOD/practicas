from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, TEXT
from datetime import date
from typing import Optional
# functions
from functions.functions import create_id

# categories model
class CategoryProduct(SQLModel, table=True):
    __tablename__ = "categories_of_products"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name_category: str = Field(nullable=False)
    
    # relaciones
    inventory_product: list["InventoryProduct"] = Relationship(back_populates="category_product")
    
    # funcion constructora
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    # funcion para devolver un diccionario
    def to_dict(self):
        return {
            "id": self.id,
            "name_category": self.name_category
        }

# inventory model
class InventoryProduct(SQLModel, table=True):
    __tablename__ = "inventory_of_products"
    
    id: str = Field(primary_key=True, nullable=False, default_factory=lambda: create_id(), max_length=32)
    product_code: str = Field(nullable=False, max_length=7)
    name_product: str = Field(nullable=True)
    description_product: str = Field(sa_column=Column(TEXT, nullable=True))
    size_product: str = Field(nullable=False)
    stock_product: int = Field(nullable=False, default=0)
    purchase_price: float = Field(nullable=False)
    sale_of_price: Optional[float] = Field(nullable=True)
    inventory_added: date = Field(nullable=False, default_factory=date.today)
    
    # relaciones
    category_product_id: int = Field(foreign_key="categories_of_products.id")
    category_product: CategoryProduct = Relationship(back_populates="inventory_product")
   
    purchase_inventory_product: list["PurchaseInventoryProduct"] = Relationship(back_populates="inventory_product")
   
    sale_of_product: list["SaleOfProduct"] = Relationship(back_populates="inventory_product")
    
    # constructor de la clase
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calculate_sale_price()
    
    # calcular 25% de precio extra para venta
    def calculate_sale_price(self):
        self.sale_of_price = self.purchase_price * 1.25
        
    # funcion para devolver un diccionario
    def to_dict(self):
        return {
            "id": self.id,
            "product_code": self.product_code,
            "name_product": self.name_product,
            "description_product": self.description_product,
            "size_product": self.size_product,
            "stock_product": self.stock_product,
            "purchase_price": self.purchase_price,
            "sale_of_price": self.sale_of_price,
            "inventory_added": self.inventory_added,
            "category_product_id": self.category_product_id
        }
        
# purchases model    
class PurchaseProduct(SQLModel, table=True):
    __tablename__ = 'purchase_products'
    id: str = Field(primary_key=True, nullable=False, default_factory=lambda: create_id(), max_length=32)
    product_code: str = Field(nullable=False)
    category_product: int = Field(nullable=False)
    name_product: str = Field(nullable=False)
    size_product: str = Field(nullable=False)
    quantity_product: int = Field(nullable=False)
    price_per_product: float = Field(nullable=False)
    total_price: Optional[float] = Field(nullable=True)
    purchase_added: date = Field(default_factory=date.today, nullable=False)

    # relaciones
    purchase_inventory_product: list["PurchaseInventoryProduct"] = Relationship(back_populates="purchase_product")
        
    # calcular total de compra de productos
    def calculate_total_price(self):
        self.total_price = self.price_per_product * self.quantity_product
    
    # constructor de la clase    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calculate_total_price()
        
    # devolver como diccionario la info
    def to_dict(self):
        return {
            "id": self.id,
            "product_code": self.product_code,
            "name_product": self.name_product,
            "size_product": self.size_product,
            "quantity_product": self.quantity_product,
            "price_per_product": self.price_per_product,
            "total_price": self.total_price,
            "purchase_added": self.purchase_added
        }

# connection between purchase and inventory model        
class PurchaseInventoryProduct(SQLModel, table=True):
    __tablename__ = "purchase_inventory_products"
    
    id: str = Field(primary_key=True, nullable=False, default_factory=lambda: create_id(), max_length=32)
    product_code: str = Field(nullable=False)
    quantity_registered: int = Field(nullable=False)
    date_registered: date = Field(nullable=False, default_factory=date.today)
    
    # relaciones
    inventory_product_id: str = Field(foreign_key="inventory_of_products.id")
    inventory_product: InventoryProduct = Relationship(back_populates="purchase_inventory_product")
    
    purchase_product_id: str = Field(foreign_key="purchase_products.id")
    purchase_product: PurchaseProduct = Relationship(back_populates="purchase_inventory_product")
    
    # funcion constructora
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    # devuelve un diccionario
    def to_dict(self):
        return {
            "id": self.id,
            "product_code": self.product_code,
            "quantity_registered": self.quantity_registered,
            "date_registered": self.date_registered,
            "inventory_product_id": self.inventory_product_id,
            "purchase_product_id": self.purchase_product_id
        }

# sales model
class SaleOfProduct(SQLModel, table=True):
    __tablename__ = "sale_of_products"
    
    id: str = Field(primary_key=True, nullable=False, default_factory=lambda: create_id(), max_length=32)
    product_code: str = Field(nullable=False)
    name_product: str = Field(nullable=False)
    quantity_sold: int = Field(nullable=False, default=0)
    price_per_product: float = Field(nullable=False)
    total_price: Optional[float] = Field(nullable=True)
    date_sold: date = Field(nullable=False, default_factory=date.today)
    
    # relaciones
    inventory_product_id: str = Field(foreign_key="inventory_of_products.id")
    inventory_product: InventoryProduct = Relationship(back_populates="sale_of_product")
    
    # funcion constructora
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_price_sold()
        
    # funcion para calcular el precio total de la venta
    def total_price_sold(self):
        self.total_price = self.price_per_product * self.quantity_sold
    
    # devuelve un diccionario 
    def to_dict(self):
        return {
            "id": self.id,
            "product_code": self.product_code,
            "name_product": self.name_product,
            "quantity_sold": self.quantity_sold,
            "price_per_product": self.price_per_product,
            "total_price": self.total_price,
            "date_sold": self.date_sold,
            "inventory_product_id": self.inventory_product_id
        }