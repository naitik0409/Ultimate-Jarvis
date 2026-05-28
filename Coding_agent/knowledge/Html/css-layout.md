# CSS Comprehensive Reference

## Flexbox
```css
.container { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center; align-items: center; gap: 1rem; }
.item { flex: 1 1 300px; /* grow shrink basis */ align-self: flex-start; order: -1; }
```

## CSS Grid
```css
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem; }
.grid { grid-template-areas: "header header" "sidebar main" "footer footer"; }
.header { grid-area: header; }
.item { grid-column: 1 / -1; /* span all */ }
```

## Custom Properties (CSS Variables)
```css
:root { --primary: #3b82f6; --radius: 8px; --space: 1rem; }
.button { background: var(--primary); border-radius: var(--radius); padding: var(--space); }
@media (prefers-color-scheme: dark) {
  :root { --primary: #60a5fa; --bg: #1f2937; }
}
```

## Animations
```css
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.animate { animation: fadeIn 0.3s ease-out forwards; }
.transition { transition: all 0.2s ease; }
.hover-scale:hover { transform: scale(1.05); }
```

## Responsive Breakpoints
```css
/* Mobile First */
.container { padding: 1rem; }
/* Tablet */ @media (min-width: 768px) { .container { padding: 2rem; max-width: 720px; margin: 0 auto; } }
/* Desktop */ @media (min-width: 1024px) { .container { max-width: 960px; } }
/* Wide */ @media (min-width: 1280px) { .container { max-width: 1200px; } }
```

## Modern CSS Features
```css
.container { container-type: inline-size; container-name: sidebar; }
@container sidebar (max-width: 400px) { .child { flex-direction: column; } }
:has(.active) { background: highlight; }
.clamp { font-size: clamp(1rem, 2.5vw, 2rem); }
```

## Dark Mode
```css
@media (prefers-color-scheme: dark) { body { background: #111; color: #eee; } }
[data-theme="dark"] { --bg: #1a1a2e; --text: #e0e0e0; }
```
