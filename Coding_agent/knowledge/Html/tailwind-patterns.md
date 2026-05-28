# Tailwind CSS Patterns

## Utility-First Approach
```html
<div class="flex items-center justify-between rounded-xl border bg-white p-6 shadow-sm dark:bg-gray-800 dark:border-gray-700">
  <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Title</h2>
  <button class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors">
    Action
  </button>
</div>
```

## Component Extraction
```html
<!-- Reuse via @apply in CSS or inline utilities -->
<style>
  .btn-primary { @apply rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 transition-colors; }
  .card { @apply rounded-xl border bg-white p-6 shadow-sm dark:bg-gray-800 dark:border-gray-700; }
</style>
```

## Responsive Design
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  <!-- 1 col on mobile, 2 on sm, 3 on lg, 4 on xl -->
</div>
<div class="text-sm md:text-base lg:text-lg">
  <!-- responsive font size -->
</div>
```

## Dark Mode
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
  <p class="text-gray-600 dark:text-gray-400">Content</p>
</div>
```

## Common Patterns
```html
<!-- Centered container -->
<div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">...</div>
<!-- Stacked layout with gap -->
<div class="flex flex-col gap-4">...</div>
<!-- Card grid -->
<div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">...</div>
<!-- Form input -->
<input class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 dark:border-gray-600 dark:bg-gray-700">
```

## Custom Config (tailwind.config.js)
```javascript
export default {
  content: ['./src/**/*.{js,jsx,ts,tsx,html}'],
  darkMode: 'class', // or 'media'
  theme: { extend: { colors: { brand: { 500: '#3b82f6' } } } },
}
```
