from unittest.mock import patch

import pytest

from app.models import Task
from app.repositories.task_repository import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)


def test_create_task(sqlalchemy_db):
    task=Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    
    result = create_task(sqlalchemy_db, task)
    
    assert result.id is not None
    assert result.title == "Learn SQLAlchemy"
    assert result.description== "Practice ORM"
    assert result.completed is False
    
    
def test_get_task_by_id(sqlalchemy_db):
    task = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    created_task = create_task(sqlalchemy_db, task)

    result = get_task_by_id(sqlalchemy_db, created_task.id)

    assert result is not None
    assert result.id == created_task.id
    assert result.title == "Learn SQLAlchemy"
    assert result.description == "Practice ORM"
    assert result.completed is False
    
    
def test_update_task(sqlalchemy_db):
    task = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    created_task = create_task(sqlalchemy_db, task)

    created_task.title = "Learn SQLAlchemy Updated"
    created_task.description = "Practice ORM Updated"
    created_task.completed = True

    result = update_task(sqlalchemy_db, created_task)

    assert result is not None
    assert result.id == created_task.id
    assert result.title == "Learn SQLAlchemy Updated"
    assert result.description == "Practice ORM Updated"
    assert result.completed is True

def test_delete_task(sqlalchemy_db):
    task = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    created_task = create_task(sqlalchemy_db, task)
    task_id = created_task.id

    delete_task(sqlalchemy_db, created_task)

    result = get_task_by_id(sqlalchemy_db, task_id)
    assert result is None


def test_get_all_tasks(sqlalchemy_db):
    task1 = Task(
        title="Learn SQLAlchemy",
        description="Practice ORM",
        completed=False
    )
    task2 = Task(
        title="Learn FastAPI",
        description="Build API",
        completed=False
    )
    create_task(sqlalchemy_db, task1)
    create_task(sqlalchemy_db, task2)

    result = get_all_tasks(sqlalchemy_db)

    assert result is not None
    assert len(result) >= 2
    assert result[0].title == "Learn SQLAlchemy" 
    assert result[1].title == "Learn FastAPI"
    
   
def test_commit_transaction_rolls_back(sqlalchemy_db):
    from app.repositories.task_repository import commit_transaction
    
    with patch.object(
        sqlalchemy_db,
        "commit",
        side_effect=RuntimeError("Simulated commit failure")
    ):
        with pytest.raises(RuntimeError, match="Simulated commit failure"):
            commit_transaction(sqlalchemy_db)