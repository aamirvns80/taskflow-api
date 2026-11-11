from app.schemas import TaskCreate
from app.services.task_service import create_task_service

def test_create_task_service(test_db):
    task=TaskCreate(title="Learn FastAPI",description="Practice FastAPI")
    task_create = create_task_service(task,test_db)
    
    assert task_create["title"]=="Learn FastAPI"
    assert task_create["description"] =="Practice FastAPI"