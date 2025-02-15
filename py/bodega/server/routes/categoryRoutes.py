from fastapi import APIRouter, HTTPException
from sqlmodel import select, Session
from pydantic import BaseModel
# models
from models.models import CategoryProduct
# config
from config import engine

router = APIRouter()

# read
@router.get('/api/category')
async def get_category():
    with Session(engine) as session:
        stmt = select(CategoryProduct)
        exec = session.exec(stmt).all()
        
        result = [category.to_dict() for category in exec]

        return {"successs": result}
    
# insert
class Add_category(BaseModel):
        name_category: str
        
        class Config:
            orm_mode = True

@router.post('/api/category')
async def post_category(category: Add_category):
    with Session(engine) as session:
        new_category = CategoryProduct(name_category=category.name_category)
        
        try:
            session.add(new_category)
            session.commit()
            return {"success": "Categoria creada", "category": new_category.to_dict()}
        except Exception as e:
            session.rollback()
            return {"error": f"Ocurrio un error {str(e)}"}

# update
@router.put('/api/category/{id_category}/{new_name_category}')
async def put_category(id_category: int, new_name_category: str):
    with Session(engine) as session:
        stmt = select(CategoryProduct).where(CategoryProduct.id == id_category)
        category = session.exec(stmt).first()
        
        if not category:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        
        try:
            category.name_category = new_name_category
            session.commit()
            session.refresh(category)
            return {"success": "Categoria actualizada", "category": category.to_dict()}
        except Exception as e:
            session.rollback()
            return {"error": f"Ocurrio un error {str(e)}"}

# delete
@router.delete('/api/category/{id_category}')
async def delete_category(id_category: int):
    with Session(engine) as session:
        stmt = select(CategoryProduct).where(CategoryProduct.id == id_category)
        category = session.exec(stmt).first()
        
        if not category:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        
        try:
            session.delete(category)
            session.commit()
            return {"success": "Categoria eliminada", "category": category}
        except Exception as e:
            session.rollback()
            return {"error": f"Ocurrio un error {str(e)}"}