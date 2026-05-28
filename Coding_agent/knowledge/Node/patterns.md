# Node.js Patterns

## Express Server
```javascript
const express = require('express')
const app = express()

app.use(express.json())

app.get('/api/items', (req, res) => {
  res.json({ items: [] })
})

app.listen(3000, () => console.log('Server running on port 3000'))
```

## Project Structure
```
project/
├── src/
│   ├── routes/
│   ├── controllers/
│   ├── models/
│   ├── middleware/
│   └── app.js
├── package.json
└── .env
```

## Common package.json scripts
```json
{
  "scripts": {
    "dev": "node --watch src/app.js",
    "start": "node src/app.js",
    "test": "jest"
  }
}
```
