# CRM System

Customer Relationship Management system built by Hermes Agent Multi-Agent Team.

## Stack
- **Backend**: FastAPI + SQLAlchemy async + SQLite
- **Frontend**: React 19 + TypeScript + Tailwind CSS + Vite
- **Deploy**: Docker Compose (Coolify-ready)

## Quick Start

```bash
# Clone & run
docker compose up -d

# Access
# - Frontend: http://localhost:5173
# - API Docs: http://localhost:8000/docs
# - Health:   http://localhost:8000/health
```

## Deploy on Coolify

1. Push this repo to GitHub/GitLab
2. In Coolify → New Resource → Docker Compose
3. Point to your repo
4. Set env vars from .env.example
5. Deploy!

## API Endpoints

| Group | Endpoints | Description |
|-------|-----------|-------------|
| Contacts | GET/POST/PUT/DELETE /api/v1/contacts | Customer management |
| Deals | GET/POST/PUT/DELETE/PATCH /api/v1/deals | Sales pipeline |
| Activities | GET/POST/PUT/DELETE /api/v1/activities | Activity logging |
| Pipelines | GET/POST/DELETE /api/v1/pipelines | Pipeline config |
| Users | GET/POST/PUT/DELETE /api/v1/users | User management |
| Stats | GET /api/v1/stats/summary | Dashboard KPIs |
