# Node.js Project Structure

## Recommended Layout
```
src/
  app.js         — express app setup (middleware, routes)
  server.js      — http server entry point
  config/
    index.js     — env vars, exports config object
    db.js        — database connection setup
  routes/
    index.js     — route aggregator
    users.js     — user routes
    items.js     — items routes
  controllers/
    users.js     — request handlers
  models/
    user.js      — data models / schemas
  middleware/
    auth.js      — auth middleware
    error.js     — error handler
  services/
    email.js     — business logic
  utils/
    logger.js    — shared utilities
tests/
  routes/
  middleware/
```

## Entry Point Pattern
```javascript
// server.js
import app from './app.js'
const PORT = process.env.PORT || 3000
const server = app.listen(PORT, () => console.log(`Server on :${PORT}`))
process.on('SIGTERM', () => { server.close(() => process.exit(0)) })
```

## Config Pattern
```javascript
// config/index.js
import dotenv from 'dotenv'
dotenv.config()
export default {
  port: process.env.PORT || 3000,
  db: { url: process.env.DATABASE_URL, pool: 10 },
  jwt: { secret: process.env.JWT_SECRET, expiresIn: '7d' },
  cors: { origin: process.env.CORS_ORIGIN?.split(',') || '*' },
}
```

## package.json Scripts
```json
{
  "scripts": {
    "dev": "node --watch src/server.js",
    "start": "node src/server.js",
    "test": "vitest",
    "lint": "eslint src/"
  },
  "type": "module"
}
```

## npm init Best Practices
- `"type": "module"` — ES modules by default
- `engines: { "node": ">=18" }` — minimum node version
- `.env` for secrets, `.env.example` for reference
