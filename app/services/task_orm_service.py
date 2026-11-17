from sqlalchemy.orm import Session

from app.models import Task
from app.repositories.task_repository import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)


def create_task_service(db:Session, task: Task):
    try:
        created_task = create_task(db, task)
        db.commit()
        db.refresh(created_task)
        return created_task
    except Exception:
        db.rollback()
        raise
    
def get_task_service(db: Session,task_id:int):
    return get_task_by_id(db, task_id)

def get_all_tasks_service(db: Session):
    return get_all_tasks(db)

def patch_task_service(db: Session, task_id: int, updates: dict):
    try:
        task = get_task_by_id(db, task_id)

        if task is None:
            return None

        for field, value in updates.items():
            setattr(task, field, value)

        updated_task = update_task(db, task)
        db.commit()
        db.refresh(updated_task)

        return updated_task
    except Exception:
        db.rollback()
        raise

def update_task_service(db: Session, task: Task):
    try:
        updated_task = update_task(db, task)
        db.commit()
        db.refresh(updated_task)
        return updated_task
    except Exception:
        db.rollback()
        raise
    
def delete_task_service(db: Session, task_id: int):
    try:
        task = get_task_by_id(db, task_id)
        if task is None:
            return False
        delete_task(db, task)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise


def update_task_by_id_service(db: Session, task_id: int, updates: dict):
    try:
        task = get_task_by_id(db, task_id)

        if task is None:
            return None

        for field, value in updates.items():
            setattr(task, field, value)

        updated_task = update_task(db, task)
        db.commit()
        db.refresh(updated_task)

        return updated_task

    except Exception:
        db.rollback()
        raise
