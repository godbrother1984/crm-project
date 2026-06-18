# CRM API — Design Document

## Tech Stack
- **Framework**: FastAPI (async Python)
- **Database**: PostgreSQL 16 with SQLAlchemy 2.0 async
- **Migrations**: Alembic
- **Container**: Docker + docker-compose
- **Testing**: pytest + httpx (async test client)

## API Endpoints

### Contacts (`/api/v1/contacts`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/contacts` | List contacts (paginated, searchable, sortable) |
| POST | `/api/v1/contacts` | Create a contact |
| GET | `/api/v1/contacts/{id}` | Get contact by ID |
| PUT | `/api/v1/contacts/{id}` | Update contact (partial) |
| DELETE | `/api/v1/contacts/{id}` | Delete contact |

### Deals (`/api/v1/deals`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/deals` | List deals (filterable by stage, contact, assignee) |
| POST | `/api/v1/deals` | Create a deal |
| GET | `/api/v1/deals/{id}` | Get deal by ID |
| PUT | `/api/v1/deals/{id}` | Update deal |
| PATCH | `/api/v1/deals/{id}/stage` | Move deal to a different stage |
| DELETE | `/api/v1/deals/{id}` | Delete deal |

### Activities (`/api/v1/activities`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/activities` | List activities (filterable by contact, deal, type, done) |
| POST | `/api/v1/activities` | Create an activity |
| GET | `/api/v1/activities/{id}` | Get activity by ID |
| PUT | `/api/v1/activities/{id}` | Update activity |
| DELETE | `/api/v1/activities/{id}` | Delete activity |

### Pipelines (`/api/v1/pipelines`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/pipelines` | List all pipelines with their stages |
| POST | `/api/v1/pipelines` | Create a pipeline (with optional stages) |
| GET | `/api/v1/pipelines/{id}` | Get pipeline with stages |
| POST | `/api/v1/pipelines/{id}/stages` | Add stage to pipeline |
| DELETE | `/api/v1/pipelines/{id}` | Delete pipeline |

### Users (`/api/v1/users`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/users` | List users |
| POST | `/api/v1/users` | Create a user |
| GET | `/api/v1/users/{id}` | Get user by ID |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |

### Stats (`/api/v1/stats`)
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/stats/summary` | Dashboard summary (counts, pipeline value, pending activities) |

### System
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |

## Database Schema

### contacts
- `id` (UUID, PK)
- `first_name`, `last_name` (varchar, required)
- `email` (varchar, unique)
- `phone`, `company`, `job_title`, `source`, `notes`
- `lifetime_value` (float)
- `created_at`, `updated_at` (timestamptz)

### deals
- `id` (UUID, PK)
- `title`, `description`
- `value` (float), `currency` (varchar)
- `stage_id` → pipeline_stages.id
- `contact_id` → contacts.id
- `assigned_to` → users.id
- `probability` (float 0–100)
- `closed_at`, `created_at`, `updated_at`

### pipeline_stages
- `id` (UUID, PK)
- `pipeline_id` → pipelines.id
- `name`, `order`, `probability`, `color`

### pipelines
- `id` (UUID, PK)
- `name` (unique), `description`
- `created_at`, `updated_at`

### activities
- `id` (UUID, PK)
- `activity_type` (enum: note/call/email/meeting/task)
- `subject`, `description`
- `contact_id` → contacts.id (optional)
- `deal_id` → deals.id (optional)
- `done`, `due_at`, `done_at`
- `created_at`, `updated_at`

### users
- `id` (UUID, PK)
- `email` (unique)
- `display_name`, `role` (admin/sales/manager), `is_active`
- `avatar_url`
- `created_at`, `updated_at`

## Running Locally

```bash
# Start PostgreSQL + API
docker compose up -d

# Or run API directly (requires PostgreSQL on localhost:5432)
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# API docs at http://localhost:8000/docs
```

## Testing

```bash
# Requires a running PostgreSQL instance
pytest tests/ -v --cov=app
```
