# React State Management

## Context API (Global State)
```jsx
const Store = createContext()
function StoreProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState)
  return <Store.Provider value={{ state, dispatch }}>{children}</Store.Provider>
}
function useStore() { return useContext(Store) }
```

## Zustand (Preferred for Simplicity)
```jsx
import { create } from 'zustand'
const useStore = create((set) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
  reset: () => set({ count: 0 }),
}))
// In component: const count = useStore((s) => s.count)
```

## Redux Toolkit
```jsx
import { createSlice, configureStore } from '@reduxjs/toolkit'
const slice = createSlice({
  name: 'counter',
  initialState: { count: 0 },
  reducers: { increment(state) { state.count += 1 } },
})
const store = configureStore({ reducer: { counter: slice.reducer } })
// Provider: <Provider store={store}>
// In component: const count = useSelector(s => s.counter.count)
// dispatch(slice.actions.increment())
```

## TanStack Query (Server State)
```jsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
function usePosts() {
  return useQuery({ queryKey: ['posts'], queryFn: () => api.get('/posts') })
}
function useCreatePost() {
  const qc = useQueryClient()
  return useMutation({ mutationFn: (data) => api.post('/posts', data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['posts'] })
  })
}
```

## When to Use What
- Local: `useState` / `useReducer`
- Shared (small): Context + useReducer
- Shared (medium): Zustand
- Server state: TanStack Query
- Complex global: Redux Toolkit
