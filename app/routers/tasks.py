from fastapi import APIRouter, Depends, HTTPException

from app.database import DATABASE_PATH, add_task, get_all_tasks, get_task_by_id
from app.dependencies import get_db_path
from app.schemas import TaskCreate, TaskResponse

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