"""
Mohd Azam — Portfolio Backend
FastAPI + SQLAlchemy + JWT Auth + Rate Limiting + File Upload
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
import os

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.core.auth import hash_password
from app.core.limiter import limiter

# Register all models
from app.models import user, content  # noqa: F401

from app.routers import auth, projects, blog, contact
from app.routers.upload import router as upload_router

# ── Create tables ─────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── App init ──────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="""
## Mohd Azam Portfolio API

Full backend for personal portfolio website.

### Features
- 🔐 JWT Authentication (access + refresh tokens)
- 📁 Projects CRUD with image upload
- 📝 Blog posts CRUD with cover images
- 📧 Contact form with email notifications
- 🚦 Rate limiting on public endpoints
- 🗄️  SQLite (dev) / PostgreSQL (production)
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Rate limiter ───────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files (uploaded images) ────────────────────────────
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ── Routers ───────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(blog.router)
app.include_router(contact.router)
app.include_router(upload_router)


# ── Seed admin on first run ───────────────────────────────────
def seed_admin():
    from app.models.user import User
    db: Session = SessionLocal()
    try:
        exists = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not exists:
            admin = User(
                name=settings.ADMIN_NAME,
                email=settings.ADMIN_EMAIL,
                password=hash_password(settings.ADMIN_PASSWORD),
                is_admin=True,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print(f"✅ Admin created: {settings.ADMIN_EMAIL}")
        else:
            print(f"ℹ️  Admin exists: {settings.ADMIN_EMAIL}")
    finally:
        db.close()


seed_admin()


# ── Routes ────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "owner": "Mohd Azam",
        "email": "aa3981863@gmail.com",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
