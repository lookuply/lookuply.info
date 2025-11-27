# Deployment Standards

## ⚠️ Important Rule

**ALWAYS deploy via GitHub Actions. NEVER deploy manually via SSH/SCP.**

## Why?

1. **Consistency** - Every deployment follows the same process
2. **Audit Trail** - All deployments tracked in GitHub Actions history
3. **Rollback** - Easy to revert to previous commit if needed
4. **Automation** - No manual steps, no human errors
5. **Testing** - CI/CD ensures code is tested before deployment

## Deployment Process

1. Make changes locally in your development environment
2. Test changes locally (if possible)
3. Commit changes with descriptive message
4. Push to `main` branch
5. GitHub Actions automatically deploys to production server

```bash
# Example workflow
git add .
git commit -m "Description of changes"
git push origin main

# GitHub Actions takes care of the rest!
```

## How It Works

The `.github/workflows/deploy.yml` file defines our deployment:

1. **Trigger**: Runs on every push to `main` branch (or manual trigger)
2. **Copy**: Uses `appleboy/scp-action` to copy files to `/tmp/lookuply-landing/`
3. **Deploy**: Uses `appleboy/ssh-action` to move files to `/var/www/html/`
4. **Permissions**: Sets proper ownership (`www-data:www-data`) and permissions (`644`)

## Currently Deployed Files

- `index.html` - Main landing page
- `logo.svg` - Logo image
- `favicon.svg` - Favicon
- `og-image.svg` - Open Graph social media image
- `translations.json` - i18n translations (24 EU languages)
- `app.js` - JavaScript for language switching
- `style.css` - Styles for landing page
- `robots.txt` - SEO crawler instructions
- `sitemap.xml` - SEO sitemap with hreflang

## Manual Deployment (Emergency Only)

In case of emergency (GitHub Actions down, urgent fix needed):

```bash
# 1. Copy files to server
scp file.ext lookuply@46.224.73.134:/tmp/

# 2. SSH into server and deploy
ssh lookuply@46.224.73.134
sudo cp /tmp/file.ext /var/www/html/
sudo chown www-data:www-data /var/www/html/file.ext
sudo chmod 644 /var/www/html/file.ext
```

**But remember**: This should be VERY rare. Always prefer GitHub Actions!

## Checking Deployment Status

- GitHub Actions: https://github.com/lookuply/lookuply.info/actions
- Live site: https://lookuply.info
- Check logs: `ssh lookuply@46.224.73.134 "sudo tail -f /var/log/nginx/access.log"`

## Rollback Process

If something goes wrong:

```bash
# 1. Revert the commit locally
git revert HEAD

# 2. Push to trigger automatic rollback deployment
git push origin main
```

Or use GitHub UI to revert the commit and GitHub Actions will deploy the previous version.

## Server Configuration Changes

For Nginx configuration changes (like security headers):

```bash
# 1. SSH into server
ssh lookuply@46.224.73.134

# 2. Edit config
sudo nano /etc/nginx/sites-available/default

# 3. Test configuration
sudo nginx -t

# 4. Reload if test passes
sudo systemctl reload nginx

# 5. Document changes in SECURITY_HEADERS.md or related docs
```

**Note**: Nginx config is NOT deployed via GitHub Actions (it's server infrastructure).

## Adding New Files to Deployment

To add new files to the deployment:

1. Update `.github/workflows/deploy.yml`:
   - Add file to `source:` in `appleboy/scp-action`
   - Add `sudo cp` command in `appleboy/ssh-action`
   - Add file to `sudo chown` and `sudo chmod` commands

2. Commit and push the workflow change
3. Next deployment will include the new file

## Best Practices

✅ **DO**:
- Test locally before pushing
- Write descriptive commit messages
- Check GitHub Actions for deployment success
- Verify changes on live site after deployment

❌ **DON'T**:
- Deploy manually via SSH/SCP
- Edit files directly on the server
- Skip testing before pushing to main
- Push untested code to production

## Monitoring

After deployment, check:
- Site loads: https://lookuply.info
- No console errors (F12 in browser)
- Language switcher works
- Security headers present: `curl -I https://lookuply.info`
- Security score: https://securityheaders.com/?q=https://lookuply.info
