from fastapi import APIRouter
from sqlmodel import select, Session
# models
from models.models import PurchaseInventoryProduct
# config
from config import engine

router = APIRouter()

# read
@router.get('/api/purchase_inventory')
async def get_purchase_inventory():
    with Session(engine) as session:
        stmt = select(PurchaseInventoryProduct)
        results = session.exec(stmt).all()
        
        to_list = [result.to_dict() for result in results]
        
        return {"success": to_list}

# insert
@router.post('/api/purchase_inventory')
async def post_purchase_inventory():
    pass

# update
@router.put('/api/purchase_inventory')
async def put_purchase_inventory():
    pass

# delete
@router.delete('/api/purchase_inventory')
async def delete_purchase_inventory():
    pass