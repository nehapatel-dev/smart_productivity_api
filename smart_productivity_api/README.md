# Smart Productivity & Task Management API

A production-style RESTful backend built with **Django + DRF + JWT + PostgreSQL**, featuring secure authentication, task & category management, filtering, pagination, analytics, soft delete, activity logs and Swagger docs.

## ✨ Features

- 🔐 JWT Authentication (register, login, refresh, profile) with custom user model
- ✅ Full CRUD for **Tasks** and **Categories** (owner-scoped)
- 🔎 Search, filter (priority/status/category/due_date), ordering, pagination
- 📊 Analytics endpoint (total / completed / pending / overdue)
- ⏰ Reminders endpoint (tasks due in next 24h)
- 🗑️ Soft delete + activity logs
- 📚 Swagger (`/swagger/`) and ReDoc (`/redoc/`) documentation
- 🛡️ Uniform JSON error envelope, object-level permissions
- ⚙️ Env-driven config, CORS, WhiteNoise, Render-ready

## 🧱 Tech Stack

Python · Django 5 · DRF · SimpleJWT · django-filter · drf-yasg · django-cors-headers · PostgreSQL/SQLite · Gunicorn · WhiteNoise

## 📁 Project Structure

```
smart_productivity_api/
├── config/         # settings, urls, wsgi/asgi
├── users/          # custom user, auth (register/login/profile)
├── categories/     # category CRUD
├── tasks/          # task CRUD, filters, analytics, reminders, logs
├── utils/          # pagination + custom exception handler
├── permissions/    # IsOwner permission
├── services/       # business logic (analytics)
├── requirements.txt
├── manage.py
├── render.yaml     # Render deployment
├── build.sh
└── Procfile
```

## 🚀 Local Setup

```bash
# 1. Clone & enter
git clone <your-repo-url> smart_productivity_api
cd smart_productivity_api

# 2. Virtualenv
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Env
cp .env.example .env              # then edit values

# 5. Migrate & run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

App runs at `http://127.0.0.1:8000/`.
Docs: `http://127.0.0.1:8000/swagger/`

## 🔑 Authentication Flow

```http
POST /api/auth/register/
{ "username": "john", "email": "john@x.com", "password": "Strong#123", "password2": "Strong#123" }

POST /api/auth/login/
{ "username": "john", "password": "Strong#123" }
→ { "access": "...", "refresh": "..." }

# All protected requests:
Authorization: Bearer <access_token>
```

## 📌 Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Create user |
| POST | `/api/auth/login/` | Get JWT pair |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET/PUT | `/api/auth/profile/` | Current user profile |
| CRUD | `/api/categories/` | Categories (list/create/retrieve/update/delete) |
| CRUD | `/api/tasks/` | Tasks |
| GET | `/api/tasks/analytics/` | Counts: total, completed, pending, overdue |
| GET | `/api/tasks/reminders/` | Tasks due in next 24h |
| GET | `/api/tasks/logs/` | Activity logs |

### Filtering, Search, Ordering, Pagination

```
GET /api/tasks/?priority=high&status=pending&category=2
GET /api/tasks/?search=report
GET /api/tasks/?ordering=-due_date
GET /api/tasks/?page=2&page_size=20
```

### Sample Task Create

```json
POST /api/tasks/
{
  "title": "Write project report",
  "description": "Q4 summary",
  "priority": "high",
  "status": "pending",
  "due_date": "2026-06-01T17:00:00Z",
  "category": 1
}
```

### Sample Analytics Response

```json
{
  "total_tasks": 25,
  "completed_tasks": 15,
  "pending_tasks": 7,
  "in_progress_tasks": 3,
  "overdue_tasks": 3
}
```

## ⚠️ Error Format (uniform)

```json
{
  "success": false,
  "code": "validation_error",
  "message": "Validation failed.",
  "errors": { "title": ["This field is required."] },
  "status_code": 400
}
```

## ☁️ Deploy to Render

1. Push this repo to GitHub.
2. On [Render](https://render.com) → **New + → Blueprint** → select repo (uses `render.yaml`).
3. Render provisions a Postgres DB and deploys the web service.
4. Set `CORS_ALLOWED_ORIGINS` to your frontend URL in the dashboard.
5. Visit `https://<your-app>.onrender.com/swagger/`.

### Manual deploy (Railway / PythonAnywhere)

- Set env vars: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`, `CORS_ALLOWED_ORIGINS`.
- Build: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
- Start: `gunicorn config.wsgi:application`

## 🧪 Quick cURL Test

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"j@x.com","password":"Strong#123","password2":"Strong#123"}'

# Login
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"Strong#123"}' | python -c "import sys,json;print(json.load(sys.stdin)['access'])")

# Create task
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"Test","priority":"high","status":"pending"}'
```

## 📝 License

MIT — free to use, modify and deploy.
