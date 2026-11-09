# TaskFlow API

A RESTful task management API built with Python, FastAPI, and SQLite.

## Overview

TaskFlow API allows users to create, retrieve, update, and delete tasks through RESTful HTTP endpoints.

The project demonstrates backend development concepts including API design, database integration, request validation, dependency injection, and automated testing.

## Tech Stack

- **Python** — Backend programming language
- **FastAPI** — REST API framework
- **SQLite** — Relational database
- **Pydantic** — Request and response validation
- **Pytest** — Automated testing
- **HTTPX** — API testing

## Features

- Create a task
- Retrieve all tasks
- Retrieve a task by ID
- Update task status
- Partially update task fields
- Delete a task
- Validate request data
- Return appropriate HTTP status codes
- Test API endpoints using pytest

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aamimn80/taskflow-api.git
cd taskflow-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m uvicorn app.main:app --reload
```

### 6. Open API documentation

Visit:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

## Project Structure

```text
taskflow-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   └── routers/
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_database.py
│   └── test_main.py
│
├── .gitignore
├── requirements.txt
└── README.md
```
## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PUT | `/tasks/{task_id}` | Update task status |
| PATCH | `/tasks/{task_id}` | Partially update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Example Request

Create a task:

```json
{
  "title": "Learn FastAPI",
  "description": "Build a professional backend project",
  "completed": false
}
```

## Testing

The project uses pytest for automated testing.

Run all tests:

```bash
python -m pytest -v
```