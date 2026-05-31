from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from datetime import datetime
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id          = Column(Integer, primary_key=True, index=True)
    number      = Column(String(5))
    name        = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    stack       = Column(JSON, default=list)   # list of tag strings
    link        = Column(String(500), default="#")
    link_label  = Column(String(50), default="View Project")
    featured    = Column(Boolean, default=False)
    is_active   = Column(Boolean, default=True)
    order       = Column(Integer, default=0)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(300), nullable=False)
    excerpt     = Column(Text, nullable=False)
    content     = Column(Text, default="")
    category    = Column(String(100), default="Engineering")
    read_time   = Column(String(20), default="5 min read")
    slug        = Column(String(300), unique=True, index=True)
    published   = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(255), nullable=False)
    subject    = Column(String(300), nullable=False)
    message    = Column(Text, nullable=False)
    is_read    = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
