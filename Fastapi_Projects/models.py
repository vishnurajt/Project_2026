from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool
    description: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    age: int
    is_active: bool
    bio: Optional[str] = None

class UserUpdate(BaseModel):
    email : Optional[str] = None
    age : Optional[str] = None
    is_active : Optional[bool] = None
    bio: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
    description: Optional[str] = None