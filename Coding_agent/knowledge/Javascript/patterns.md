# JavaScript Patterns

## Async/Await
```javascript
async function fetchData(url) {
  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw error
  }
}
```

## ES6+ Features
- Destructuring: `const { name, age } = obj`
- Spread: `const copy = { ...original }`
- Optional chaining: `obj?.prop?.nested`
- Nullish coalescing: `value ?? defaultValue`
- Arrow functions: `const fn = (x) => x * 2`
- Modules: `import/export`

## DOM Helpers
```javascript
document.querySelector('.class')
document.getElementById('id')
element.addEventListener('click', handler)
element.textContent = 'text'
```
