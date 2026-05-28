# JavaScript Async Patterns

## Promises
```javascript
const promise = new Promise((resolve, reject) => {
  setTimeout(() => resolve('done'), 1000)
})
promise.then(console.log).catch(console.error).finally(() => cleanup())
```

## Async/Await
```javascript
async function fetchUser(id) {
  const resp = await fetch(`/api/users/${id}`)
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
  return resp.json()
}
```

## Error Handling
```javascript
async function safeFetch(url) {
  try {
    return await fetchWithTimeout(url, 5000)
  } catch (err) {
    console.error('Fetch failed:', err)
    return fallbackData
  }
}
```

## Parallel Execution
```javascript
async function loadDashboard() {
  const [user, posts, notifications] = await Promise.all([
    fetchUser(), fetchPosts(), fetchNotifications()
  ])
  return { user, posts, notifications }
}
```

## Event Loop
```javascript
// Microtasks (Promise, queueMicrotask) run before next macrotask
// Macrotasks (setTimeout, setInterval, I/O, DOM events)
console.log(1)
setTimeout(() => console.log(2), 0) // macrotask — last
Promise.resolve().then(() => console.log(3)) // microtask — between
console.log(4)
// Output: 1, 4, 3, 2
```

## AbortController
```javascript
const ac = new AbortController()
setTimeout(() => ac.abort(), 3000)
fetch(url, { signal: ac.signal }).catch(err => {
  if (err.name === 'AbortError') console.log('cancelled')
})
```

## async Generators
```javascript
async function* streamPages(url) {
  let page = 1
  while (true) {
    const data = await fetch(`${url}?page=${page}`).then(r => r.json())
    if (!data.length) break
    yield data
    page++
  }
}
for await (const page of streamPages('/api/items')) { ... }
```
