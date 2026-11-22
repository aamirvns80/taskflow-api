# TaskFlow API

A RESTful task management API built with **Python 3.13**, **FastAPI**, **SQLAlchemy**, and **SQLite**. The project demonstrates a layered backend architecture, database migrations, automated testing, containerization, and continuous integration.

## Overview

TaskFlow API provides HTTP endpoints to create, retrieve, update, and delete tasks. It is structured as a maintainable backend application with separate API routers, service logic, database models, and repository code.

## Features

- Create a task and retrieve all tasks
- Retrieve an individual task by ID
- Replace a task with PUT and partially update it with PATCH
- Delete a task
- Validate request and response data with Pydantic
- Use SQLAlchemy ORM and SQLite for persistence
- Separate API, service, and repository responsibilities
- Manage schema changes with Alembic migrations
- Configure application settings with environment variables
- Centralize application logging and handle unexpected server errors
- Run automated tests with pytest
- Build and run the API with Docker Compose
- Run tests automatically with GitHub Actions on pushes and pull requests

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Application language |
| FastAPI | REST API framework |
| SQLAlchemy 2.x | ORM and database access |
| SQLite | Relational database |
| Pydantic | Request and response validation |
| Alembic | Database schema migrations |
| pytest | Automated tests |
| HTTPX | API test client |
| Docker / Docker Compose | Containerization and local deployment |
| GitHub Actions | Continuous integration |

## Project Structure

```text
taskflow-api/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── routers/
│   │   └── tasks.py
│   ├── repositories/
│   │   └── task_repository.py
│   ├── services/
│   │   ├── task_service.py
│   │   └── task_orm_service.py
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── db_session.py
│   ├── db_dependencies.py
│   ├── dependencies.py
│   ├── logging_config.py
│   ├── models.py
│   └── schemas.py
├── migrations/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13
- Git
- Docker Desktop (optional, for containerized execution)

### 1. Clone the repository

```bash
git clone https://github.com/aamirvns80/taskflow-api.git
cd taskflow-api
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python -m alembic upgrade head
```

This applies the migrations defined in the `migrations/` directory to the configured SQLite database. Back up an existing database before applying schema changes.

### 5. Start the development server

```bash
python -m uvicorn app.main:app --reload
```

The API is served at `http://127.0.0.1:8000`.

### 6. Open API documentation

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API Endpoints

The task router is mounted under `/tasks`.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Basic health check |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PUT | `/tasks/{task_id}` | Replace task fields |
| PATCH | `/tasks/{task_id}` | Partially update task fields |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Example: Create a task

Send a `POST` request to `/tasks/` with:

```json
{
  "title": "Learn FastAPI",
  "description": "Build a professional backend project",
  "completed": false
}
```

Use the interactive Swagger UI at `/docs` to try the endpoints and inspect their request and response schemas.

## Database Migrations

Alembic tracks database schema changes. Common commands:

```bash
# Apply all pending migrations
python -m alembic upgrade head

# Show the current database revision
python -m alembic current

# Show migration history
python -m alembic history

# Roll back one migration
python -m alembic downgrade -1
```

Only run downgrade commands when you understand the impact on stored data. Back up the SQLite database first.

## Run with Docker Compose

Make sure Docker Desktop is running, then build and start the service:

```bash
docker compose build
docker compose up -d
```

Check the container and logs:

```bash
docker compose ps
docker compose logs -f api
```

Open [http://localhost:8000/docs](http://localhost:8000/docs).

Stop the service:

```bash
docker compose down
```

The Compose configuration mounts the local `taskflow.db` file into the container so the SQLite database persists across container restarts. Keep backups of this file.

## Running Tests

Run the complete test suite from the project root:

```bash
python -m pytest -v
```

Or use quiet output:

```bash
python -m pytest -q
```

## Continuous Integration

The GitHub Actions workflow at `.github/workflows/ci.yml` runs when code is pushed to, or a pull request targets, the configured branches. It checks out the repository, sets up Python 3.13, installs `requirements.txt`, and runs `pytest -q`.

View workflow runs: [GitHub Actions](https://github.com/aamirvns80/taskflow-api/actions).

## Configuration

Application settings are defined in `app/config.py` and can be overridden with environment variables. The settings include:

- `APP_NAME`
- `APP_ENV`
- `DEBUG`

A local `.env` file may be used for development configuration. Do not commit secrets or private credentials.

## Current Scope

This project is a learning and portfolio backend API. Authentication, user accounts, authorization, pagination, and production database deployment are not described as implemented features.

## License

No license is currently specified. Contact the repository owner before reusing this project beyond the permissions granted by GitHub's default terms.
