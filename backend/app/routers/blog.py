from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_admin
from app.models.content import BlogPost
from app.models.user import User
from app.schemas.schemas import BlogCreate, BlogUpdate, BlogOut

router = APIRouter(prefix="/api/blog", tags=["Blog"])


# ── PUBLIC ────────────────────────────────────────────────────
@router.get("/", response_model=List[BlogOut])
def list_posts(db: Session = Depends(get_db)):
    """Return all published blog posts, newest first."""
    return db.query(BlogPost).filter(BlogPost.published == True).order_by(BlogPost.created_at.desc()).all()


@router.get("/{slug}", response_model=BlogOut)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(BlogPost).filter(BlogPost.slug == slug, BlogPost.published == True).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


# ── ADMIN ─────────────────────────────────────────────────────
@router.get("/admin/all", response_model=List[BlogOut])
def admin_list_posts(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    return db.query(BlogPost).order_by(BlogPost.created_at.desc()).all()


@router.post("/", response_model=BlogOut, status_code=201)
def create_post(
    data: BlogCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    existing = db.query(BlogPost).filter(BlogPost.slug == data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="A post with this slug already exists")
    post = BlogPost(**data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=BlogOut)
def update_post(
    post_id: int,
    data: BlogUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin)
):
    post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
