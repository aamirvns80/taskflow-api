
from unittest import result

import pytest

from app.database import (
    add_task,
    delete_task_by_id,
    get_all_tasks,
    get_connection,
    get_task_by_id,
    update_task_status,
)


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
   
    
    
    
    