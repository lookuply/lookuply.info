# Security Headers Configuration

Recommended security headers for Lookuply landing page.

## Nginx Configuration

Add these headers to your Nginx configuration file:

```nginx
# /etc/nginx/sites-available/lookuply.info

server {
    server_name lookuply.info www.lookuply.info;

    # ... existing configuration ...

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; frame-ancestors 'self';" always;

    # Permissions Policy (formerly Feature-Policy)
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()" always;

    # HSTS (HTTP Strict Transport Security)
    # Only add this after confirming HTTPS works perfectly
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # ... rest of configuration ...
}
```

## Apply Changes

```bash
# Test Nginx configuration
sudo nginx -t

# Reload Nginx if test passes
sudo systemctl reload nginx
```

## Verify Headers

Test the headers are applied:

```bash
curl -I https://lookuply.info
```

Or use online tools:
- https://securityheaders.com
- https://observatory.mozilla.org

## Privacy Headers

Since Lookuply is privacy-focused, we don't use:
- ❌ Google Analytics
- ❌ Facebook Pixel
- ❌ Third-party tracking
- ❌ Cookies (except localStorage for language preference)

## Expected Security Score

With these headers, you should achieve:
- **SecurityHeaders.com:** A+ rating
- **Mozilla Observatory:** A+ rating
- **SSL Labs:** A+ rating (already achieved with Let's Encrypt)

## Notes

- All headers are set with `always` flag to ensure they're sent even on error pages
- CSP allows `unsafe-inline` for styles/scripts since we use inline CSS and JS
- HSTS preload is enabled for maximum security
- No tracking or analytics = maximum privacy
