from fastapi.testclient import TestClient

from app.main import app

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
    
    assert response.status_code ==200
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
    response = client.patch(f"/tasks/{task_id}",json={"completed":True})
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"]=="Learn Python"
    assert data["description"] =="Practice coding"
    assert data["completed"] is True
    
    
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