# React Testing & Styling

## React Testing Library
```jsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
test('increments on click', async () => {
  render(<Counter />)
  const btn = screen.getByRole('button', { name: /increment/i })
  await userEvent.click(btn)
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
})
```

## Mocking API Calls
```jsx
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
const server = setupServer(http.get('/api/data', () => HttpResponse.json({ items: [] })))
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## Async Assertions
```jsx
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument()
})
// findBy* = waitFor + query
const el = await screen.findByText('Loaded')
```

## Tailwind CSS
```jsx
export default function Card({ title, children }) {
  return (
    <div className="rounded-xl border bg-white p-6 shadow-sm dark:bg-gray-800">
      <h2 className="mb-2 text-lg font-semibold">{title}</h2>
      <div className="text-gray-600 dark:text-gray-300">{children}</div>
    </div>
  )
}
```

## CSS Modules
```jsx
import styles from './Card.module.css'
<div className={styles.card}>{children}</div>
```

## styled-components
```jsx
import styled from 'styled-components'
const Button = styled.button`
  background: ${p => p.$variant === 'primary' ? 'blue' : 'gray'};
  padding: 8px 16px;
  border-radius: 6px;
`
```
