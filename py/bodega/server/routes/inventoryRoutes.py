from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from typing import Optional
# models
from models.models import InventoryProduct
# config
from config import engine

router = APIRouter()

# read
@router.get('/api/inventory')
async def get_inventory():
    with Session(engine) as session:
        stmt = select(InventoryProduct)
        exec = session.exec(stmt).all()
        
        result = [inventory.to_dict() for inventory in exec]
        
        return {"success": result}

# insert
class Add_inventory(BaseModel):
    product_code: str
    name_product: str
    description_product: Optional[str] = Field(None)
    size_product: str
    stock_product: Optional[int] = Field(None)
    purchase_price: float
    category_product_id: int
    
    class Config:
        orm_mode = True

@router.post('/api/inventory')
async def post_inventory(product: Add_inventory):
    with Session(engine) as session:
        stmt = select(InventoryProduct).where(
            InventoryProduct.product_code == product.product_code, 
            InventoryProduct.name_product == product.name_product, 
            InventoryProduct.size_product == product.size_product
        )
        product_exists = session.exec(stmt).first()
        
        if product_exists is None:
            new_product_in_inventory = InventoryProduct(**product.model_dump())
            
            try:
                session.add(new_product_in_inventory)
                session.commit()
                return {"success": "Producto insertado con éxito", "product": new_product_in_inventory.to_dict()}
            except Exception as e:
                session.rollback()
                raise HTTPException(status_code=500, detail=f"Ocurrió un error {str(e)}")                
        else:
            raise HTTPException(status_code=409, detail="El producto ya existe en el inventario")
        

# update
class Put_inventory(BaseModel):
    product_code: Optional[str] = Field(None)
    name_product: Optional[str] = Field(None)
    description_product: Optional[str] = Field(None)
    size_product: Optional[str] = Field(None)
    stock_product: Optional[int] = Field(None)
    purchase_price: Optional[float] = Field(None)
    category_product_id: Optional[int] = Field(None)
    
    class Config:
        orm_mode = True

@router.put('/api/inventory/{id_product}')
async def put_inventory(product: Put_inventory, id_product: str):
    with Session(engine) as session:
        stmt = select(InventoryProduct).where(InventoryProduct.id == id_product)
        product_to_update = session.exec(stmt).first()
        
        
        if product_to_update is None:
            raise HTTPException(status_code=404, detail="El producto seleccionado no existe en el inventario")
        
        product_data = product.model_dump()
        
        for field, value in product_data.items():
            setattr(product_to_update, field, value)
            
        try:
            session.add(product_to_update)
            session.commit()
            session.refresh(product_to_update)
            return {"success": "Producto actualizado", "product": product_to_update.to_dict()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocurrió un error {str(e)}")        
        
# delete
@router.delete('/api/inventory/{id_product}')
async def delete_inventory(id_product: str):
    with Session(engine) as session:
        stmt = select(InventoryProduct).where(InventoryProduct.id == id_product)
        product = session.exec(stmt).first()
        
        if product is None:
            raise HTTPException(status_code=404, detail="El producto seleccionado no existe en el inventario")
        
        try:
            session.delete(product)
            session.commit()
            return {"success": "Producto eliminado", "product": product.to_dict()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocurrió un error {str(e)}")   