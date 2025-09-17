## DarkerDB Dashboard (Django + React)

Production-ready scaffold for a plug-and-go app integrating the Dark and Darker API.

### Stack
- Backend: Django 5, DRF, SimpleJWT, Postgres
- Frontend: React + Vite + React Router + Recharts
- DevOps: Docker + Docker Compose

### Quickstart
1) Create a `.env` file at the project root with:
```
POSTGRES_DB=darkerdb
POSTGRES_USER=darker
POSTGRES_PASSWORD=changeme
POSTGRES_PORT=5432

DJANGO_SECRET_KEY=unsafe-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
BACKEND_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

DARKERDB_API_BASE=https://api.darkerdb.com
DARKERDB_API_KEY=a946526942b378823b1b

FRONTEND_PORT=5173
BACKEND_PORT=8000
```
2) Build and run:
```
docker compose up -d --build
```
3) Open:
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/api/docs/

4) Create DB tables (first boot also runs migrations automatically via entrypoint):
```
docker compose exec backend python manage.py migrate
```

5) Create superuser (optional):
```
docker compose exec backend python manage.py createsuperuser
```

### Backend
- App: `backend/` (Django project name: `core`, app: `market`)
- Auth: JWT via `/api/token/` and `/api/token/refresh/`
- Endpoints (initial):
  - `GET /api/items/` (proxies DarkerDB `/v1/items`, upserts items)
  - `GET /api/items/{id}/market/` (proxies DarkerDB `/v1/market` for the item, stores price snapshots)
  - `GET /api/items/{id}/history/` (local price snapshots for charts)
  - `GET /api/dashboard/` (favorites + latest population snapshot)
  - `GET /api/leaderboard/?id=EA6_SHR` (proxies and caches leaderboard)
  - `GET /api/population/` (proxies and stores snapshot)
  - `POST /api/auth/register/` (create account)
  - `POST /api/auth/password-reset/` (console email demo)

Management commands:
```
docker compose exec backend python manage.py sync_market --item "Lightfoot Boots" --limit 50
docker compose exec backend python manage.py sync_population
docker compose exec backend python manage.py sync_leaderboard EA6_SHR
```

### Frontend
- App: `frontend/`
- Pages: Dashboard, Items list, Item detail, Leaderboard
- Dev server proxies `/api` to backend per `vite.config.js`

### Notes / Next
- Add user registration and password reset endpoints and UI
- Add favorites management in UI and price history charts with Recharts
- Add caching and background jobs (Celery/Redis) for scheduled syncs
 - Swap email backend to SMTP in production


"# darkermp" 
