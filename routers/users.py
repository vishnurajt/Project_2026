from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import db_models
from models import  UserResponse, UserUpdate, UsersListResponse
from auth import hash_password, get_current_user
from models import User, UserResponse, UserUpdate, UsersListResponse
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: User, db: Session = Depends(get_db)):
    if db.query(db_models.UserDB).filter(
        db_models.UserDB.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(db_models.UserDB).filter(
        db_models.UserDB.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = db_models.UserDB(
        username=user.username,
        email=user.email,
        age=user.age,
        password=hash_password(user.password),
        is_active=user.is_active,
        bio=user.bio
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user


@router.get("/", response_model=UsersListResponse)
def get_bool_users(is_active: bool = None, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    query = db.query(db_models.UserDB)
    
    if is_active is not None:
        query = query.filter(db_models.UserDB.is_active == is_active)
    
    users = query.all()
    return {"users": users,
     "total": len(users)}  

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(
        db_models.UserDB.id == user_id
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.put("/{user_id}",response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db : Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(db_models.UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_data.dict(exclude_unset=True)
    if "email" in update_data:
        existing_email = db.query(db_models.UserDB).filter(
            db_models.UserDB.email == update_data["email"],
            db_models.UserDB.id != user_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(
        db_models.UserDB.id == user_id
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}
