from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
import db_models
from models import ItemUpdate, User, Item, UserUpdate

# This creates the actual tables in the database on startup
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ── USERS ──

@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(db_models.UserDB).filter(
        db_models.UserDB.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = db_models.UserDB(
        username=user.username,
        email=user.email,
        age=user.age,
        is_active=user.is_active,
        bio=user.bio
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created", "user": db_user}

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(
        db_models.UserDB.id == user_id
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ── ITEMS ──

@app.post("/items")
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

@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(db_models.ItemDB).all()
    return {"items": items, "total": len(items)}

@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(db_models.ItemDB).filter(
        db_models.ItemDB.id == item_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/users")
def get_bool_users(is_active: bool = None, db: Session = Depends(get_db)):
    query = db.query(db_models.UserDB)
    
    if is_active is not None:
        query = query.filter(db_models.UserDB.is_active == is_active)
    
    users = query.all()
    return {"users": users, "total": len(users)}  


@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: UserUpdate, db : Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(db_models.UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return {"message": "User updated", "user": user}


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(
        db_models.UserDB.id == user_id
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}


@app.put("/items/{item_id}")
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

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(db_models.ItemDB).filter(
        db_models.ItemDB.id == item_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} deleted successfully"}