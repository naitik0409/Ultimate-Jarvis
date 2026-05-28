# Python Project Setup

## pyproject.toml
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.100",
    "uvicorn[standard]",
    "sqlalchemy>=2.0",
    "pydantic>=2.0",
]
[project.optional-dependencies]
dev = ["pytest>=7", "pytest-asyncio", "httpx", "coverage"]
```

## Virtual Environment
```
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
pip install -e ".[dev]"
```

## Standard Layout
```
src/
  __init__.py
  main.py
  config.py
  routers/
  models/
  schemas/
  services/
  middleware/
tests/
  conftest.py
  test_main.py
```

## Environment Variables
```python
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_url: str = "sqlite:///dev.db"
    secret_key: str = "dev-secret"
    debug: bool = True
    class Config: env_file = ".env"
settings = Settings()
```

## Dependency Management
- `requirements.txt` for pinned deps
- `pyproject.toml` for metadata + optional dev/test deps
- `pip-compile` from pip-tools for lockfiles
