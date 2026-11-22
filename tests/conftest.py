
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_connection
from app.db_dependencies import get_db
from app.main import app
from app.models import Base


@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test.db"

    connection = get_connection(db_path)
    connection.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    connection.close()

    yield db_path


@pytest.fixture
def sqlalchemy_engine(tmp_path):
    database_file = tmp_path / "sqlalchemy_test.db"

    test_engine = create_engine(
        f"sqlite:///{database_file}",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=test_engine)

    yield test_engine

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def sqlalchemy_client(sqlalchemy_engine):
    TestingSessionLocal = sessionmaker(
        bind=sqlalchemy_engine,
        autoflush=False,
        autocommit=False,
    )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    previous_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        if previous_override is not None:
            app.dependency_overrides[get_db] = previous_override
        else:
            app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def sqlalchemy_db(sqlalchemy_engine):
    TestingSessionLocal = sessionmaker(
        bind=sqlalchemy_engine,
        autoflush=False,
        autocommit=False,
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()



@pytest.fixture
def client(sqlalchemy_client):
    return sqlalchemy_client
