from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import db_models
from routers import auth_router, users, items
from tasks import log_request_to_file
from starlette.background import BackgroundTask


# Create tables on startup
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- CORS MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LOGGING MIDDLEWARE ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"response status: {response.status_code}")
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"incoming request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"response status: {response.status_code}")
    
    # Log to file in background
    response.background = BackgroundTask(
        log_request_to_file,
        request.method,
        str(request.url),
        response.status_code
    )
    
    return response
# --- EXCEPTION HANDLERS ---
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

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": exc.detail
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

# --- ROUTERS ---
app.include_router(auth_router.router)
app.include_router(users.router)
app.include_router(items.router)