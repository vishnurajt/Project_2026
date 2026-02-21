from fastapi import FastAPI
from models import Item, User
from typing import Optional
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, I'm back!"}

@app.get("/about")
def about():
    return {"name": "Vishnuraj", "role": "Python Backend Engineer"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": f"Item number {item_id}"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

@app.get("/profile")
def profile():
    return {
        "name": "Vishnuraj T",
        "city": "Tirur, Kerala",
        "skills": ["Python", "FastAPI", "Flask", "PostgreSQL", "Docker"],
        "years_of_experience": 3
    }


item_db = []
users_db = []

@app.post("/items")
def create_item(item: Item):
    item_db.append(item)
    return {"message": "Item created succesfully", "item": item }

@app.get("/items")
def get_items():
    return {"items": item_db}

@app.post("/items/validate")
def validate_item(item: Item):
    if item.price <= 0:
        return {"error": "price must be greater than zero"}
    if len(item.name) < 3:
        return {"error": "name must be atleast 3 characters long"}
    return {"Valid": True, "item": item}


@app.post("/users")
def create_user(user: User):
    users_db.append(user.dict())
    return {"message": "User created successfully", "user": user}

@app.get("/users")
def get_users():
    return {"users": users_db, "count": len(users_db)}