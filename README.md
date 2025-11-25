# lookuply.info

**Landing page for Lookuply - Privacy-first search engine**

Live at: [lookuply.info](https://lookuply.info)

---

## Overview

This repository contains the source code for the Lookuply landing page - a simple, fast, and beautiful introduction to our privacy-first search engine supporting all 24 EU languages.

### Features

- **Lightning Fast**: Static HTML/CSS/JS
- **Responsive Design**: Works on all devices
- **Minimal Dependencies**: No heavy frameworks
- **SEO Optimized**: Meta tags, OpenGraph, structured data
- **Multi-language**: Landing page in 24 languages
- **Open Source**: MIT License

---

## Live Site

🌐 **[lookuply.info](https://lookuply.info)**

---

## Technology Stack

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid/Flexbox
- **Vanilla JavaScript**: No frameworks
- **No tracking**: No analytics, no cookies
- **Static hosting**: Cloudflare Pages / Nginx

---

## Project Structure

```
lookuply.info/
├── index.html           # Main landing page
├── css/
│   ├── style.css        # Main stylesheet
│   └── responsive.css   # Mobile styles
├── js/
│   ├── main.js          # Main JavaScript
│   └── language.js      # Language switcher
├── images/
│   ├── logo.svg         # Lookuply logo
│   └── hero.webp        # Hero image
├── locales/             # Translations (24 languages)
│   ├── en.json
│   ├── de.json
│   ├── fr.json
│   └── ...
└── public/              # Static assets
    ├── favicon.ico
    ├── robots.txt
    └── sitemap.xml
```

---

## Local Development

### Prerequisites

```bash
- Web browser
- Local web server (optional)
```

### Running Locally

**Option 1: Python SimpleHTTPServer**
```bash
# Clone repository
git clone https://github.com/lookuply/lookuply.info.git
cd lookuply.info

# Start server
python3 -m http.server 8000

# Open http://localhost:8000
```

**Option 2: Node.js http-server**
```bash
npm install -g http-server
http-server -p 8000

# Open http://localhost:8000
```

**Option 3: Just open the file**
```bash
# Simply open index.html in your browser
open index.html  # macOS
xdg-open index.html  # Linux
```

---

## Content Sections

### 🏠 Hero Section

```html
<section class="hero">
  <h1>Search the Web with Privacy</h1>
  <p>Open-source search engine supporting 24 EU languages</p>
  <a href="https://search.lookuply.info" class="cta-button">
    Try Lookuply
  </a>
</section>
```

### ✨ Features

- **Privacy-First**: No tracking, no data collection
- **24 Languages**: All EU languages from day one
- **Open Source**: Transparent, auditable code
- **API Access**: Build your own applications
- **Ad-Free**: Clean, focused search experience

### 🌍 Language Support

Visual showcase of all 24 supported languages with flags.

### 🚀 Getting Started

Quick links to:
- Try the search
- API documentation
- GitHub repositories
- Community

### 📞 Contact

- Email: hello@lookuply.info
- GitHub: [@lookuply](https://github.com/lookuply)
- Status: [status.lookuply.info](https://status.lookuply.info)

---

## Design Guidelines

### Color Palette

```css
:root {
  --primary-color: #2563EB;    /* Blue */
  --secondary-color: #10B981;  /* Green */
  --text-dark: #1F2937;
  --text-light: #6B7280;
  --background: #FFFFFF;
  --surface: #F9FAFB;
}
```

### Typography

```css
font-family:
  -apple-system, BlinkMacSystemFont,
  'Segoe UI', 'Roboto', 'Oxygen',
  'Ubuntu', 'Cantarell', 'Fira Sans',
  'Droid Sans', 'Helvetica Neue',
  sans-serif;
```

### Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 640px) { }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }
```

---

## SEO Configuration

### Meta Tags

```html
<meta name="description" content="Privacy-first search engine supporting 24 EU languages. Open source, no tracking, ad-free.">
<meta name="keywords" content="search engine, privacy, open source, EU languages">
```

### OpenGraph

```html
<meta property="og:title" content="Lookuply - Privacy-First Search">
<meta property="og:description" content="Open-source search engine supporting 24 EU languages">
<meta property="og:image" content="https://lookuply.info/images/og-image.png">
<meta property="og:url" content="https://lookuply.info">
```

### Structured Data

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Lookuply",
  "url": "https://lookuply.info",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://search.lookuply.info/?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

---

## Translations

### Adding New Language

```bash
# 1. Create translation file
cp locales/en.json locales/sk.json

# 2. Translate all strings
{
  "hero": {
    "title": "Hľadajte na webe s ochranou súkromia",
    "subtitle": "Open-source vyhľadávač podporujúci 24 jazykov EÚ",
    "cta": "Vyskúšať Lookuply"
  },
  ...
}

# 3. Add language to switcher in language.js
const languages = {
  ...,
  'sk': 'Slovenčina'
};

# 4. Test translation
```

---

## Performance

### Lighthouse Scores

- **Performance**: 100/100
- **Accessibility**: 100/100
- **Best Practices**: 100/100
- **SEO**: 100/100

### Optimizations

- Minified CSS/JS
- WebP images with fallbacks
- Preload critical resources
- Async JavaScript loading
- Service Worker (optional PWA)

---

## Deployment

### Cloudflare Pages

```bash
# Automatic deployment from GitHub
# Push to main branch → auto-deploy
```

### Nginx

```nginx
server {
    listen 80;
    server_name lookuply.info www.lookuply.info;

    root /var/www/lookuply.info;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    # SSL configuration handled by Certbot
}
```

### GitHub Pages

```bash
# Enable GitHub Pages in repository settings
# Select source: main branch / (root)
# Custom domain: lookuply.info
```

---

## Contributing

We welcome contributions to improve the landing page!

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

### What to Contribute

- Design improvements
- New translations
- Performance optimizations
- Accessibility enhancements
- Bug fixes

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

---

## Related Projects

- [lookuply/crawler](https://github.com/lookuply/crawler) - Web crawler (GPL-3.0)
- [lookuply/indexer](https://github.com/lookuply/indexer) - Content indexing (GPL-3.0)
- [lookuply/search-api](https://github.com/lookuply/search-api) - Search API (GPL-3.0)
- [lookuply/frontend](https://github.com/lookuply/frontend) - Search interface (GPL-3.0)
- [lookuply/infrastructure](https://github.com/lookuply/infrastructure) - Infrastructure (GPL-3.0)
- [lookuply/docs](https://github.com/lookuply/docs) - Documentation (GPL-3.0)

---

## Links

- **Website**: [lookuply.info](https://lookuply.info)
- **Search**: [search.lookuply.info](https://search.lookuply.info)
- **API**: [api.lookuply.info](https://api.lookuply.info)
- **Documentation**: [docs.lookuply.info](https://docs.lookuply.info)
- **Status**: [status.lookuply.info](https://status.lookuply.info)
- **GitHub**: [@lookuply](https://github.com/lookuply)

---

**Simple. Fast. Private. Open Source.**
