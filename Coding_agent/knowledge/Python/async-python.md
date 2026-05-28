# Async Python Patterns

## asyncio Basics
```python
import asyncio
async def fetch_data():
    await asyncio.sleep(1)
    return {"data": "done"}
result = await fetch_data()
```

## Running Async Code
```python
asyncio.run(main())  # Python 3.7+
asyncio.create_task(coro())  # schedule in background
```

## Concurrent Tasks
```python
async def main():
    tasks = [fetch_item(i) for i in range(10)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
```

## Timeouts
```python
async def fetch_with_timeout():
    try:
        result = await asyncio.wait_for(fetch(), timeout=5.0)
    except asyncio.TimeoutError:
        result = fallback
```

## aiohttp (HTTP Client)
```python
import aiohttp
async with aiohttp.ClientSession() as session:
    async with session.get("https://api.com/data") as resp:
        data = await resp.json()
```

## Async Generators
```python
async def stream_data():
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i
async for item in stream_data():
    print(item)
```

## Async Context Managers
```python
class AsyncResource:
    async def __aenter__(self): ...
    async def __aexit__(self, *exc): ...
async with AsyncResource() as res:
    await res.use()
```

## SQLAlchemy Async
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
async with AsyncSession(engine) as session:
    result = await session.execute(select(User))
```

## Event Loop
```python
loop = asyncio.get_event_loop()
loop.run_in_executor(None, blocking_fn)  # offload to thread pool
```
