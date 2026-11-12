from unittest.mock import patch

from app.routers import tasks

#client = TestClient(app)

def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_create_task(client):
    response = client.post("/tasks",json={
        "title": "Learn FastAPI",
        "description": "Practice API testing",
        "completed": False
    })

    assert response.status_code ==201
    data = response.json()

    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Practice API testing"
    assert data["completed"] is False
    assert "id" in data


def test_patch_task(client):
    create_response = client.post("/tasks",json={
        "title": "Learn Python",
        "description": "Practice coding",
        "completed": False
    })

    task_id = create_response.json()["id"]
    response = client.patch(f"/tasks/{task_id}",json={"title":"Learn FastAPI"})
    assert response.status_code == 200

    data = response.json()
    assert data["title"]=="Learn FastAPI"
    assert data["description"] =="Practice coding"
    assert data["completed"] is False


def test_delete_task(client):
    create_response=client.post("/tasks",json={
        "title":"Learn Python",
        "description":"Practice coding",
        "completed": False
    })

    task_id =create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code ==200
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code ==404

def test_health_endpoint(client):
    response=client.get("/health")

    assert response.status_code ==200
    assert response.json() == {"status":"healthy"}

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code ==200
    assert response.json()=={"message":"Welcome to TaskFlow API"}


def test_patch_nonexistent_task(client):
    response = client.patch("/tasks/9898",json={
        "title": "Learn FastAPI"
    })

    assert response.status_code ==404

    assert response.json()["detail"] =="Task not found"

def test_patch_empty_updates(client):
    create_response = client.post("/tasks/",json={
        "title":"Learn Python",
        "description":"Practice coding",
        "completed":False
    })

    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}",json={})

    assert response.status_code ==400
    assert response.json()["detail"]=="No fields provided for update"

def test_patch_null_title(client):
    create_response = client.post("/tasks/",json={
        "title":"Learn Python",
        "description":"Practice coding",
        "completed":False
    })

    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}",json={"title":None})


    assert response.status_code ==422

def test_patch_invalid_boolean(client):
    create_response = client.post("/tasks/",json={
        "title":"Learn Python",
        "description":"Practice coding",
        "completed":False
    })

    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}",json={"completed":"True"})

    assert response.status_code ==422

def test_patch_valid_boolean(client):
    create_response = client.post("/tasks/",json={
        "title":"Learn Python",
        "description":"Practice coding",
        "completed":False
    })

    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}",json={"completed":True})

    assert response.status_code ==200
    assert response.json()["completed"] is True

def test_put_task(client):
    create_response = client.post("/tasks/",json={
        "title":"Learn Python",
        "description":"Practice coding",
        "completed":False
    })

    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}",json={
        "title":"Learn FastAPI",
        "description":"Build APIs",
        "completed":True
    })
    print("PUT response:",response.status_code, response.json())

    assert response.status_code ==200
    print("PUT response after status check:", response.status_code, response.json())


def test_put_nonexistent_task(client):
    response = client.put("/tasks/9898",json={
        "title":"Learn FastAPI",
        "description":"Build APIs",
        "completed":True
    })

    assert response.status_code ==404
    assert response.json()["detail"]=="Task not found"

def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/9898")

    assert response.status_code ==404
    assert response.json()["detail"]=="Task not found"

def test_create_task_returns_none(client):
    with patch.object(tasks, "create_task_service", return_value=None):
        response = client.post("/tasks/",json={
            "title":"Learn Python",
            "description":"Practice coding",
            "completed":False
        })
        assert response.status_code ==500
        assert response.json()["detail"]=="Created task could not be retrieved"

def test_patch_service_returns_zero(client):
    create_response = client.post("/tasks/",json={
        "title":"Learn Python",
        "description":"Practice coding",
        "completed":False
    })

    task_id = create_response.json()["id"]

    with patch.object(tasks, "patch_task_service", return_value=0):
        response = client.patch(f"/tasks/{task_id}",json={
            "title": "Learn FastAPI"
        })
        assert response.status_code ==404
        assert response.json()["detail"]=="Task not found"


def test_put_service_returns_zero(client):
    create_response = client.post("/tasks/",json={
        "title":"Learn Python",
        "description":"Practice coding",
        "completed":False
    })

    task_id = create_response.json()["id"]

    with patch.object(tasks, "update_task_service", return_value=0):
        response = client.put(f"/tasks/{task_id}",json={
            "title":"Learn FastAPI",
            "description":"Build APIs",
            "completed":True
        })
        assert response.status_code ==404
        assert response.json()["detail"]=="Task not found"




