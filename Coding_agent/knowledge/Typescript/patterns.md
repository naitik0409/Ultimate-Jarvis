# TypeScript Patterns

## Basic Types
```typescript
type User = {
  id: number
  name: string
  email: string
  role: 'admin' | 'user'
}

interface ApiResponse<T> {
  data: T
  status: number
  message: string
}
```

## Generics
```typescript
function getFirst<T>(arr: T[]): T | undefined {
  return arr[0]
}
```

## React with TypeScript
```tsx
interface Props {
  title: string
  count?: number
  onClick: (id: string) => void
}

const Component: React.FC<Props> = ({ title, count = 0, onClick }) => {
  return <button onClick={() => onClick(title)}>{title} ({count})</button>
}
```

## tsconfig.json
```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2020",
    "module": "ESNext",
    "jsx": "react-jsx"
  }
}
```
