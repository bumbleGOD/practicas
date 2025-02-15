from sqlmodel import SQLModel, create_engine, Session, select
# models
from models.models import CategoryProduct, InventoryProduct, PurchaseProduct, PurchaseInventoryProduct, SaleOfProduct

# configuración de base de datos
mysql_url = "mysql+pymysql://root:@localhost:3306/bodega"
engine = create_engine(mysql_url, echo=True)

# configuración del enrutador

# crear tablas de la db 
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
# crear categorias
def create_categories():
    categories_to_add = [
        {"id": 1, "name_category": "Camisetas"},
        {"id": 2, "name_category": "Camisas"},
        {"id": 3, "name_category": "Blusas"},
        {"id": 4, "name_category": "Chaquetas"},
        {"id": 5, "name_category": "Pantalones"},
        {"id": 6, "name_category": "Jeans"},
        {"id": 7, "name_category": "Shorts"},
        {"id": 8, "name_category": "Faldas"},
        {"id": 9, "name_category": "Zapatos"},
    ]
    
    with Session(engine) as session:
        stmt = session.exec(select(CategoryProduct.id)).all()
        to_list = set(stmt)
        
        to_insert = [CategoryProduct(**category) for category in categories_to_add if category["id"] not in to_list]
        
        if to_insert:
            session.add_all(to_insert)
            session.commit()
            print("categorias creadas")
        else:
            print("categorias ya existentes")