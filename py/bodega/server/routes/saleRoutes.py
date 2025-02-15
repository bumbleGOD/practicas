from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlmodel import select, Session
# models
from models.models import SaleOfProduct
from models.models import InventoryProduct
# config
from config import engine

router = APIRouter()

# read
@router.get('/api/sale')
async def get_sale():
    with Session(engine) as session:
        stmt = select (SaleOfProduct)
        results = session.exec(stmt).all()
        
        to_list = [result.to_dict() for result in results]
        
        return {"success": to_list}

# insert
class Post_sale(BaseModel):
    quantity_sold: int
    inventory_product_id: str
    
    class Config:
        orm_mode = True

@router.post('/api/sale')
async def post_sale(sale: Post_sale):
    with Session(engine) as session:
        product_inventory = session.exec(select(InventoryProduct).where(InventoryProduct.id == sale.inventory_product_id)).first()
        
        if product_inventory is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        if product_inventory.stock_product < sale.quantity_sold:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        
        try:
            product_sale = SaleOfProduct(
                **sale.model_dump(),
                product_code=product_inventory.product_code,
                name_product=product_inventory.name_product, 
                price_per_product=product_inventory.sale_of_price
            )
            session.add(product_sale)
            product_inventory.stock_product -= sale.quantity_sold
            
            session.commit()
            session.refresh(product_inventory)
            return {"success": "Venta realizada", "product_inventory": product_inventory.to_dict(), "product_sold": product_sale.to_dict()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocurrió un error {str(e)}")

# update
@router.put('/api/sale')
async def put_sale():
    pass

# delete
@router.delete('/api/sale')
async def delete_sale():
    pass