# S'n'D — Seek & Destroy

OSINT database for tracking Russian military personnel involved in the war against Ukraine.

## Stack

- **Backend** — Python / FastAPI + MongoDB (odmantic)
- **Frontend** — Nuxt.js 2 (SPA)
- **Infrastructure** — Docker Compose, Nginx, Mailpit

## Running locally

**Requirements:** Docker (or Podman) with Compose.

```bash
docker-compose -f docker-compose.dev.yml up -d
```

| Service | URL |
|---|---|
| App | http://localhost:8080 |
| API docs | http://localhost:8080/api/docs |
| Mail UI | http://localhost:1080 |

## Database setup

Run once after first start (idempotent — safe to re-run):

```bash
# Create indexes
docker exec -w /opt/project api python migrations/migrate.py

# Load demo data
docker exec -w /opt/project api python migrations/seed.py
```

## Demo credentials

| Email | Password | Role |
|---|---|---|
| admin@snd.local | Admin1234! | Admin |
| editor@snd.local | Editor1234! | Editor |
| guest@snd.local | Guest1234! | Guest |

**Roles:** Guest — read only · Editor — add/edit records · Admin — full access.
