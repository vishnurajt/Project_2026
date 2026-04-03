# FastAPI Learning Project

A REST API built while learning FastAPI — covers database integration, authentication, error handling, and response models.

Built as part of a structured 8-week backend engineering comeback plan.

---

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM for database operations
- **SQLite** — local database (switches to PostgreSQL in production projects)
- **Pydantic v2** — request/response validation
- **python-jose** — JWT token creation and verification
- **passlib[bcrypt]** — password hashing
- **Uvicorn** — ASGI server

---

## Features

- Full CRUD for Users and Items
- JWT Authentication (register, login, protected routes)
- Password hashing with bcrypt — plain text never stored
- Response models — password field never exposed in responses
- Global error handling (400, 401, 404, 422, 500)
- Duplicate email and username checks
- Partial updates with `exclude_unset=True`
- Dynamic filtering — `GET /users?is_active=true`

---

## Project Structure
Fastapi_Projects/
├── main.py          # All endpoints
├── models.py        # Pydantic models (input/output/response)
├── db_models.py     # SQLAlchemy table definitions
├── database.py      # Engine, session, get_db dependency
├── auth.py          # JWT logic and get_current_user dependency
├── requirements.txt
└── .gitignore


---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Create account with hashed password |
| POST | `/login` | Returns JWT access token |
| GET | `/me` | Get logged-in user (protected) |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create user |
| GET | `/users` | List users, optional `?is_active=` filter (protected) |
| GET | `/users/{id}` | Get single user |
| PUT | `/users/{id}` | Partial update |
| DELETE | `/users/{id}` | Delete user |

### Items
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items` | Create item |
| GET | `/items` | List all items |
| GET | `/items/{id}` | Get single item |
| PUT | `/items/{id}` | Partial update |
| DELETE | `/items/{id}` | Delete item |

---

## Running Locally
```bash
# Clone the repo
git clone https://github.com/vishnurajt/Project_2026.git
cd your-repo-name

# Create virtual environment
python -m venv env
env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

## What I Learned

- How FastAPI handles dependency injection with `Depends()`
- SQLAlchemy ORM — models, sessions, queries, commits
- JWT flow — hashing passwords, creating tokens, protecting routes
- Pydantic response models — controlling what data gets exposed
- Proper HTTP error handling and status codes
- Git workflow — daily commits, `.gitignore`, clean history