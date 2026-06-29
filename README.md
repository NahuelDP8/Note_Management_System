# Note Management System

A full-stack notes application with JWT authentication, note archiving, category filtering, and PostgreSQL-backed CI pipelines.

## Overview

This repository includes:

- `backend`: FastAPI + SQLAlchemy + Alembic
- `frontend`: React + TypeScript + Vite
- `ci`: benchmark tooling and CI comparison docs
- CI pipelines for GitHub Actions, GitLab CI/CD, and Bitbucket Pipelines

## Core Features

- User registration and login with JWT access tokens
- Private notes per authenticated user
- Create, update, archive, unarchive, and delete notes
- Category management and note filtering by categories
- Protected frontend routes (login required)

## Tech Stack

- Backend: Python 3.11+, FastAPI, SQLAlchemy, Alembic, Pydantic
- Frontend: React 19, TypeScript, Vite, Axios
- Database: PostgreSQL (recommended)
- CI/CD: GitHub Actions, GitLab CI/CD, Bitbucket Pipelines

## Project Structure

```text
.
|-- backend/
|   |-- app/
|   |-- alembic/
|   |-- requirements.txt
|-- frontend/
|   |-- src/
|   |-- package.json
|-- ci/
|   |-- benchmark/run_with_timer.sh
|   |-- BENCHMARK_GUIDE.md
|   |-- PIPELINE_COMPARISON.md
|-- .github/workflows/ci.yml
|-- .gitlab-ci.yml
|-- bitbucket-pipelines.yml
```

## Environment Variables

Backend settings are loaded from `backend/.env`.

Required variables:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/notes_db
SECRET_KEY=change-this-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:5173
```

Optional for tests:

```env
TEST_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/notes_test
```

## Local Development

### Option A: Conda (recommended)

From repository root:

```bash
conda env create -f environment.yml
conda activate notes-management-system
```

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend (new terminal):

```bash
cd frontend
corepack enable
pnpm install
pnpm run dev
```

### Option B: pip + venv

Backend:

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
corepack enable
pnpm install
pnpm run dev
```

## Database and Seed Data

The API runs `init_db()` on startup (`Base.metadata.create_all`).

To load demo data (demo user + default categories):

```bash
cd backend
python -m app.db.seed
```

Demo credentials created by seed:

- Email: `user@example.com`
- Password: `string`

## API Endpoints

Base URL:

- `http://127.0.0.1:8000/api/v1`

Main routes:

- `POST /auth/register`
- `POST /auth/login` (form-urlencoded)
- `GET /notes`
- `POST /notes`
- `PUT /notes/{note_id}`
- `PATCH /notes/{note_id}/archive`
- `PATCH /notes/{note_id}/unarchive`
- `DELETE /notes/{note_id}`
- `GET /categories`
- `POST /categories`

Docs:

- Swagger UI: `http://127.0.0.1:8000/docs`

## Frontend App

- Login page: `/`
- Protected notes page: `/notes`
- API client base URL comes from `VITE_API_BASE_URL`.

## Production Deployment

### Render

Use `render.yaml` from the repository root to create the backend web service and PostgreSQL database.

Required Render environment variables:

```env
DATABASE_URL=<provided by Render PostgreSQL>
SECRET_KEY=<strong-production-secret>
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:5173,https://<vercel-production-domain>,https://*.vercel.app
```

`DATABASE_URL` is wired from the Render database in `render.yaml`. Render may provide a `postgres://` or `postgresql://` URL; the backend normalizes it for the `psycopg` driver.

`CORS_ORIGINS` is comma-separated. Keep local development explicit with `http://localhost:5173`, add the production Vercel URL, and include `https://*.vercel.app` to allow Vercel preview deployments. Production and preview origins should use HTTPS to avoid mixed content issues.

### Vercel

Deploy the `frontend` directory as the Vercel project.

Required Vercel environment variable:

```env
VITE_API_BASE_URL=https://<render-backend-url>/api/v1
```

Set this variable in the Vercel dashboard for Production, Preview, and Development environments. The frontend does not fall back to localhost in production builds, so missing or non-HTTPS production values fail fast instead of shipping a broken deploy.

Vercel uses `frontend/vercel.json` to build with pnpm and route React Router pages such as `/notes` back to `index.html`. Requests under `/api/*` and static files are not rewritten.

### Frontend to Backend Flow

The browser calls the Render API directly using `VITE_API_BASE_URL`. FastAPI only accepts browser requests from origins listed in `CORS_ORIGINS`, including the production Vercel domain and Vercel preview URLs.

## Testing

From `backend/`:

```bash
pytest app/tests -q
```

If you use conda without activation:

```bash
conda run -n notes-management-system pytest app/tests -q
```

## CI/CD

Provider configs:

- GitHub Actions: `.github/workflows/ci.yml`
- GitLab CI/CD: `.gitlab-ci.yml`
- Bitbucket Pipelines: `bitbucket-pipelines.yml`

All three pipelines currently validate:

- Frontend: `pnpm install --frozen-lockfile`, lint, build
- Backend: dependency install + `pytest`
- PostgreSQL service for backend tests
- Benchmark timing output as CSV artifacts

CI benchmark docs:

- `ci/BENCHMARK_GUIDE.md`
- `ci/PIPELINE_COMPARISON.md`

## Useful Commands

Frontend:

```bash
cd frontend
pnpm run lint
pnpm run build
```

Backend:

```bash
cd backend
python -m pip install --upgrade pip
pytest app/tests -q
```

## Notes

- CORS is configured through `CORS_ORIGINS`.
- Production hardening should include strict secret management and migration-only schema changes.
