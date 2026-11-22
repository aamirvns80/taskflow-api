import logging
import sqlite3
from unittest.mock import Mock, patch

import pytest

from app.database import (
    DATABASE_PATH,
    add_task,
    create_tables,
    delete_task_by_id,
    get_all_tasks,
    get_connection,
    get_task_by_id,
    patch_task,
    update_task_status,
)
from app.dependencies import get_db_path


def test_database_connection(test_db):
    connection = get_connection(test_db)
    assert connection is not None


def test_tasks_table_exists(test_db):
    connection =get_connection(test_db)
    cursor = connection.execute("""
                             SELECT name
                             FROM  sqlite_master
                             WHERE type = 'table' AND name ='tasks'
                             """)
    result = cursor.fetchone()

    assert result is not None
    assert result["name"] == "tasks"
    connection.close()

def test_insert_task(test_db):
    task_id = add_task(
        "Learn SQL",
        "Practice SQLite",
        False,
        test_db
    )
    result = get_task_by_id(task_id,test_db)

    assert result["title"] == "Learn SQL"
    assert result["description"] == "Practice SQLite"
    assert result["completed"] == 0



def test_get_completed_tasks(test_db):
    add_task("Task 1","Description 1", True, test_db)
    add_task("Task 2","Description 2", False, test_db)
    tasks = get_all_tasks(test_db)
    completed_tasks = [task for task in tasks if task["completed"] == 1]


    assert len(completed_tasks) == 1
    assert completed_tasks[0]["title"] == "Task 1"



def test_update_task_status(test_db):
    task_id = add_task(
        "Learn Python",
        "Practice FastAPI",
        False,
        test_db
    )
    rows_updated = update_task_status(task_id, True, test_db)
    result = get_task_by_id(task_id, test_db)
    assert rows_updated == 1
    assert result["completed"]== 1

def test_delete_task(test_db):
    task_id = add_task("Learn Python","Practice Python", False, test_db)
    rows_deleted = delete_task_by_id(task_id, test_db)
    result = get_task_by_id(task_id, test_db)

    assert result is None
    assert rows_deleted == 1

def test_get_all_tasks(test_db):
    add_task("Task1","description1",False, test_db)
    add_task("Task2","description2",True,test_db)
    tasks = get_all_tasks(test_db)
    assert len(tasks)==2


def test_patch_task(test_db):
    task_id =add_task("Learn Python","Practice coding",False,test_db)
    updates = {"title":"Learn FastAPI"}
    rows_updated = patch_task(task_id,updates,test_db)
    result = get_task_by_id(task_id,test_db)

    assert result["title"]=="Learn FastAPI"
    assert result["description"] =="Practice coding"
    assert result["completed"] == 0


def test_patch_task_empty_updates(test_db):
    task_id =add_task(
        "Learn Python",
        "Practice coding",
        False,
        test_db
    )

    with pytest.raises(ValueError):
        patch_task(task_id,{},test_db)

def test_patch_task_invalid_field(test_db):
    task_id =add_task(
        "Learn Pthon",
        "Practice coding",
        False,
        test_db
    )

    updates ={"invalid_column":"Hello"}
    with pytest.raises(ValueError):
        patch_task(task_id,updates,test_db)

def test_patch_task_nonexistent_id(test_db):
    rows_updated=patch_task(999,{"title":"New title"},test_db)
    assert rows_updated==0



def test_rollback_update(test_db):
    task_id = add_task(
        "Learn Python",
        "Practice coding",
        False,
        test_db
    )

    connection =get_connection(test_db)

    try:
        connection.execute(
            "UPDATE tasks SET completed =? WHERE id=?",
            (1,task_id)
        )

        connection.rollback()

    finally:
        connection.close()

        original_row = get_task_by_id(task_id,test_db)

        assert original_row["completed"]==0

def test_rollback_on_exception(test_db):
    task_id = add_task(title="Learn python",
                       description="Practice coding",
                       completed=False,
                       db_path=test_db)

    connection = get_connection(test_db)
    with pytest.raises(ValueError,match="Simulated database failure"):

        try:
            connection.execute(
                "UPDATE tasks SET completed =? WHERE id=?",
                (1,task_id)
            )
            raise ValueError("Simulated database failure")
        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    original_row = get_task_by_id(task_id,test_db)

    assert original_row["completed"] ==0

def test_add_task_rolls_back_on_error():
    with patch("app.database.get_connection") as mock_get_connection:
        mock_connection = Mock()

        mock_get_connection.return_value=mock_connection
        mock_connection.execute.side_effect = RuntimeError("Database failure")

        with pytest.raises(RuntimeError,match="Database failure"):
            add_task(
                title="Learn Python",
                description="Practice coding",
                completed=False,
                db_path="test.db"
            )

        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()


def test_update_task_rolls_back_on_error():
    with patch("app.database.get_connection") as mock_get_connection:
        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection
        mock_connection.execute.side_effect = RuntimeError("Database failure")

        with pytest.raises(RuntimeError,match="Database failure"):
            update_task_status(
                task_id=1,
                completed=True,
                db_path="test.db"
            )

        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()


def test_delete_task_rolls_back_on_error():
    with patch("app.database.get_connection") as mock_get_connection:
        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection
        mock_connection.execute.side_effect = RuntimeError("Database failure")

        with pytest.raises(RuntimeError,match="Database failure"):
            delete_task_by_id(
                task_id=1,
                db_path="test.db"
            )

        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()

def test_patch_task_rolls_back_on_error():
    with patch("app.database.get_connection") as mock_get_connection:
        mock_connection = Mock()
        mock_get_connection.return_value = mock_connection
        mock_connection.execute.side_effect = RuntimeError("Database failure")

        with pytest.raises(RuntimeError,match="Database failure"):
            patch_task(
                task_id=1,
                updates={
                    "title":"Updated title"
                },
                db_path="test.db"
            )
        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()


def test_create_tables_closes_connection_on_error():
    with patch("app.database.get_connection") as mock_get_connection:
        mock_connection = Mock()
        mock_get_connection.return_value=mock_connection

        mock_connection.execute.side_effect = RuntimeError("Table creation failed")

        with pytest.raises(RuntimeError, match="Table creation failed"):
            create_tables(db_path="test.db")
        mock_connection.rollback.assert_called_once()
        mock_connection.close.assert_called_once()



def test_get_db_path():
    result = get_db_path()
    assert result == DATABASE_PATH


def test_database_error_is_logged(tmp_path, caplog):

    from app.database import add_task

    db_path = tmp_path / "empty.db"

    with caplog.at_level(logging.ERROR):

        with pytest.raises(sqlite3.OperationalError):
            add_task(
                title="Test task",
                description="Trigger database error",
                completed=False,
                db_path=db_path
            )
    assert "Failed to add task" in caplog.text
    assert "no such table: tasks" in caplog.text









