from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool
    desceiption: Optional[str] = None

class User(BaseModel):
    username: str
    email: str
    age: int
    is_active: bool
    bio: Optional[str] = None