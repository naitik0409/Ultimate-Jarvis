# HTML5 Reference

## Document Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Page description for SEO">
  <title>Page Title</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>...</body>
</html>
```

## Forms
```html
<form action="/api/submit" method="POST" novalidate>
  <label for="email">Email</label>
  <input type="email" id="email" name="email" required autocomplete="email">
  <label for="message">Message</label>
  <textarea id="message" name="message" rows="4" required></textarea>
  <select name="category" required>
    <option value="">Select...</option>
    <option value="a">Option A</option>
  </select>
  <button type="submit">Submit</button>
</form>
```

## Accessibility (a11y)
```html
<nav aria-label="Main navigation" role="navigation">...</nav>
<button aria-label="Close" aria-expanded="false">✕</button>
<div role="alert" aria-live="polite">Error message</div>
<img src="photo.jpg" alt="Description of image" />
```

## SEO Meta Tags
```html
<meta name="description" content="...">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://example.com/page">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="https://example.com/image.jpg">
<meta name="twitter:card" content="summary_large_image">
```

## Modern HTML Best Practices
- Use `<dialog>` for modals (no JS needed for show/close)
- Use `<details>` / `<summary>` for accordions
- Use `<template>` for reusable HTML fragments
- Use `loading="lazy"` on `<img>` for deferred loading
- Use `decoding="async"` on `<img>` for faster paint
- Use `<picture>` with `<source>` for responsive images
