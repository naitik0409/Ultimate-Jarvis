# Database Patterns

## SQL Queries
```sql
-- Create
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- CRUD
INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *;
SELECT * FROM users WHERE id = $1;
UPDATE users SET name = $1 WHERE id = $2 RETURNING *;
DELETE FROM users WHERE id = $1;

-- Joins
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'active';
```

## ORM Patterns (SQLAlchemy)
```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
```

## MongoDB (Mongoose)
```javascript
const schema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, unique: true }
})
const User = mongoose.model('User', schema)
```
