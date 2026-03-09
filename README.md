# Secura-AI
Security layers for your developing models.

## Run (local dev, easiest)

### Backend

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt

# SQLite quickstart (no migrations)
set AUTO_CREATE_SCHEMA=true
python -m uvicorn backend.app.main:app --reload
```

Open the UI at `http://127.0.0.1:8000/ui/`.

### Create an API key (for console endpoints)

Set a bootstrap token and call the bootstrap endpoint once:

```bash
set BOOTSTRAP_TOKEN=change-me
curl -X POST http://127.0.0.1:8000/admin/bootstrap -H "X-Bootstrap-Token: change-me"
```

Copy the returned `api_key` into the UI Settings (or top bar `apiKey` field).

## Run (Docker Compose)

```bash
docker compose up -d postgres redis
docker compose run --rm migrate
docker compose up -d api worker
```

Then open the UI at `http://127.0.0.1:8000/ui/`.

## Python SDK

See `[sdk/python/README.md](sdk/python/README.md)`.
