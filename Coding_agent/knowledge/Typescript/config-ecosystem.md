# TypeScript Config & Tooling

## tsconfig.json (Recommended)
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

## Project References (Monorepo)
```json
// root tsconfig.json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/web" }
  ]
}
```

## Build with tsup (Fast)
```bash
npm i -D tsup
# tsup src/index.ts --dts --sourcemap --format cjs,esm
```

## Vite + TypeScript
```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
})
```

## Useful Compiler Options
- `noUnusedLocals: true` — error on unused variables
- `noUnusedParameters: true` — error on unused params
- `exactOptionalPropertyTypes: true` — strict optional handling
- `noPropertyAccessFromIndexSignature: true` — force `obj['key']` for index sigs

## .d.ts Declarations
```typescript
// env.d.ts
declare namespace NodeJS {
  interface ProcessEnv { API_KEY: string; NODE_ENV: 'dev' | 'prod' }
}
// global.d.ts
declare module '*.module.css' { const classes: { readonly [key: string]: string }; export default classes }
```
