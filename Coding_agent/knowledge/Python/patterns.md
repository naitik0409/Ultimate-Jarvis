# Python Project Structure

## Common Layout
```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── modules/
├── tests/
│   └── test_main.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## FastAPI Patterns
```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items")
async def create_item(item: Item):
    return item
```

## Common Snippets
- File I/O: `open(path, 'r', encoding='utf-8')`
- Async: `async def / await`
- Type hints: `def func(x: int) -> str:`
