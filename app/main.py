from fastapi import Depends, FastAPI, HTTPException

from app.database import (
    DATABASE_PATH,
    delete_task_by_id,
    get_task_by_id,
    patch_task,
    update_task_status,
)
from app.dependencies import get_db_path
from app.routers import tasks
from app.schemas import TaskCreate, TaskPatch, TaskResponse, TaskUpdate

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


@app.get("/tasks/{task_id}")
def get_task(task_id: int,db_path=Depends(get_db_path)):
    result = get_task_by_id(task_id,db_path)
    if result is None:
        raise HTTPException(status_code=404,
                                detail="Task not found")
   
    result={
        "id":result["id"],
        "title":result["title"],
        "description":result["description"],
        "completed":result["completed"]
    }
    return result
        
    
    
@app.put("/tasks/{task_id}",response_model=TaskResponse)
def update_task(task_id:int,task_data:TaskUpdate,db_path=Depends(get_db_path)):
    rows_update = update_task_status(task_id,task_data.completed,db_path)
    if rows_update ==0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
        
    updated_rows = get_task_by_id(task_id,db_path)
    updated_rows={
        "id":updated_rows["id"],
        "title":updated_rows["title"],
        "description":updated_rows["description"],
        "completed": updated_rows["completed"]
        
    }
    
    return updated_rows
   
@app.delete("/tasks/{task_id}")
def delete_task(task_id:int,db_path=Depends(get_db_path)):
    row_deleted = delete_task_by_id(task_id,db_path)
    
    if row_deleted ==0:
          raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
    return {
        "message":"Task deleted successfully"
    }
        

    
@app.patch("/tasks/{task_id}",response_model=TaskResponse)
def update_task(task_id:int,task_data:TaskPatch,db_path=Depends(get_db_path)):
    updates = task_data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )
        
    rows_updated = patch_task(task_id,updates,db_path)
    if rows_updated ==0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
        
        
    updated_task = get_task_by_id(task_id,db_path)
    
    return{
        "id": updated_task["id"],
        "title":updated_task["title"],
        "description":updated_task["description"],
        "completed":bool(updated_task["completed"])
    }
        
    
    
    
    
