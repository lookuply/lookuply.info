# Lookuply Landing Page

Official landing page for [lookuply.info](https://lookuply.info) - Privacy-first search engine supporting 24 EU languages.

🌐 **Live:** https://lookuply.info

---

## 🚀 Quick Start

This is a simple, single-file HTML landing page with embedded CSS. Changes pushed to `main` branch are automatically deployed via GitHub Actions.

### Features

- **Single File**: Everything in `index.html`
- **No Dependencies**: Pure HTML/CSS
- **Responsive Design**: Works on all devices
- **Auto-Deploy**: GitHub Actions CI/CD
- **Fast**: Served via Nginx + Cloudflare CDN
- **Secure**: HTTPS with Let's Encrypt

---

## 📁 Project Structure

```
lookuply.info/
├── index.html                 # Landing page (all-in-one)
├── .github/
│   └── workflows/
│       └── deploy.yml         # CI/CD workflow
└── README.md                  # This file
```

Simple and clean - just one HTML file with embedded CSS.

---

## 💻 Local Development

### Clone & Edit

```bash
git clone git@github.com:lookuply/lookuply.info.git
cd lookuply.info

# Edit the landing page
nano index.html

# Test locally - just open in browser
open index.html
```

### Deploy Changes

```bash
git add index.html
git commit -m "Update: description of changes"
git push origin main

# GitHub Actions will automatically deploy!
# Check: https://github.com/lookuply/lookuply.info/actions
```

Changes go live at https://lookuply.info within ~1 minute.

---

## 🎨 Current Content

### Landing Page Features

- ✅ **Privacy First** - No tracking, no data collection, no user profiling
- ✅ **24 EU Languages** - Supporting all official European Union languages
- ✅ **Open Source** - Transparent, auditable code (GPL-3.0 licensed)

### Links

- GitHub: https://github.com/lookuply
- Documentation: https://github.com/lookuply/docs
- Contact: hello@lookuply.info

### Design

- **Theme**: Purple gradient (`#667eea` to `#764ba2`)
- **Typography**: System fonts (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto)
- **Responsive**: Mobile-first design with media queries

---

## 🚀 Deployment

### CI/CD Pipeline

GitHub Actions automatically deploys on every push to `main` branch.

**Workflow:** `.github/workflows/deploy.yml`

```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    steps:
      - name: Copy file via SCP
        uses: appleboy/scp-action@v0.1.7

      - name: Deploy file
        uses: appleboy/ssh-action@v1.0.3
        # Copies to /var/www/html/index.html
```

**Deployment Flow:**
```
Push to main → GitHub Actions → SCP to server → Deploy to Nginx
```

### Infrastructure

- **Server**: Hetzner CPX41 (46.224.73.134)
- **Web Server**: Nginx
- **SSL**: Let's Encrypt (auto-renewal enabled, expires 2026-02-24)
- **CDN**: Cloudflare (proxy enabled)
- **DNS**: Cloudflare nameservers

### Authentication

- **SSH Key**: RSA 4096-bit deployment key
- **Stored**: GitHub Secrets → `SSH_PRIVATE_KEY`
- **Server**: `/home/lookuply/.ssh/authorized_keys`

---

## 📝 Status

✅ Landing page live
✅ CI/CD pipeline working
✅ SSL certificate active
✅ Cloudflare CDN enabled

**Current:** Week 4 complete (Infrastructure + Landing Page)
**Next:** Week 5 - Branding & Translations

---

## 🔗 Links

- **Live Site**: https://lookuply.info
- **GitHub Org**: https://github.com/lookuply
- **Documentation**: https://github.com/lookuply/docs
- **Contact**: hello@lookuply.info

---

## 📄 License

GPL-3.0 License - Open source, privacy-first search engine.

---

## 🏗️ Related Repositories

- [lookuply/crawler](https://github.com/lookuply/crawler) - Web crawler
- [lookuply/search-engine](https://github.com/lookuply/search-engine) - Search engine core
- [lookuply/api](https://github.com/lookuply/api) - API service
- [lookuply/frontend](https://github.com/lookuply/frontend) - Search interface
- [lookuply/infrastructure](https://github.com/lookuply/infrastructure) - Infrastructure as code
- [lookuply/docs](https://github.com/lookuply/docs) - Documentation

---

**Lookuply** - Privacy-first search • 24 EU languages • Open source • Community-driven
