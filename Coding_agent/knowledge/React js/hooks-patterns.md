# React Hooks Reference

## useState
```jsx
const [count, setCount] = useState(0)
setCount(prev => prev + 1) // functional update
```

## useEffect
```jsx
useEffect(() => {
  fetchData().then(setData)
  return () => cleanup() // unmount
}, [dep]) // empty [] = mount only
```

## useRef
```jsx
const ref = useRef(null)
<input ref={ref} />
const prevValue = useRef(value) // hold mutable refs
```

## useMemo / useCallback
```jsx
const sorted = useMemo(() => sort(items), [items])
const handleClick = useCallback(() => doThing(id), [id])
```

## useContext
```jsx
const ThemeCtx = createContext('light')
// Provider: <ThemeCtx.Provider value="dark">
const theme = useContext(ThemeCtx)
```

## useReducer
```jsx
function reducer(state, action) {
  switch (action.type) {
    case 'inc': return { count: state.count + 1 }
    default: return state
  }
}
const [state, dispatch] = useReducer(reducer, { count: 0 })
```

## Custom Hook Pattern
```jsx
function useLocalStorage(key, initial) {
  const [value, setValue] = useState(() => {
    return JSON.parse(localStorage.getItem(key)) ?? initial
  })
  useEffect(() => localStorage.setItem(key, JSON.stringify(value)), [key, value])
  return [value, setValue]
}
```

## Newer Hooks (React 19)
```jsx
use(Promise)        // unwrap promise directly in render
use(Context)         // alternative to useContext
useOptimistic(state, reducer)
useFormStatus()
useTransition()      // mark state update as non-urgent
```
