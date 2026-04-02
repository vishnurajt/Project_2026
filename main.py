from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session 
from sqlalchemy.exc import IntegrityError
from database import engine, get_db
import db_models
from models import ItemUpdate, User, Item, UserUpdate, UserResponse, UsersListResponse

# This creates the actual tables in the database on startup
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "error": "Validation failed",
            "details": exc.errors()
        }
    )
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong. Please try again."
        }
    )

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: User, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(db_models.UserDB).filter(
        db_models.UserDB.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    existing_email = db.query(db_models.UserDB).filter(
        db_models.UserDB.email == user.email).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = db_models.UserDB(
        username=user.username,
        email=user.email,
        age=user.age,
        password=user.password,
        is_active=user.is_active,
        bio=user.bio
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()  
        raise HTTPException(status_code=400, detail="User with this email or username already exists")
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(
        db_models.UserDB.id == user_id
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users", response_model=UsersListResponse)
def get_bool_users(is_active: bool = None, db: Session = Depends(get_db)):
    query = db.query(db_models.UserDB)
    
    if is_active is not None:
        query = query.filter(db_models.UserDB.is_active == is_active)
    
    users = query.all()
    return {"users": users, "total": len(users)}  


@app.put("/users/{user_id}",response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db : Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(db_models.UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_data.dict(exclude_unset=True)
    existing_email = db.query(db_models.UserDB).filter(
    db_models.UserDB.email == user_data.email,  # user_data = the request
    db_models.UserDB.id != user_id).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
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
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} deleted successfully"}

