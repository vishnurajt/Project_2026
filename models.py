from pydantic import BaseModel
from typing import Optional, List

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool
    description: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    age: int
    password: str
    is_active: bool
    bio: Optional[str] = None

class UserUpdate(BaseModel):
    email : Optional[str] = None
    age : Optional[int] = None
    is_active : Optional[bool] = None
    bio: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
    description: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: int
    is_active: bool
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class UsersListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
