import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from main import app  # Adjust the import according to your project structure
from src.models.user import User as UserModel
from src.util.dependencies import get_db
from src.auth.auth import authenticate_user, create_access_token, get_password_hash
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from src.config.database import Base
import uuid
from sqlalchemy.ext.declarative import declarative_base

# Define your test database URL (adjust as needed)
TEST_DATABASE_URL = "postgresql://test_user:test_pass@test-db:5432/test_postgres"

@pytest.fixture(scope="session")
def test_engine():
    """Set up the test engine, create tables, and run migrations."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)  # Ensure that your Base has all ORM models registered.
    # Run migrations if any
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")
    yield engine
    # Clean up: drop all to clean the database
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture(scope="module")
def client(test_engine):
    """Create a test client that uses the test database."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def authenticated_user(client):
    """Fixture to add an authentication token to the test client headers."""
    db = next(client.app.dependency_overrides[get_db]())

    # Create a new user in the test database
    username = f"testuser_{uuid.uuid4()}"
    password = "securepassword"
    hashed_password = get_password_hash(password)
    user = UserModel(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()  # This commit is okay because each test runs in its transaction managed by client fixture

    # Authenticate the test user and create a token
    token = create_access_token(data={"sub": username})
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client

    # Revert changes by rolling back the transaction after each function
    # Since the session is managed by the `client` fixture and overridden `get_db`, the teardown happens there

@pytest.fixture(scope="function")
def db_session(test_engine):
    """Creates a new database session for tests, ensuring each test is isolated."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()
