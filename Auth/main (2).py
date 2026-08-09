# Auth Microservice

A standalone authentication microservice, extracted from the monolithic
Library Management System's `auth_system.py` and rebuilt as a real service:
bcrypt password hashing, JWT tokens, its own database, and a REST API that
other services (the library app, or anything else) can call instead of
sharing an in-memory `user_db` dict.

## Why a microservice instead of `auth_system.py`?

The original `auth_system.py` stored plain-text passwords in an in-memory
dict — fine for a classroom demo, not fine for anything real. This service:
- Hashes passwords with bcrypt (never stores plain text)
- Issues short-lived JWT access tokens instead of re-checking a password dict
- Persists users in a real database (SQLite by default, swappable via `DATABASE_URL`)
- Exposes a `/verify-token` endpoint so other services (e.g. the library CLI/GUI)
  can validate a token without needing direct DB access or duplicating JWT logic

## Run locally

```bash
cd auth_microservice
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Interactive API docs: http://localhost:8001/docs

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./auth.db` | DB connection string |
| `SECRET_KEY` | `dev-only-secret-change-me` | JWT signing key — **override in prod** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token lifetime |

## API

| Method | Path | Body | Description |
|---|---|---|---|
| GET | `/health` | — | Liveness check |
| POST | `/register` | `{username, email, password}` | Create a user |
| POST | `/login` | form: `username`, `password` | Returns `{access_token, token_type}` |
| GET | `/me` | Header: `Authorization: Bearer <token>` | Current user profile |
| POST | `/verify-token?token=...` | — | Validate a token (for other services) |

## Run tests

```bash
pytest tests/ -v
```

## Run with Docker (when you're ready to containerize)

```bash
docker build -t auth-microservice .
docker run -p 8001:8001 -e SECRET_KEY=change-me auth-microservice
```
