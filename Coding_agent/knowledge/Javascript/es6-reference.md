# ES6+ JavaScript Reference

## Variables
```javascript
const PI = 3.14   // block-scoped, cannot reassign
let count = 0     // block-scoped, can reassign
```

## Destructuring
```javascript
const { name, age, ...rest } = obj
const [first, second, ...tail] = arr
function fn({ id, title } = {}) {} // param destructuring with default
```

## Spread & Rest
```javascript
const merged = { ...a, ...b }
const arr = [...set, ...other]
const sorted = [...items].sort()
function sum(...nums) { return nums.reduce((a, b) => a + b, 0) }
```

## Optional Chaining & Nullish
```javascript
user?.address?.street           // undefined if any nullish
data ?? fallback                // fallback only for null/undefined
obj?.prop ?? 'default'
```

## Array Methods
```javascript
items.map(x => x * 2)
items.filter(x => x > 0)
items.reduce((sum, x) => sum + x, 0)
items.find(x => x.id === target)
items.some(x => x > 10)         // boolean
items.every(x => x > 0)         // boolean
items.flatMap(x => [x, x * 2])  // map + flatten
```

## Modules
```javascript
// export.js — export const fn = () => {}; export default class {}
// import.js — import defaultExport, { named1, named2 } from './export.js'
// dynamic: const mod = await import('./module.js')
```

## Promise Patterns
```javascript
Promise.all([p1, p2])           // all settle (fail-fast)
Promise.allSettled([p1, p2])    // all settle (never fails)
Promise.race([p1, p2])          // first to settle
Promise.any([p1, p2])           // first to fulfill
```
