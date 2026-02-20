from fastapi import FastAPI

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