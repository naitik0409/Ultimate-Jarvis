# React Routing & Auth

## React Router Setup
```jsx
import { BrowserRouter, Routes, Route, Link } from 'react-router'
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/items/:id" element={<ItemDetail />} />
      </Routes>
    </BrowserRouter>
  )
}
```

## Navigation
```jsx
import { useNavigate, useParams, useSearchParams } from 'react-router'
const navigate = useNavigate()
navigate('/dashboard', { replace: true }) // replace history
const { id } = useParams()
const [searchParams, setSearchParams] = useSearchParams()
searchParams.get('page')
```

## Protected Routes
```jsx
function ProtectedRoute({ children }) {
  const user = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return children
}
// Usage: <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
```

## Auth Context
```jsx
const AuthContext = createContext(null)
function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const login = async (email, pass) => {
    const u = await api.login(email, pass)
    setUser(u); localStorage.setItem('token', u.token)
  }
  const logout = () => { setUser(null); localStorage.removeItem('token') }
  return <AuthContext.Provider value={{ user, login, logout }}>{children}</AuthContext.Provider>
}
function useAuth() { return useContext(AuthContext) }
```

## Lazy Loading
```jsx
const Dashboard = lazy(() => import('./Dashboard'))
<Suspense fallback={<Spinner />}>
  <Dashboard />
</Suspense>
```
