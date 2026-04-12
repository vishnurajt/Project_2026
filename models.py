from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    age: int
    is_active: bool
    bio: Optional[str] = None



class UsersListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    users: List[UserResponse]
    total: int
    

class Token(BaseModel):
    access_token: str
    token_type: str
