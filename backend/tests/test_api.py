"""
Mohd Azam Portfolio — Backend Tests
Run: pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.core.auth import hash_password
from app.models.user import User
from app.models.content import Project, BlogPost

# ── In-memory test database ───────────────────────────────────
TEST_DB_URL = "sqlite:///./test_portfolio.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    session = TestSession()
    yield session
    session.close()


@pytest.fixture
def admin_user(db):
    user = User(
        name="Mohd Azam",
        email="aa3981863@gmail.com",
        password=hash_password("TestPass@123"),
        is_admin=True,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_token(client, admin_user):
    res = client.post("/api/auth/login", json={
        "email": "aa3981863@gmail.com",
        "password": "TestPass@123"
    })
    return res.json()["access_token"]


@pytest.fixture
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


# ── HEALTH ────────────────────────────────────────────────────
class TestHealth:
    def test_root(self, client):
        res = client.get("/")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"
        assert res.json()["owner"] == "Mohd Azam"

    def test_health(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"


# ── AUTH ──────────────────────────────────────────────────────
class TestAuth:
    def test_login_success(self, client, admin_user):
        res = client.post("/api/auth/login", json={
            "email": "aa3981863@gmail.com",
            "password": "TestPass@123"
        })
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, admin_user):
        res = client.post("/api/auth/login", json={
            "email": "aa3981863@gmail.com",
            "password": "WrongPass"
        })
        assert res.status_code == 401

    def test_login_wrong_email(self, client):
        res = client.post("/api/auth/login", json={
            "email": "nobody@example.com",
            "password": "anything"
        })
        assert res.status_code == 401

    def test_get_me(self, client, auth_headers):
        res = client.get("/api/auth/me", headers=auth_headers)
        assert res.status_code == 200
        assert res.json()["email"] == "aa3981863@gmail.com"
        assert res.json()["is_admin"] is True

    def test_get_me_no_token(self, client):
        res = client.get("/api/auth/me")
        assert res.status_code == 401

    def test_refresh_token(self, client, admin_user):
        login_res = client.post("/api/auth/login", json={
            "email": "aa3981863@gmail.com", "password": "TestPass@123"
        })
        refresh_token = login_res.json()["refresh_token"]
        res = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
        assert res.status_code == 200
        assert "access_token" in res.json()

    def test_change_password(self, client, auth_headers):
        res = client.post("/api/auth/change-password", headers=auth_headers, json={
            "current_password": "TestPass@123",
            "new_password": "NewPass@456"
        })
        assert res.status_code == 200

    def test_change_password_wrong_current(self, client, auth_headers):
        res = client.post("/api/auth/change-password", headers=auth_headers, json={
            "current_password": "WrongOld",
            "new_password": "NewPass@456"
        })
        assert res.status_code == 400


# ── PROJECTS ──────────────────────────────────────────────────
class TestProjects:
    def test_list_projects_empty(self, client):
        res = client.get("/api/projects/")
        assert res.status_code == 200
        assert res.json() == []

    def test_create_project(self, client, auth_headers):
        res = client.post("/api/projects/", headers=auth_headers, json={
            "number": "01",
            "name": "DevFlow Dashboard",
            "description": "A real-time engineering metrics dashboard.",
            "stack": ["React", "Node", "Postgres"],
            "link": "https://github.com",
            "link_label": "GitHub",
            "featured": True,
            "is_active": True,
            "order": 1
        })
        assert res.status_code == 201
        assert res.json()["name"] == "DevFlow Dashboard"
        assert res.json()["featured"] is True

    def test_create_project_requires_admin(self, client):
        res = client.post("/api/projects/", json={
            "name": "Hacked Project", "description": "Not allowed", "stack": []
        })
        assert res.status_code == 401

    def test_get_project(self, client, auth_headers):
        create = client.post("/api/projects/", headers=auth_headers, json={
            "name": "Test Project", "description": "Test desc", "stack": ["Python"]
        })
        pid = create.json()["id"]
        res = client.get(f"/api/projects/{pid}")
        assert res.status_code == 200
        assert res.json()["name"] == "Test Project"

    def test_update_project(self, client, auth_headers):
        create = client.post("/api/projects/", headers=auth_headers, json={
            "name": "Old Name", "description": "Old desc", "stack": []
        })
        pid = create.json()["id"]
        res = client.put(f"/api/projects/{pid}", headers=auth_headers, json={
            "name": "New Name", "description": "New desc", "stack": ["Go"]
        })
        assert res.status_code == 200
        assert res.json()["name"] == "New Name"

    def test_delete_project(self, client, auth_headers):
        create = client.post("/api/projects/", headers=auth_headers, json={
            "name": "To Delete", "description": "bye", "stack": []
        })
        pid = create.json()["id"]
        res = client.delete(f"/api/projects/{pid}", headers=auth_headers)
        assert res.status_code == 200
        gone = client.get(f"/api/projects/{pid}")
        assert gone.status_code == 404


# ── BLOG ──────────────────────────────────────────────────────
class TestBlog:
    def test_list_posts_empty(self, client):
        res = client.get("/api/blog/")
        assert res.status_code == 200
        assert res.json() == []

    def test_create_post(self, client, auth_headers):
        res = client.post("/api/blog/", headers=auth_headers, json={
            "title": "Designing Good APIs",
            "excerpt": "A deep look at API design.",
            "content": "Full content here...",
            "category": "Engineering",
            "read_time": "8 min read",
            "slug": "designing-good-apis",
            "published": True
        })
        assert res.status_code == 201
        assert res.json()["slug"] == "designing-good-apis"

    def test_get_post_by_slug(self, client, auth_headers):
        client.post("/api/blog/", headers=auth_headers, json={
            "title": "Test Post", "excerpt": "Test", "content": "",
            "category": "Testing", "read_time": "1 min",
            "slug": "test-post", "published": True
        })
        res = client.get("/api/blog/test-post")
        assert res.status_code == 200
        assert res.json()["title"] == "Test Post"

    def test_duplicate_slug_rejected(self, client, auth_headers):
        payload = {"title": "P", "excerpt": "E", "content": "",
                   "category": "C", "read_time": "1 min", "slug": "same-slug", "published": False}
        client.post("/api/blog/", headers=auth_headers, json=payload)
        res = client.post("/api/blog/", headers=auth_headers, json=payload)
        assert res.status_code == 400

    def test_unpublished_not_in_public_list(self, client, auth_headers):
        client.post("/api/blog/", headers=auth_headers, json={
            "title": "Draft Post", "excerpt": "Draft", "content": "",
            "category": "Draft", "read_time": "2 min",
            "slug": "draft-post", "published": False
        })
        res = client.get("/api/blog/")
        posts = res.json()
        assert all(p["published"] for p in posts)


# ── CONTACT ───────────────────────────────────────────────────
class TestContact:
    def test_submit_contact(self, client):
        res = client.post("/api/contact/", json={
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Project Inquiry",
            "message": "Hello Mohd Azam, I have a project for you."
        })
        assert res.status_code == 201
        assert "message" in res.json()

    def test_submit_contact_invalid_email(self, client):
        res = client.post("/api/contact/", json={
            "name": "Test", "email": "not-an-email",
            "subject": "Test", "message": "Hello there, this is a test message."
        })
        assert res.status_code == 422

    def test_submit_contact_short_message(self, client):
        res = client.post("/api/contact/", json={
            "name": "Test", "email": "test@example.com",
            "subject": "Test", "message": "Hi"
        })
        assert res.status_code == 422

    def test_admin_list_messages(self, client, auth_headers):
        client.post("/api/contact/", json={
            "name": "Sender", "email": "sender@example.com",
            "subject": "Hello", "message": "This is a test message for admin listing."
        })
        res = client.get("/api/contact/", headers=auth_headers)
        assert res.status_code == 200
        assert len(res.json()) >= 1

    def test_mark_read(self, client, auth_headers):
        client.post("/api/contact/", json={
            "name": "A", "email": "a@example.com",
            "subject": "Sub", "message": "Long enough message here for testing."
        })
        msgs = client.get("/api/contact/", headers=auth_headers).json()
        mid = msgs[0]["id"]
        res = client.patch(f"/api/contact/{mid}/read", headers=auth_headers)
        assert res.status_code == 200

    def test_unread_count(self, client, auth_headers):
        res = client.get("/api/contact/unread-count", headers=auth_headers)
        assert res.status_code == 200
        assert "unread" in res.json()

    def test_delete_message(self, client, auth_headers):
        client.post("/api/contact/", json={
            "name": "Del", "email": "del@example.com",
            "subject": "Delete me", "message": "Please delete this test message."
        })
        msgs = client.get("/api/contact/", headers=auth_headers).json()
        mid = msgs[0]["id"]
        res = client.delete(f"/api/contact/{mid}", headers=auth_headers)
        assert res.status_code == 200
