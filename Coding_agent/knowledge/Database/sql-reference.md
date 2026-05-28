# SQL Comprehensive Reference

## DDL (Data Definition)
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(100) NOT NULL,
  role VARCHAR(20) DEFAULT 'user',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role_created ON users(role, created_at DESC);
ALTER TABLE users ADD COLUMN avatar_url TEXT;
ALTER TABLE users DROP COLUMN avatar_url;
```

## DML (Data Manipulation)
```sql
INSERT INTO users (email, name) VALUES ($1, $2) RETURNING *;
SELECT id, name FROM users WHERE role = 'admin' ORDER BY created_at DESC LIMIT 50 OFFSET 0;
UPDATE users SET name = $1, updated_at = NOW() WHERE id = $2 RETURNING *;
DELETE FROM users WHERE id = $1;
```

## Joins
```sql
-- INNER: only matching rows
SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id;
-- LEFT: all users even if no orders
SELECT u.name, COUNT(o.id) FROM users u LEFT JOIN orders o ON u.id = o.user_id GROUP BY u.id;
-- SELF: employees and their managers
SELECT e.name, m.name AS manager FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;
```

## Aggregation & Grouping
```sql
SELECT role, COUNT(*), AVG(age), MIN(created_at), MAX(created_at)
FROM users GROUP BY role HAVING COUNT(*) > 5;
```

## Window Functions
```sql
SELECT name, salary, RANK() OVER (ORDER BY salary DESC) as rank,
  LAG(salary) OVER (ORDER BY salary) as prev_salary,
  AVG(salary) OVER (PARTITION BY department) as dept_avg
FROM employees;
```

## CTE (Common Table Expression)
```sql
WITH active_users AS (
  SELECT * FROM users WHERE last_login > NOW() - INTERVAL '30 days'
)
SELECT au.name, COUNT(o.id) as orders
FROM active_users au LEFT JOIN orders o ON au.id = o.user_id
GROUP BY au.id;
```

## Transactions
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT; -- or ROLLBACK;
```
