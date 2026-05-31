"""
File Upload Router
Profile photo aur project images upload karne ke liye
"""
import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.core.auth import get_current_admin
from app.models.user import User

router = APIRouter(prefix="/api/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_MB = 5


def get_upload_dir(subfolder: str) -> str:
    path = os.path.join(UPLOAD_DIR, subfolder)
    os.makedirs(path, exist_ok=True)
    return path


@router.post("/photo")
async def upload_profile_photo(
    file: UploadFile = File(...),
    _: User = Depends(get_current_admin)
):
    """Profile photo upload — returns public URL."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WebP, GIF allowed")

    contents = await file.read()
    if len(contents) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_SIZE_MB}MB allowed")

    ext = file.filename.split(".")[-1].lower()
    filename = f"profile_{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(get_upload_dir("profile"), filename)

    with open(save_path, "wb") as f:
        f.write(contents)

    return {"url": f"/uploads/profile/{filename}", "filename": filename}


@router.post("/project-image")
async def upload_project_image(
    file: UploadFile = File(...),
    _: User = Depends(get_current_admin)
):
    """Project image upload — returns public URL."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WebP, GIF allowed")

    contents = await file.read()
    if len(contents) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_SIZE_MB}MB allowed")

    ext = file.filename.split(".")[-1].lower()
    filename = f"project_{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(get_upload_dir("projects"), filename)

    with open(save_path, "wb") as f:
        f.write(contents)

    return {"url": f"/uploads/projects/{filename}", "filename": filename}


@router.post("/blog-cover")
async def upload_blog_cover(
    file: UploadFile = File(...),
    _: User = Depends(get_current_admin)
):
    """Blog cover image upload — returns public URL."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, WebP, GIF allowed")

    contents = await file.read()
    if len(contents) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_SIZE_MB}MB allowed")

    ext = file.filename.split(".")[-1].lower()
    filename = f"blog_{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(get_upload_dir("blog"), filename)

    with open(save_path, "wb") as f:
        f.write(contents)

    return {"url": f"/uploads/blog/{filename}", "filename": filename}
