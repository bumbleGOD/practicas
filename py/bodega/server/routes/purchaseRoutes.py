from fastapi import APIRouter, HTTPException
from sqlmodel import select, Session
from pydantic import BaseModel
# models
from models.models import PurchaseProduct
from models.models import PurchaseInventoryProduct
from models.models import InventoryProduct
# config
from config import engine

router = APIRouter()

# read
@router.get('/api/purchase')
async def get_purchase():
    with Session(engine) as session:
        stmt = select(PurchaseProduct)
        results = session.exec(stmt).all()
        
        to_list = [result.to_dict() for result in results]
        
        return {"success": to_list}

# insert
class Add_purchase(BaseModel):
    product_code: str
    category_product: int
    name_product: str
    size_product: str
    quantity_product: int
    price_per_product: float
    
    class Config:
        orm_mode = True

@router.post('/api/purchase')
async def post_purchase(purchase: Add_purchase):
    with Session(engine) as session:
        new_purchase = PurchaseProduct(**purchase.model_dump())
        
        try:
            session.add(new_purchase)
            session.commit()
            
            product_in_inventory = select(InventoryProduct).where(
                InventoryProduct.product_code == new_purchase.product_code, 
                InventoryProduct.name_product == new_purchase.name_product, 
                InventoryProduct.size_product == new_purchase.size_product
            )
            result = session.exec(product_in_inventory).first()
            
            if result is None:
                new_product_in_inventory = InventoryProduct(
                    product_code=new_purchase.product_code, 
                    name_product=new_purchase.name_product, 
                    size_product=new_purchase.size_product, 
                    stock_product=new_purchase.quantity_product, 
                    purchase_price=new_purchase.price_per_product, 
                    category_product_id=new_purchase.category_product
                )
                session.add(new_product_in_inventory)
                session.commit()
                
                new_purchase_inventory = PurchaseInventoryProduct(
                    product_code=new_purchase.product_code, 
                    quantity_registered=new_purchase.quantity_product,
                    inventory_product_id=new_product_in_inventory.id,
                    purchase_product_id=new_purchase.id
                )
                session.add(new_purchase_inventory)
                session.commit()
            else:
                result.stock_product += new_purchase.quantity_product
                result.purchase_price = new_purchase.price_per_product
                session.commit()
                
                new_purchase_inventory = PurchaseInventoryProduct(
                    product_code=new_purchase.product_code, 
                    quantity_registered=new_purchase.quantity_product,
                    inventory_product_id=result.id,  
                    purchase_product_id=new_purchase.id
                )
                session.add(new_purchase_inventory)
                session.commit()

            return {"success": "Compra registrada", "purchase": new_purchase.to_dict()}
        
        except Exception as e:
            session.rollback()
            return {"error": f"Ocurrió un error {str(e)}"}

# update
@router.put('/api/purchase')
async def put_purchase():
    pass

# delete
@router.delete('/api/purchase')
async def delete_purchase():
    pass