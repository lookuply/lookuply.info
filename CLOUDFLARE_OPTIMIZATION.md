# Cloudflare Optimization for Lighthouse

## Issue: Email Obfuscation Script Blocking LCP

Cloudflare's Email Address Obfuscation feature injects `email-decode.min.js` which:
- Adds 461 ms to critical path latency
- Blocks LCP (Largest Contentful Paint)
- Not needed for simple `mailto:` links

## Solution: Disable Email Obfuscation

### Steps:

1. **Log in to Cloudflare Dashboard**
   - Go to https://dash.cloudflare.com
   - Select domain: `lookuply.info`

2. **Navigate to Scrape Shield**
   - In the left sidebar, click on **"Scrape Shield"**
   - Or go directly to: Security → Scrape Shield

3. **Disable Email Address Obfuscation**
   - Find **"Email Address Obfuscation"** toggle
   - Turn it **OFF** (grey)

4. **Verify Changes**
   - Wait 1-2 minutes for CDN cache to clear
   - Test page: https://lookuply.info
   - Check network tab - `email-decode.min.js` should be gone

## Expected Performance Improvement

### Before:
```
Maximum critical path latency: 461 ms
├── Initial Navigation (326 ms)
├── email-decode.min.js (461 ms) ← BLOCKING
└── style.css (460 ms) ← BLOCKING
```

### After:
```
Maximum critical path latency: ~326 ms
└── Initial Navigation (326 ms)
```

**Expected improvement:** ~135 ms faster LCP (~29% reduction)

## Alternative: Keep Email Protection

If you want to keep email protection but avoid the script:

1. **Use email image** instead of `mailto:` link
2. **Use contact form** instead of direct email
3. **Manually obfuscate** email in HTML (e.g., `hello [at] lookuply [dot] info`)

## Other Cloudflare Optimizations

While you're in Cloudflare dashboard, consider:

### Speed → Optimization
- ✅ **Auto Minify:** Enable HTML, CSS, JS
- ✅ **Brotli:** Enable (better compression than gzip)
- ✅ **Rocket Loader:** OFF (can break dynamic JS)
- ✅ **Mirage:** Enable (lazy load images)

### Caching → Configuration
- **Browser Cache TTL:** 4 hours (for landing page)
- **Always Online:** Enable

### Security → Settings
- ✅ **Always Use HTTPS:** Enable
- ✅ **Automatic HTTPS Rewrites:** Enable
- ✅ **Opportunistic Encryption:** Enable

## Testing

After making changes:

```bash
# Check if email-decode.min.js is gone
curl -s https://lookuply.info | grep "email-decode"
# Should return nothing

# Run Lighthouse
lighthouse https://lookuply.info --view
```

## Notes

- Changes propagate through CDN in 1-2 minutes
- May need to clear browser cache to see changes
- Cloudflare cache can be purged manually: Caching → Purge Everything
