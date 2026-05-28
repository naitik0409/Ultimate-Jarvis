# Advanced TypeScript Types

## Utility Types
```typescript
Partial<T>     // all optional
Required<T>    // all required
Pick<T, K>     // subset of keys
Omit<T, K>     // exclude keys
Record<K, V>   // object from keys to values
Readonly<T>    // all readonly
Exclude<T, U>  // union minus members
Extract<T, U>  // intersection of union members
NonNullable<T> // removes null/undefined
ReturnType<F>  // return type of function
Parameters<F>  // tuple of parameter types
Awaited<T>     // unwrap promises
```

## Conditional Types
```typescript
type IsString<T> = T extends string ? true : false
type Result = IsString<'hello'> // true
type ArrayElement<T> = T extends (infer U)[] ? U : never
type El = ArrayElement<number[]> // number
```

## Mapped Types
```typescript
type Readonly<T> = { readonly [K in keyof T]: T[K] }
type Optional<T> = { [K in keyof T]?: T[K] }
type Nullable<T> = { [K in keyof T]: T[K] | null }
type Getters<T> = { [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K] }
```

## Template Literal Types
```typescript
type EventName = `on${Capitalize<string>}`
type Color = 'red' | 'blue'
type Variant = `${Color}-${number | 'dark' | 'light'}`
type ApiPath = `/api/${string}`
```

## Branded Types
```typescript
type Brand<K, T> = K & { __brand: T }
type UserId = Brand<number, 'UserId'>
type Email = Brand<string, 'Email'>
function getUser(id: UserId) { ... }
getUser(123 as UserId) // must be explicitly cast
```

## Discriminated Unions
```typescript
type Result<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
  | { status: 'loading' }
function handle(r: Result<number>) {
  if (r.status === 'success') r.data // narrowed
}
```

## Type Guards
```typescript
function isError(r: Result<unknown>): r is { status: 'error'; error: string } {
  return r.status === 'error'
}
```
