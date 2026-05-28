# Node.js Database & Auth Patterns

## PostgreSQL (node-postgres)
```javascript
import pg from 'pg'
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL })
export async function query(text, params) {
  const result = await pool.query(text, params)
  return result.rows
}
```

## Prisma ORM
```javascript
// schema.prisma — model User { id Int @id @default(autoincrement); email String @unique }
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()
const users = await prisma.user.findMany({ where: { active: true }, include: { posts: true } })
const user = await prisma.user.create({ data: { email: 'a@b.com', name: 'Alice' } })
```

## Mongoose (MongoDB)
```javascript
import mongoose from 'mongoose'
mongoose.connect(process.env.MONGO_URI)
const schema = new mongoose.Schema({ title: String, createdAt: { type: Date, default: Date.now } })
schema.index({ title: 'text' })
export const Item = mongoose.model('Item', schema)
// const items = await Item.find({ title: /pattern/i }).sort({ createdAt: -1 }).limit(20)
```

## JWT Auth
```javascript
import jwt from 'jsonwebtoken'
export function generateToken(user) {
  return jwt.sign({ id: user.id, role: user.role }, process.env.JWT_SECRET, { expiresIn: '7d' })
}
export function verifyToken(token) {
  return jwt.verify(token, process.env.JWT_SECRET)
}
```

## Session Auth (express-session)
```javascript
import session from 'express-session'
app.use(session({ secret: process.env.SESSION_SECRET, resave: false, saveUninitialized: false,
  cookie: { httpOnly: true, secure: true, sameSite: 'strict', maxAge: 24 * 60 * 60 * 1000 }
}))
```

## bcrypt Password Hashing
```javascript
import bcrypt from 'bcrypt'
const hash = await bcrypt.hash(password, 12)
const match = await bcrypt.compare(plaintext, hash)
```

## Rate Limiting
```javascript
import rateLimit from 'express-rate-limit'
const limiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 100, standardHeaders: true })
app.use('/api/auth', limiter)
```
