# JavaScript DOM & Web APIs

## DOM Selection
```javascript
document.querySelector('.class')       // first match
document.querySelectorAll('div.item')  // NodeList (forEach works)
document.getElementById('id')
document.getElementsByClassName('cls')
```

## DOM Manipulation
```javascript
el.textContent = 'text'         // safe, no HTML parsing
el.innerHTML = '<b>bold</b>'    // XSS risk — sanitize first
el.classList.add('active')
el.classList.remove('hidden')
el.classList.toggle('visible')
el.setAttribute('data-id', '123')
el.dataset.id                   // -> '123'
```

## Event Handling
```javascript
el.addEventListener('click', handler, { once: true })
el.removeEventListener('click', handler)
// Event delegation:
parent.addEventListener('click', (e) => {
  if (e.target.matches('.item')) handleItem(e.target)
})
```

## Fetch API
```javascript
const resp = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data),
  credentials: 'include',  // for cookies
})
if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
const result = await resp.json()
```

## Web Storage
```javascript
localStorage.setItem('key', JSON.stringify(value))
JSON.parse(localStorage.getItem('key'))
sessionStorage.setItem('key', value)  // cleared on tab close
```

## Canvas
```javascript
const ctx = canvas.getContext('2d')
ctx.fillStyle = 'red'
ctx.fillRect(10, 10, 100, 100)
ctx.beginPath(); ctx.arc(50, 50, 30, 0, Math.PI * 2); ctx.fill()
```

## Intersection Observer
```javascript
const obs = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) loadMore() })
}, { threshold: 0.1 })
obs.observe(sentinel)
```
