# Database Schema Design

## Normalization Principles
- **1NF**: Atomic columns, no repeating groups
- **2NF**: All non-key columns depend on full primary key
- **3NF**: No transitive dependencies (non-key depends on non-key)
- In practice: 3NF is usually sufficient; denormalize for read performance

## Relationships
```sql
-- One-to-Many: user has many posts (FK on posts.user_id)
CREATE TABLE posts (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users(id), ...);
-- Many-to-Many: posts and tags
CREATE TABLE post_tags (post_id INTEGER REFERENCES posts(id), tag_id INTEGER REFERENCES tags(id), PRIMARY KEY (post_id, tag_id));
```

## Indexing Strategy
```sql
-- B-tree: equality + range queries (default)
CREATE INDEX idx_users_email ON users(email);
-- Composite: column order matters — put high-selectivity first
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);
-- Partial: only index subset
CREATE INDEX idx_active_orders ON orders(status) WHERE status = 'active';
-- Unique: enforce + fast lookup
CREATE UNIQUE INDEX idx_users_email ON users(email);
```

## Query Optimization
- Use `EXPLAIN ANALYZE` to check query plans
- Avoid `SELECT *` — fetch only needed columns
- Use `LIMIT` + `OFFSET` for pagination (or keyset pagination for large datasets)
- Keyset pagination: `WHERE id > $1 ORDER BY id LIMIT 100` (more efficient than OFFSET)
- Add missing indexes based on WHERE + JOIN + ORDER BY columns

## Migrations (Alembic)
```python
# alembic init alembic
# alembic revision --autogenerate -m "add users table"
# alembic upgrade head
```

## Naming Conventions
- Tables: plural_snake_case (`users`, `order_items`)
- Columns: singular_snake_case (`created_at`)
- PK: `id`
- FK: `referenced_table_singular_id` (`user_id`)
- Indexes: `idx_table_column` / `idx_table_col1_col2`
- Unique constraints: `uq_table_column`
