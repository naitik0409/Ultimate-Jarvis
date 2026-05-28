# React + TypeScript Patterns

## Typed Props
```tsx
interface ButtonProps {
  label: string
  variant?: 'primary' | 'secondary'
  disabled?: boolean
  onClick: (e: React.MouseEvent<HTMLButtonElement>) => void
  children?: React.ReactNode
}
export const Button: React.FC<ButtonProps> = ({ label, variant = 'primary', ...props }) => (
  <button className={`btn-${variant}`} {...props}>{label}</button>
)
```

## useState with Type
```tsx
const [user, setUser] = useState<User | null>(null)
const [items, setItems] = useState<Item[]>([])
```

## useReducer with Type
```tsx
type Action = { type: 'add'; payload: Item } | { type: 'remove'; id: number }
const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case 'add': return { ...state, items: [...state.items, action.payload] }
    case 'remove': return { ...state, items: state.items.filter(i => i.id !== action.id) }
  }
}
```

## Typed Context
```tsx
interface AuthCtx { user: User | null; login: (e: string, p: string) => Promise<void> }
const AuthContext = createContext<AuthCtx | undefined>(undefined)
function useAuth(): AuthCtx {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be inside AuthProvider')
  return ctx
}
```

## Generic Components
```tsx
interface ListProps<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
}
function List<T>({ items, renderItem }: ListProps<T>) {
  return <div>{items.map(renderItem)}</div>
}
```

## ForwardRef with Generics
```tsx
const Input = forwardRef<HTMLInputElement, { label: string }>(({ label }, ref) => (
  <div><label>{label}</label><input ref={ref} /></div>
))
```

## Event Handlers
```tsx
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value)
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => { e.preventDefault(); submit() }
```

## Custom Hook Types
```tsx
function useLocalStorage<T>(key: string, initial: T): [T, (v: T | ((p: T) => T)) => void] { ... }
```
