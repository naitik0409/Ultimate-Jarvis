# ORM Patterns

## SQLAlchemy 2.0 (Python)
```python
from sqlalchemy import create_engine, select, ForeignKey
from sqlalchemy.orm import declarative_base, Session, Mapped, mapped_column, relationship
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    posts: Mapped[list['Post']] = relationship(back_populates='author')
class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped['User'] = relationship(back_populates='posts')
engine = create_engine('postgresql://user:pass@localhost/db')
Base.metadata.create_all(engine)
with Session(engine) as session:
    user = session.execute(select(User).where(User.id == 1)).scalar_one()
    session.add(User(name='Alice')); session.commit()
```

## Prisma (Node.js/TS)
```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}
model Post {
  id       Int    @id @default(autoincrement())
  title    String
  content  String?
  author   User   @relation(fields: [authorId], references: [id])
  authorId Int
}
```
```typescript
const user = await prisma.user.findUnique({ where: { email }, include: { posts: true } })
const users = await prisma.user.findMany({ skip: 0, take: 20, orderBy: { createdAt: 'desc' } })
await prisma.user.update({ where: { id }, data: { name: 'New Name' } })
```

## Mongoose (MongoDB/Node.js)
```javascript
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true, lowercase: true },
  name: { type: String, trim: true },
  role: { type: String, enum: ['user', 'admin'], default: 'user' },
}, { timestamps: true })
userSchema.index({ name: 'text', email: 'text' })
const User = mongoose.model('User', userSchema)
await User.create({ email: 'a@b.com', name: 'Alice' })
await User.find({ role: 'admin' }).sort({ createdAt: -1 }).limit(10).lean()
await User.findByIdAndUpdate(id, { $set: { name } }, { new: true })
```
