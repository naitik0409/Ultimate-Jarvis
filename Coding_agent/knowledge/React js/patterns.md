# React Component Patterns

## Functional Component
```jsx
import { useState, useEffect } from 'react'

export default function Component({ prop }) {
  const [state, setState] = useState(null)

  useEffect(() => {
    // side effect
  }, [])

  return <div>{state}</div>
}
```

## Custom Hook Pattern
```jsx
function useCustomHook(param) {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetchData(param).then(setData)
  }, [param])
  return data
}
```

## State Management
- Local: `useState`, `useReducer`
- Global: Context API, Zustand, Redux

## Styling
- CSS Modules: `import styles from './Component.module.css'`
- Tailwind: className utilities
- styled-components: tagged template literals
