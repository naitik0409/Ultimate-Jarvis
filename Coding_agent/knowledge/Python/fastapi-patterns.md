# FastAPI Patterns

## Basic App
```python
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
app = FastAPI(title="API", version="1.0.0")
```

## Dependency Injection
```python
from fastapi import Depends, Header, HTTPException
async def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    user = verify_token(token)
    if not user: raise HTTPException(401, "Invalid token")
    return user
@app.get("/me")
async def read_me(user = Depends(get_current_user)):
    return user
```

## CRUD Routes
```python
@app.get("/items", response_model=list[ItemOut])
async def list_items(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return db.query(Item).offset(skip).limit(limit).all()
@app.post("/items", response_model=ItemOut, status_code=201)
async def create_item(item: ItemCreate, db=Depends(get_db)):
    db_item = Item(**item.model_dump())
    db.add(db_item); db.commit(); db.refresh(db_item)
    return db_item
```

## Error Handling
```python
from fastapi import Request
from fastapi.responses import JSONResponse
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

## Background Tasks
```python
from fastapi import BackgroundTasks
def send_email(user_id: int): ...
@app.post("/register")
async def register(user: UserCreate, tasks: BackgroundTasks):
    tasks.add_task(send_email, user.id)
    return {"ok": True}
```

## WebSocket
```python
from fastapi import WebSocket, WebSocketDisconnect
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect: pass
```
