from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import engine, Base
from routers import auth, students, users
import models  # noqa: F401 – ensures models are registered before create_all


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables and seed initial data on startup
    Base.metadata.create_all(bind=engine)
    from seed import seed_data
    seed_data()
    yield


app = FastAPI(
    title="Student Management API",
    description="JWT-authenticated, role-based student management system",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/auth",     tags=["Auth"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(users.router,    prefix="/api/users",    tags=["Users"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Student Management API is running 🚀"}
