from fastapi import APIRouter, Depends, HTTPException

from app.database import (
    add_task,
    delete_task_by_id,
    get_all_tasks,
    get_task_by_id,
    patch_task,
    update_task_status,
)
from app.dependencies import get_db_path
from app.schemas import TaskCreate, TaskPatch, TaskResponse, TaskUpdate

router= APIRouter()



@router.get("/",response_model=list[TaskResponse])
def get_tasks(db_path=Depends(get_db_path)):
    rows = get_all_tasks(db_path)
    return [{
        "id":row["id"],
        "title":row["title"],
        "description":row["description"],
        "completed":bool(row["completed"])

    }
            for row in rows]


@router.post("/",response_model=TaskResponse,status_code=201)
def create_task(task:TaskCreate,db_path = Depends(get_db_path)):
    task_id = add_task(
        task.title,
        task.description,
        task.completed,
        db_path
    )

    task= get_task_by_id(task_id,db_path)

    if task is None:
        raise HTTPException(
            status_code = 500,
            detail="Created task could not be retrieved"
        )

    return {
        "id": task["id"],
        "title": task["title"],
        "description": task["description"],
        "completed": bool(task["completed"])
    }


@router.get("/{task_id}",response_model=TaskResponse)
def get_task(task_id: int,db_path=Depends(get_db_path)):
    result = get_task_by_id(task_id,db_path)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return{
        "id":result["id"],
        "title": result["title"],
        "description":result["description"],
        "completed":bool(result["completed"])
    }


@router.put("/{task_id}",response_model=TaskResponse)
def update_task(task_id:int,task_data:TaskUpdate,db_path = Depends(get_db_path)):
    rows_update = update_task_status(task_id,task_data.completed,db_path)
    if rows_update==0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    updated_rows=get_task_by_id(task_id,db_path)

    return{
        "id":updated_rows["id"],
        "title":updated_rows["title"],
        "description":updated_rows["description"],
        "completed":bool(updated_rows["completed"])
    }


@router.patch("/{task_id}",response_model=TaskResponse)
def update_task(task_id:int,task_data: TaskPatch,db_path = Depends(get_db_path)):
    updates =task_data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    rows_updated=patch_task(task_id,updates,db_path)

    if rows_updated==0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    updated_task=get_task_by_id(task_id,db_path)

    return{
        "id":updated_task["id"],
        "title":updated_task["title"],
        "description":updated_task["description"],
        "completed":bool(updated_task["completed"])
    }

@router.delete("/{task_id}")
def delete_task(task_id: int,db_path = Depends(get_db_path)):
    rows_deleted = delete_task_by_id(task_id,db_path)
    if rows_deleted==0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )


    return {
        "message": "Task deleted successfully"
    }