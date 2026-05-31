from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from typing import List
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.database import get_db
from app.core.config import settings
from app.core.auth import get_current_admin
from app.core.limiter import limiter
from app.models.content import ContactMessage
from app.models.user import User
from app.schemas.schemas import ContactRequest, ContactOut

router = APIRouter(prefix="/api/contact", tags=["Contact"])


async def send_email_notification(name: str, email: str, subject: str, message: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[Portfolio] New message from {name}: {subject}"
        msg["From"]    = settings.SMTP_USER
        msg["To"]      = settings.CONTACT_RECEIVER

        html = f"""
        <html><body style="font-family:Inter,sans-serif;background:#0A1628;color:#E2EAF2;padding:2rem;">
          <div style="max-width:600px;margin:0 auto;background:#0D1E36;border:0.5px solid rgba(168,184,204,0.15);padding:2rem;">
            <h2 style="font-family:Georgia,serif;color:#7B9FBF;border-bottom:1px solid rgba(168,184,204,0.15);padding-bottom:1rem;">
              New Portfolio Contact
            </h2>
            <table style="width:100%;margin:1.5rem 0;">
              <tr><td style="color:#A8B8CC;width:80px;font-size:12px;text-transform:uppercase;letter-spacing:1px;padding:0.5rem 0;">Name</td>
                  <td style="color:#F4F7FB;font-weight:500;">{name}</td></tr>
              <tr><td style="color:#A8B8CC;font-size:12px;text-transform:uppercase;letter-spacing:1px;padding:0.5rem 0;">Email</td>
                  <td style="color:#F4F7FB;font-weight:500;">{email}</td></tr>
              <tr><td style="color:#A8B8CC;font-size:12px;text-transform:uppercase;letter-spacing:1px;padding:0.5rem 0;">Subject</td>
                  <td style="color:#F4F7FB;font-weight:500;">{subject}</td></tr>
            </table>
            <div style="background:#122444;border-left:3px solid #5B82A6;padding:1.25rem;margin-top:1rem;">
              <p style="font-size:12px;color:#A8B8CC;text-transform:uppercase;letter-spacing:1px;margin-bottom:0.75rem;">Message</p>
              <p style="color:#E2EAF2;line-height:1.8;">{message}</p>
            </div>
            <p style="margin-top:2rem;font-size:11px;color:#A8B8CC;text-align:center;">
              Mohd Azam Portfolio — aa3981863@gmail.com
            </p>
          </div>
        </body></html>
        """
        msg.attach(MIMEText(html, "html"))

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
    except Exception as e:
        print(f"[Email Error] {e}")


# ── PUBLIC — rate limited to 5/minute per IP ──────────────────
@router.post("/", status_code=201)
@limiter.limit("5/minute")
async def submit_contact(
    request: Request,
    data: ContactRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    msg = ContactMessage(
        name=data.name, email=data.email,
        subject=data.subject, message=data.message,
    )
    db.add(msg)
    db.commit()
    background_tasks.add_task(
        send_email_notification, data.name, data.email, data.subject, data.message
    )
    return {"message": "Message received! Mohd Azam will reply within 24 hours."}


# ── ADMIN ─────────────────────────────────────────────────────
@router.get("/", response_model=List[ContactOut])
def list_messages(db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    return db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).all()


@router.get("/unread-count")
def unread_count(db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    count = db.query(ContactMessage).filter(ContactMessage.is_read == False).count()
    return {"unread": count}


@router.patch("/{message_id}/read")
def mark_read(message_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    msg.is_read = True
    db.commit()
    return {"message": "Marked as read"}


@router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    msg = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(msg)
    db.commit()
    return {"message": "Deleted"}
