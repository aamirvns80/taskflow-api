import pytest
from fastapi.testclient import TestClient


def test_create_task(sqlalchemy_client: TestClient):
    response = sqlalchemy_client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "completed": False
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    
    

def test_task_crud_workflow(sqlalchemy_client: TestClient):
    # 1. Create a task
    create_response = sqlalchemy_client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "description": "Complete SQLAlchemy migration",
            "completed": False,
        },
    )

    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]

    # 2. Retrieve task by ID
    get_response = sqlalchemy_client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Learn FastAPI"

    # 3. Retrieve all tasks
    list_response = sqlalchemy_client.get("/tasks/")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    # 4. Replace task using PUT
    put_response = sqlalchemy_client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Learn Python Backend",
            "description": "Complete the TaskFlow project",
            "completed": False,
        },
    )

    assert put_response.status_code == 200
    assert put_response.json()["title"] == "Learn Python Backend"

    # 5. Partially update task using PATCH
    patch_response = sqlalchemy_client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["completed"] is True

    # 6. Delete task
    delete_response = sqlalchemy_client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200

    # 7. Verify task no longer exists
    missing_response = sqlalchemy_client.get(f"/tasks/{task_id}")

    assert missing_response.status_code == 404
