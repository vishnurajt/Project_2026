from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
import db_models
from models import User, UserResponse, Token
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: User, db: Session = Depends(get_db)):
    if db.query(db_models.UserDB).filter(
        db_models.UserDB.username == user.username
    ).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(db_models.UserDB).filter(
        db_models.UserDB.email == user.email
    ).first():
        raise HTTPException(status_code=400, detail="Email already registered")
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
        raise HTTPException(status_code=400, detail="Registration failed")
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(db_models.UserDB).filter(
        db_models.UserDB.username == form_data.username
    ).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user