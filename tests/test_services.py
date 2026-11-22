from unittest.mock import patch

import pytest

from app.schemas import TaskCreate, TaskUpdate
from app.services.task_service import (
    create_task_service,
    delete_task_service,
    get_all_tasks_service,
    get_task_service,
    patch_task_service,
    update_task_service,
)


def test_create_task_service(test_db):
    task=TaskCreate(title="Learn FastAPI",description="Practice FastAPI")
    task_create = create_task_service(task,test_db)

    assert task_create["title"]=="Learn FastAPI"
    assert task_create["description"] =="Practice FastAPI"


def test_create_task_service_with_mock():
    with patch("app.services.task_service.add_task") as mock_add_task:
        mock_add_task.return_value=1
        task = TaskCreate(title="Learn FastAPI",description="Practice FastAPI")


        with patch("app.services.task_service.get_task_by_id") as mock_get_task:
            mock_get_task.return_value = {"id": 1, "title": "Learn FastAPI", "description": "Practice FastAPI", "completed": False}
            result = create_task_service(task, "test_db")
            mock_add_task.assert_called_once_with(
                task.title, task.description, False, "test_db"
            )
            mock_get_task.assert_called_once_with(1, "test_db")
            assert result["id"] == 1
            assert result["title"] == "Learn FastAPI"
            assert result["description"] == "Practice FastAPI"
            assert result["completed"] is False



def test_create_task_service_when_database_fails():
    with patch("app.services.task_service.add_task") as mock_add_task:
        mock_add_task.side_effect=RuntimeError("Database error")

        task=TaskCreate(title="Learn FastAPI",
                        description="Practice FastAPI")

        with pytest.raises(RuntimeError,match="Database error"):
            create_task_service(task,"test.db")

def test_update_task_service_with_mock():
    with patch("app.services.task_service.update_task_status") as mock_update_task:
        mock_update_task.return_value = 1
        task_data = TaskUpdate(
            title="Learn FastAPI",
            description="Practice FastAPI",
            completed = True)
        result = update_task_service(
            task_id=1,
            task_data = task_data,
            db_path = "test.db"
        )

        mock_update_task.assert_called_once_with(
            1,
            True,
            "test.db"
        )
        assert result == 1

def test_update_task_service_when_database_fails():
    with patch("app.services.task_service.update_task_status") as mock_update:
        mock_update.side_effect = RuntimeError("Database error")
        task_data = TaskUpdate(
            title="Learn FastAPI",
            description="Practice FastAPI",
            completed=True
        )
        with pytest.raises(RuntimeError, match="Database error"):
            update_task_service(
                task_id=1,
                task_data=task_data,
                db_path="test.db"
            )


def test_patch_task_service_with_mock():
    with patch("app.services.task_service.patch_task") as mock_patch:
        mock_patch.return_value = 1
        updates = {
            "title": "Updated title"
        }
        result = patch_task_service(
            task_id=1,
            updates=updates,
            db_path="test.db"
        )
        mock_patch.assert_called_once_with(
            1,
            updates,
            "test.db"
        )
        assert result == 1

def test_patch_task_service_when_database_fails():
    with patch("app.services.task_service.patch_task") as mock_patch:
        mock_patch.side_effect = RuntimeError("Database error")
        updates = {
            "title": "Updated title"
        }
        with pytest.raises(RuntimeError, match="Database error"):
            patch_task_service(
                task_id=1,
                updates=updates,
                db_path="test.db"
            )

def test_delete_task_service_with_mock():
    with patch("app.services.task_service.delete_task_by_id") as mock_delete:
        mock_delete.return_value=1
        result = delete_task_service(
            task_id=1,
            db_path="test.db"

        )
        mock_delete.assert_called_once_with(
            1,
            "test.db"
        )
        assert result == 1

def test_delete_task_service_when_database_fails():
    with patch("app.services.task_service.delete_task_by_id") as mock_delete:
        mock_delete.side_effect = RuntimeError("Database error")
        with pytest.raises(RuntimeError, match="Database error"):
            delete_task_service(
                task_id=1,
                db_path="test.db"
            )

def test_get_task_service_with_mock():
    with patch("app.services.task_service.get_task_by_id") as mock_get_task:
        mock_get_task.return_value = {"id": 1, "title": "Learn FastAPI", "description": "Practice FastAPI", "completed": False}
        result = get_task_service(
            task_id = 1,
            db_path="test.db"
        )
        mock_get_task.assert_called_once_with(
            1,
            "test.db"
        )
        assert result["id"] == 1
        assert result["title"] == "Learn FastAPI"
        assert result["description"] == "Practice FastAPI"
        assert result["completed"] is False

def test_get_task_service_when_task_not_found():
    with patch("app.services.task_service.get_task_by_id") as mock_get_task:
        mock_get_task.return_value = None
        result = get_task_service(
            task_id=999,
            db_path="test.db"
        )
        mock_get_task.assert_called_once_with(
            999,
            "test.db"
        )
        assert result is None

def test_get_all_tasks_service_with_mock():
    with patch("app.services.task_service.get_all_tasks") as mock_get_all:
        mock_get_all.return_value = [
            {"id": 1, "title": "Learn FastAPI", "description": "Practice FastAPI", "completed": False},
            {"id": 2, "title": "Learn Python", "description": "Practice Python", "completed": True}
        ]
        result = get_all_tasks_service(
            "test.db"
        )
        mock_get_all.assert_called_once_with(
            "test.db"
        )
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["title"] == "Learn FastAPI"
        assert result[0]["description"] == "Practice FastAPI"
        assert result[0]["completed"] is False
        assert result[1]["id"] == 2
        assert result[1]["title"] == "Learn Python"
        assert result[1]["description"] == "Practice Python"
        assert result[1]["completed"] is True


def test_get_all_tasks_service_when_no_tasks():
    with patch("app.services.task_service.get_all_tasks") as mock_get_all:
        mock_get_all.return_value = []
        result = get_all_tasks_service(
            "test.db"
        )
        mock_get_all.assert_called_once_with(
            "test.db"
        )
        assert result == []
        assert isinstance(result, list)
