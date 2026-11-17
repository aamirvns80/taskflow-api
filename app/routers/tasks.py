
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db_dependencies import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskPatch, TaskResponse, TaskUpdate
from app.services.task_orm_service import (
    create_task_service as create_task_orm_service,
)
from app.services.task_orm_service import (
    delete_task_service as delete_task_orm_service,
)
from app.services.task_orm_service import (
    get_all_tasks_service as get_all_tasks_orm_service,
)
from app.services.task_orm_service import (
    get_task_service as get_task_orm_service,
)
from app.services.task_orm_service import (
    patch_task_service as patch_task_orm_service,
)
from app.services.task_orm_service import (
    update_task_by_id_service,
)

router = APIRouter()


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return get_all_tasks_orm_service(db)



@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.model_dump())

    created_task = create_task_orm_service(db, new_task)

    if created_task is None:
        raise HTTPException(
            status_code=500,
            detail="Created task could not be retrieved",
        )

    return created_task



@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_orm_service(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def replace_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    updates = task_data.model_dump()

    updated_task = update_task_by_id_service(db, task_id, updates)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskPatch,
    db: Session = Depends(get_db),
):
    updates = task_data.model_dump(exclude_unset=True)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update",
        )

    updated_task = update_task_by_id_service(db, task_id, updates)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted = delete_task_orm_service(db, task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}
