from unittest.mock import patch

import pytest

from app.models import Task
from app.repositories.task_repository import get_task_by_id
from app.services.task_orm_service import (
    create_task_service,
    delete_task_service,
    get_all_tasks_service,
    get_task_service,
    update_task_service,
)


def test_create_task_service(sqlalchemy_db):
    task =Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    
    result = create_task_service(sqlalchemy_db, task)
    
    assert result.id is not None
    assert result.title == "Learn SQLAlchemy"
    assert result.description == "Practice ORM"
    assert result.completed is False
    

def test_create_task_service_rolls_back(sqlalchemy_db):
    task = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    
    with patch("app.services.task_orm_service.create_task", side_effect=RuntimeError("Database failure")):
        with pytest.raises(RuntimeError,match="Database failure"):
            create_task_service(sqlalchemy_db, task)
    
    # Ensure the task was not committed
    assert sqlalchemy_db.query(Task).count() == 0
    
    
def test_delete_task_service(sqlalchemy_db):
    task = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    
    )
    created_task = create_task_service(sqlalchemy_db, task)
    task_id = created_task.id
    
    result = delete_task_service(sqlalchemy_db, task_id)
    
    assert result is True
    assert get_task_by_id(sqlalchemy_db, created_task.id) is None
    
    
def test_delete_task_service_not_found(sqlalchemy_db):
    result = delete_task_service(sqlalchemy_db, 999)
    assert result is False
    
    
def test_update_task_service(sqlalchemy_db):
    task = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    created_task = create_task_service(sqlalchemy_db, task)
    created_task.title = "Learn SQLAlchemy Updated"
    created_task.description = "Practice ORM Updated"
    created_task.completed = True

    updated_task = update_task_service(sqlalchemy_db, created_task)

    assert updated_task.id == created_task.id
    assert updated_task.title == "Learn SQLAlchemy Updated"
    assert updated_task.description == "Practice ORM Updated"
    assert updated_task.completed is True
    
def test_get_task_service(sqlalchemy_db):
    task = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    created_task = create_task_service(sqlalchemy_db, task)
    task_id = created_task.id

    result = get_task_service(sqlalchemy_db, task_id)

    assert result.id == created_task.id
    assert result.title == "Learn SQLAlchemy"
    assert result.description == "Practice ORM"
    assert result.completed is False
    
def test_get_all_tasks_service(sqlalchemy_db):
    task1 = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    task2 = Task(
        title="Learn FastAPI",
        description="Practice API",
        completed=False
    )
    create_task_service(sqlalchemy_db, task1)
    create_task_service(sqlalchemy_db, task2)

    result = get_all_tasks_service(sqlalchemy_db)

    assert len(result) == 2
    assert result[0].title == "Learn SQLAlchemy"
    assert result[1].title == "Learn FastAPI"