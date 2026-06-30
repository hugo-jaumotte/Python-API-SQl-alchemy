import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import models

# Create an SQLite in-memory database for the tests.

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    models.Base.metadata.create_all(bind=engine)

    yield engine

    engine.dispose()

# Give a session maker for each test.
@pytest.fixture(scope="function")
def test_db(test_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    yield TestingSessionLocal