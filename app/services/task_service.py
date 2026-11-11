from app.database import (
    add_task,
    delete_task_by_id,
    get_all_tasks,
    get_task_by_id,
    patch_task,
    update_task_status,
)
from app.schemas import TaskCreate, TaskUpdate


def create_task_service(task:TaskCreate,db_path):
    task_id = add_task(
        task.title,
        task.description,
        task.completed,
        db_path
    )
    
    task = get_task_by_id(task_id,db_path)
    
    return task


def get_task_service(task_id:int,db_path):
    task = get_task_by_id(task_id,db_path)
    return task


def update_task_service(task_id: int,task_data: TaskUpdate,db_path):
    rows_updated = update_task_status(
        task_id,
        task_data.completed,
        db_path
    )
    return rows_updated


def patch_task_service(task_id: int,updates:dict[str,object],db_path):
    rows_updated = patch_task(
        task_id,
        updates,
        db_path
    )
    
    return rows_updated


def delete_task_service(task_id:int,db_path):
    rows_deleted =delete_task_by_id(task_id,db_path)
    return rows_deleted

def get_all_tasks_service(db_Path):
    tasks = get_all_tasks(db_Path)
    return tasks