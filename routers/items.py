from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import db_models
from models import Item,ItemUpdate


router = APIRouter(prefix="/items", tags=["Item"])


# --- ITEM ROUTES ---
@router.post("/")
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = db_models.ItemDB(
        name=item.name,
        price=item.price,
        in_stock=item.in_stock,
        description=item.description
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Item created", "item": db_item}

@router.get("/")
def get_items(db: Session = Depends(get_db)):
    items = db.query(db_models.ItemDB).all()
    return {"items": items, "total": len(items)}

@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(db_models.ItemDB).filter(
        db_models.ItemDB.id == item_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}")
def update_item(item_id: int, item_data: ItemUpdate, db : Session = Depends(get_db)):
    item = db.query(db_models.ItemDB).filter(db_models.ItemDB.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return {"message": "Item updated", "item": item}

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(db_models.ItemDB).filter(
        db_models.ItemDB.id == item_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} deleted successfully"}

