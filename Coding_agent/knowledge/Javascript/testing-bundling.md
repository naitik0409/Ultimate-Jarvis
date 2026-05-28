# JavaScript Testing & Bundling

## Vitest (Recommended)
```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest'
describe('math', () => {
  it('adds', () => expect(add(2, 3)).toBe(5))
})
```

## Mocking in Vitest
```javascript
const mockFn = vi.fn().mockReturnValue(42)
vi.spyOn(obj, 'method').mockImplementation(() => 'mocked')
vi.mock('../api', () => ({ fetchData: vi.fn(() => Promise.resolve([])) }))
```

## Jest (Compatible)
```javascript
jest.fn()
jest.spyOn(obj, 'method')
jest.mock('module', () => ({ fn: () => 'mock' }))
beforeEach(() => jest.clearAllMocks())
```

## DOM Testing (jsdom)
```javascript
import { screen, fireEvent } from '@testing-library/dom'
document.body.innerHTML = `<button>Click</button>`
fireEvent.click(screen.getByText('Click'))
```

## Vite Config
```javascript
// vite.config.js
export default defineConfig({
  plugins: [react()],
  server: { port: 3000, proxy: { '/api': 'http://localhost:8000' } },
  build: { outDir: 'dist', sourcemap: true },
})
```

## Webpack (Legacy)
```javascript
module.exports = {
  entry: './src/index.js',
  output: { path: path.resolve(__dirname, 'dist'), filename: 'bundle.js' },
  module: { rules: [{ test: /\.jsx?$/, use: 'babel-loader' }] },
  plugins: [new HtmlWebpackPlugin({ template: './public/index.html' })],
  devServer: { port: 3000 },
}
```

## ESLint + Prettier
```javascript
// eslint.config.js
export default [{
  rules: { 'no-unused-vars': 'warn', 'no-console': 'off' }
}]
// .prettierrc — { "semi": false, "singleQuote": true, "tabWidth": 2 }
```
