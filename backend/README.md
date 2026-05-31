# Mohd Azam — Portfolio Backend
> FastAPI · SQLAlchemy · JWT Auth · SQLite/PostgreSQL · Email Notifications

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              ← FastAPI app entry point
│   ├── core/
│   │   ├── config.py        ← Environment settings
│   │   ├── database.py      ← SQLAlchemy engine & session
│   │   └── auth.py          ← JWT tokens & password hashing
│   ├── models/
│   │   ├── user.py          ← User model
│   │   └── content.py       ← Project, BlogPost, ContactMessage models
│   ├── schemas/
│   │   └── schemas.py       ← Pydantic request/response schemas
│   └── routers/
│       ├── auth.py          ← Login, refresh, me, change-password
│       ├── projects.py      ← CRUD for portfolio projects
│       ├── blog.py          ← CRUD for blog posts
│       └── contact.py       ← Contact form + email notification
├── tests/                   ← Add your tests here
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Setup

### 1. Clone & enter the backend folder
```bash
cd backend
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
# Edit .env with your values (secret key, email credentials, etc.)
```

### 5. Run the server
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be live at **http://localhost:8000**
Interactive docs at **http://localhost:8000/docs**

---

## 🔐 Authentication

The backend uses **JWT Bearer tokens**.

### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "aa3981863@gmail.com",
  "password": "ChangeMe@123"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

Use the access token in subsequent requests:
```http
Authorization: Bearer eyJ...
```

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/api/auth/login` | Public | Login with email + password |
| POST | `/api/auth/refresh` | Public | Get new access token |
| GET | `/api/auth/me` | Auth | Get current user info |
| POST | `/api/auth/change-password` | Auth | Change password |

### Projects
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/projects/` | Public | List active projects |
| GET | `/api/projects/{id}` | Public | Get single project |
| GET | `/api/projects/admin/all` | Admin | List all projects |
| POST | `/api/projects/` | Admin | Create project |
| PUT | `/api/projects/{id}` | Admin | Update project |
| DELETE | `/api/projects/{id}` | Admin | Delete project |

### Blog
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/blog/` | Public | List published posts |
| GET | `/api/blog/{slug}` | Public | Get post by slug |
| GET | `/api/blog/admin/all` | Admin | List all posts |
| POST | `/api/blog/` | Admin | Create post |
| PUT | `/api/blog/{id}` | Admin | Update post |
| DELETE | `/api/blog/{id}` | Admin | Delete post |

### Contact
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/api/contact/` | Public | Submit contact form (sends email) |
| GET | `/api/contact/` | Admin | List all messages |
| GET | `/api/contact/unread-count` | Admin | Count unread messages |
| PATCH | `/api/contact/{id}/read` | Admin | Mark message as read |
| DELETE | `/api/contact/{id}` | Admin | Delete message |

---

## 📧 Email Setup (Contact Form)

1. Go to your Google Account → Security → App Passwords
2. Generate an app password for "Mail"
3. Add to `.env`:
```
SMTP_USER=aa3981863@gmail.com
SMTP_PASSWORD=your-16-char-app-password
```

---

## 🗄️ Switch to PostgreSQL (Production)

In `.env`, replace:
```
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio_db
```

Install psycopg2:
```bash
pip install psycopg2-binary
```

---

## 🌐 Connect Frontend

In your `script.js`, update the base URL:
```javascript
const API_BASE = 'http://localhost:8000';

// Example: Fetch projects
const res = await fetch(`${API_BASE}/api/projects/`);
const projects = await res.json();
```

---

## 🔒 Security Checklist (Before Going Live)
- [ ] Change `SECRET_KEY` to a long random string
- [ ] Change `ADMIN_PASSWORD` to something strong
- [ ] Set `DEBUG=False`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set correct `FRONTEND_URL` for CORS
- [ ] Use environment variables, never commit `.env`
