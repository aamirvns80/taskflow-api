from app.models import Task
from sqlalchemy.orm import Session

def get_task_by_id(db:Session,task_id: int):
    return db.get(Task,task_id)


def get_all_tasks(db: Session):
    return db.query(Task).all()

def create_task(db: Session,task: Task):
    db.add(task)
    db.flush()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task):
    db.flush()
    db.refresh(task)
    return task

def delete_task(db: Session,task: Task):
    db.delete(task)
    db.flush()
    
def commit_transaction(db:Session):
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
