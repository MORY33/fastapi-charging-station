import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from main import app
from src.models.user import User as UserModel
from src.util.dependencies import get_db
from src.auth.auth import authenticate_user, create_access_token, get_password_hash
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from src.config.database import Base
import uuid
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from src.models.charging_station import StationTypeEnum, CurrentType, ChargingStationType

TEST_DATABASE_URL = "postgresql://test_user:test_pass@test-db:5432/test_postgres"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Run migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="session")
def session_override(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return override_get_db

@pytest.fixture(scope="module")
def client(session_override):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def authenticated_user(client):
    db = next(client.app.dependency_overrides[get_db]())

    # Create a new user
    username = f"testuser_{uuid.uuid4()}"
    password = "securepassword"
    hashed_password = get_password_hash(password)
    user = UserModel(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()

    # Authenticate the test user and create a token
    token = create_access_token(data={"sub": username})
    client.headers.update({"Authorization": f"Bearer {token}"})

    yield client


@pytest.fixture(scope="function")
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def charging_station_type(db_session):
    existing_type = db_session.query(ChargingStationType).filter_by(name=StationTypeEnum.TYPE_A).first()
    if not existing_type:
        test_type = ChargingStationType(
            id=uuid.uuid4(),
            name=StationTypeEnum.TYPE_A,
            plug_count=4,
            efficiency=0.88,
            current_type=CurrentType.AC
        )
        db_session.add(test_type)
        db_session.commit()
        return test_type
    else:
        return existing_type
