# Express.js Patterns

## Basic App
```javascript
import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
const app = express()
app.use(helmet())
app.use(cors())
app.use(express.json({ limit: '1mb' }))
```

## Router Pattern
```javascript
import { Router } from 'express'
const router = Router()
router.get('/', async (req, res, next) => {
  try {
    const items = await db.findMany()
    res.json(items)
  } catch (err) { next(err) }
})
export default router
// app.use('/api/items', router)
```

## Route Parameters
```javascript
router.get('/:id', async (req, res) => {
  const item = await db.findById(req.params.id)
  if (!item) return res.status(404).json({ error: 'Not found' })
  res.json(item)
})
```

## Middleware
```javascript
const auth = (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '')
  if (!token) return res.status(401).json({ error: 'Unauthorized' })
  req.user = verify(token)
  next()
}
app.use('/api', auth) // protect all /api routes
```

## Error Middleware
```javascript
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === 'production' ? 'Server Error' : err.message
  })
})
```

## Async Handler Wrapper
```javascript
const asyncHandler = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next)
router.get('/', asyncHandler(async (req, res) => {
  const data = await fetchData()
  res.json(data)
}))
```

## File Upload (Multer)
```javascript
import multer from 'multer'
const upload = multer({ dest: 'uploads/', limits: { fileSize: 5 * 1024 * 1024 } })
router.post('/upload', upload.single('file'), (req, res) => {
  res.json({ path: req.file.path })
})
```
