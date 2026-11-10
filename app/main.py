from fastapi import Depends, FastAPI, HTTPException

from app.database import (
    delete_task_by_id,
    get_task_by_id,
    patch_task,
)
from app.dependencies import get_db_path
from app.routers import tasks
from app.schemas import TaskPatch, TaskResponse, TaskUpdate

app = FastAPI(
    title="TaskFlow API",
    description="A task management API built with Python.",
    version="0.1.0")

app.include_router(tasks.router,prefix="/tasks")

@app.get("/")
def read_root():
    return {
        "message":"Welcome to TaskFlow API"
    }

@app.get("/health")
def health_check():
    return{
        "status":"healthy"
    }









