from fastapi import FastAPI
from contextlib import asynccontextmanager
# functions
from datetime import date
# db
from sqlmodel import create_engine, SQLModel
from config import engine, create_db_and_tables, create_categories
# router
from routes.categoryRoutes import router as category_router
from routes.inventoryRoutes import router as inventory_router
from routes.purchaseRoutes import router as purchase_router
from routes.purchaseInventoryRoutes import router as purchase_inventory_router
from routes.saleRoutes import router as sale_router

def create_app():
    # configuración de startup y shutdown
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("inicio: Iniciando servidor")
        create_db_and_tables()
        create_categories()
        yield
        print("fin: Cerrando servidor")
    
    # configuración de fastapi
    app = FastAPI(lifespan=lifespan)
    
    # configuración del router
    app.include_router(category_router)
    app.include_router(inventory_router)
    app.include_router(purchase_router)
    app.include_router(purchase_inventory_router)
    app.include_router(sale_router)
        
    return app