import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.database import get_connection
from app.main import app, get_db_path


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path/"test.db"
    connection =get_connection(db_path)
    connection.execute("""
                       CREATE TABLE tasks (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           description TEXT NOT NULL,
                           completed INTEGER NOT NULL DEFAULT 0)""")
   
    connection.close()
    yield db_path
    
    
@pytest.fixture
def override_get_db_path(test_db):
    def _override_get_db_path():
        return test_db
    
    return _override_get_db_path

@pytest.fixture
def client(override_get_db_path):
    app.dependency_overrides[get_db_path]=override_get_db_path
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.clear()
    
    