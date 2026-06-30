# Entry point of the FastAPI application
# Responsible for assembling the API by registering all routers
# Routers expose the HTTP layer and delegate business logic to services
import os

# CORS middleware setup (allowing frontend to communicate with backend)
from fastapi.middleware.cors import CORSMiddleware

# Load variables from .env file (like DATABASE_URL) before any other imports that might rely on them only in local)
if os.getenv("RENDER") is None:
    from dotenv import load_dotenv
    load_dotenv()


FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS", "")
FRONTEND_ORIGINS = [origin.strip() for origin in FRONTEND_ORIGINS.split(",") if origin]

from fastapi import FastAPI

# Import routers for each resource of the API
from app.api.routes import goals, tasks, focus_sessions, users, login, password_reset

# Import database models to ensure they are registered with SQLAlchemy before any database operations
import app.db.models

# Create the FastAPI application instance
app = FastAPI(
    title="Focus API",
    description="Backend API for managing learning, goals, tasks, and focus sessions.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers (modular route definitions)
app.include_router(goals.router)
app.include_router(tasks.router)
app.include_router(focus_sessions.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(password_reset.router)

# Basic health-check endpoint
@app.get("/")
def read_root():
    return {"status": "ok", "db": "connected", "version": "1.0.0"}