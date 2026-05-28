# Node.js Testing & Deployment

## Vitest for Node
```javascript
import { describe, it, expect, vi, beforeAll } from 'vitest'
import request from 'supertest'
import app from '../app.js'
describe('GET /api/items', () => {
  it('returns 200 with items', async () => {
    const res = await request(app).get('/api/items')
    expect(res.status).toBe(200)
    expect(res.body).toHaveProperty('items')
  })
})
```

## Mocking Database in Tests
```javascript
vi.mock('../db.js', () => ({
  query: vi.fn().mockResolvedValue([{ id: 1, name: 'test' }])
}))
// or use testcontainers for real DB
```

## Dockerfile
```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "src/server.js"]
```

## docker-compose.yml
```yaml
services:
  app:
    build: .
    ports: ["3000:3000"]
    env_file: .env
    depends_on: [db]
  db:
    image: postgres:16-alpine
    environment: POSTGRES_DB=app POSTGRES_PASSWORD=secret
    volumes: [pgdata:/var/lib/postgresql/data]
volumes: { pgdata: }
```

## Health Check
```javascript
app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime(), timestamp: Date.now() })
})
```

## PM2 (Production Process Manager)
```json
// ecosystem.config.json
{ "apps": [{
  "name": "app", "script": "src/server.js",
  "instances": "max", "exec_mode": "cluster",
  "env": { "NODE_ENV": "production" }
}]}
```

## Logging (pino)
```javascript
import pino from 'pino'
const logger = pino({ level: process.env.LOG_LEVEL || 'info' })
logger.info({ userId, action }, 'user performed action')
```
