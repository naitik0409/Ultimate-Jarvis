# Python Testing Patterns (pytest)

## Basic Test
```python
import pytest
def test_add(): assert add(2, 3) == 5
```

## Fixtures
```python
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
def test_create_user(db_session):
    user = User(name="test")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
```

## Async Tests
```python
import pytest
@pytest.mark.asyncio
async def test_async_func():
    result = await fetch_data()
    assert result is not None
```

## Mocking
```python
from unittest.mock import Mock, patch, AsyncMock
@patch("mymodule.external_api")
def test_with_mock(mock_api):
    mock_api.return_value = {"data": "mocked"}
    result = my_function()
    mock_api.assert_called_once()
```

## Parametrized
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4), (0, 0), (-1, 1)
])
def test_square(input, expected):
    assert square(input) == expected
```

## FastAPI Test Client
```python
from fastapi.testclient import TestClient
client = TestClient(app)
def test_read_main():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []
```

## Fixture Scopes
- `function` (default): fresh per test
- `class`: once per class
- `module`: once per module
- `session`: once per run
