# PlatformV2-Dev Migration Complete

**Created:** 2026-02-10
**Source:** platformv2-dev.webstagingserver.co.uk (Nimbus Hosting)
**Destination:** Digital Ocean Droplet (134.209.186.176)
**Status:** ✅ Fully Operational

---

## 🎉 Migration Summary

Successfully cloned the WordPress "Hive" platform from Nimbus hosting to your Digital Ocean droplet with full version control via GitHub.

### What Was Accomplished

1. ✅ **Exported database** from Nimbus (79 tables)
2. ✅ **Transferred 14,188 files** (625MB) via rsync
3. ✅ **Set up LEMP stack** (Linux, Nginx, MySQL 8.0, PHP 8.3)
4. ✅ **Configured database** with proper authentication
5. ✅ **Updated WordPress URLs** to droplet IP
6. ✅ **Initialized Git repository** with version history
7. ✅ **Pushed to GitHub** for rollback capability

---

## 🌐 Access Information

### Website Front-End
- **URL:** http://134.209.186.176/
- **Application:** Hive (WordPress-based learning platform)
- **Status:** Fully functional with database connectivity

### Droplet Access
- **IP:** 134.209.186.176
- **Username:** root
- **Password:** Digitalocan 2025Rootpassword75X
- **SSH Command:** `ssh root@134.209.186.176`

### GitHub Repository
- **URL:** https://github.com/mda756/platformv2-dev
- **Visibility:** Private
- **Branches:** master (main branch)
- **Commits:** 2 (initial clone + configuration)

---

## 📁 File Locations

### Website Files
```
/var/www/platformv2-dev/
├── public/                    # WordPress root (document root for Nginx)
│   ├── wp-admin/
│   ├── wp-content/
│   ├── wp-includes/
│   ├── wp-config.php         # Database configuration
│   └── index.php
├── .git/                      # Git repository
└── .gitignore
```

### Nginx Configuration
- **Config file:** `/etc/nginx/sites-available/platformv2-dev`
- **Enabled:** `/etc/nginx/sites-enabled/platformv2-dev`
- **Document root:** `/var/www/platformv2-dev/public`

---

## 🗄️ Database Information

### Connection Details
- **Database name:** platformv2_dev
- **Username:** wp_platformv2
- **Password:** Yoke2026Platform!
- **Host:** localhost
- **Tables:** 79 (all successfully imported)

### Access via Claude Code
```bash
# SSH to droplet
ssh root@134.209.186.176

# Access database as root (recommended for Claude Code)
mysql -u root platformv2_dev

# Example queries
mysql -u root platformv2_dev -e "SHOW TABLES;"
mysql -u root platformv2_dev -e "SELECT * FROM wp_hbgcjihu_options WHERE option_name = 'home';"
```

### Database Tables Overview
- **WordPress core:** wp_hbgcjihu_* (standard WordPress tables)
- **Hive custom:** hive_* (chat sessions, user searches, trusted sources, etc.)
- **Ninja Forms:** ng_* (user info, progress tracking, feedback)

---

## 🔄 Git Version Control & Rollback

### Current Repository Status
```bash
# View commit history
ssh root@134.209.186.176 'cd /var/www/platformv2-dev && git log --oneline'

# Output:
# 17bb38b Configure database user and update WordPress URLs for droplet
# eab7ae9 Initial commit: Cloned from Nimbus platformv2-dev
```

### Rolling Back Changes

**Rollback to initial Nimbus state:**
```bash
ssh root@134.209.186.176
cd /var/www/platformv2-dev
git reset --hard eab7ae9
# Revert wp-config.php and database URLs to Nimbus settings
```

**Rollback to previous commit:**
```bash
git log --oneline              # Find commit hash
git reset --hard <commit-hash> # Rollback to specific commit
```

**View changes between commits:**
```bash
git diff HEAD~1                # Compare with previous commit
git show 17bb38b              # View specific commit changes
```

### Making New Changes
```bash
# After making changes to files
git add -A
git commit -m "Description of changes"
git push origin master
```

---

## 🛠️ Common Operations

### Restart Services
```bash
ssh root@134.209.186.176

# Restart Nginx
systemctl restart nginx

# Restart PHP-FPM
systemctl restart php8.3-fpm

# Restart MySQL
systemctl restart mysql
```

### View Logs
```bash
# Nginx error log
tail -f /var/log/nginx/error.log

# PHP error log
tail -f /var/log/php8.3-fpm.log

# MySQL error log
tail -f /var/log/mysql/error.log
```

### Check Service Status
```bash
systemctl status nginx
systemctl status php8.3-fpm
systemctl status mysql
```

### Update WordPress URLs (if needed)
```bash
mysql -u root platformv2_dev << 'EOF'
UPDATE wp_hbgcjihu_options
SET option_value = 'http://NEW_URL_HERE'
WHERE option_name IN ('siteurl', 'home');
EOF
```

---

## 🔒 Security Notes

### Current Setup
- Website accessible via HTTP (not HTTPS)
- Using root user for SSH (full access)
- Database password stored in wp-config.php
- Private GitHub repository (only accessible to mda756 account)

### Recommended Improvements (Optional)
1. **SSL Certificate:** Install Let's Encrypt for HTTPS
2. **Firewall:** Configure UFW to restrict ports
3. **Non-root user:** Create dedicated user for SSH access
4. **Database backups:** Set up automated daily backups
5. **Monitoring:** Install monitoring for uptime tracking

---

## 📊 System Resources

### Droplet Specifications
- **Plan:** Basic - $6/month
- **CPU:** 1 vCPU
- **RAM:** 1GB
- **Storage:** 25GB SSD (currently using ~4GB)
- **Bandwidth:** 1TB transfer/month
- **Location:** London (lon1)

### Current Usage
```bash
# Check disk usage
ssh root@134.209.186.176 'df -h /var/www/platformv2-dev'

# Check memory usage
ssh root@134.209.186.176 'free -h'
```

---

## 🔄 Syncing Changes from Nimbus (Manual)

If updates are made to the original Nimbus site and you want to pull them:

### Option 1: Full Re-sync (Nuclear Option)
```bash
ssh root@134.209.186.176
cd /var/www/platformv2-dev

# Backup current state
git add -A && git commit -m "Backup before Nimbus sync"
git push origin master

# Re-sync from Nimbus
rsync -avz --delete \
  -e "ssh -i ~/.ssh/nimbus_hosting" \
  siteadmin@d6023.lon1.stableserver.net:/home/stableserver/public_html/platformv2-dev/ \
  /var/www/platformv2-dev/public/

# Commit changes
git add -A && git commit -m "Synced from Nimbus on $(date +%Y-%m-%d)"
git push origin master
```

### Option 2: Selective File Sync
```bash
# Sync only specific directories (e.g., wp-content/uploads)
rsync -avz \
  -e "ssh -i ~/.ssh/nimbus_hosting" \
  siteadmin@d6023.lon1.stableserver.net:/home/stableserver/public_html/platformv2-dev/wp-content/uploads/ \
  /var/www/platformv2-dev/public/wp-content/uploads/
```

### Option 3: Database Sync Only
```bash
# Export from Nimbus via phpMyAdmin (web interface)
# Then import to droplet
mysql -u root platformv2_dev < backup.sql

# Or direct MySQL-to-MySQL (if ports are open)
mysqldump -h d6023.lon1.stableserver.net -u deefe_dbsuperu_deefe -p deefe_dbsuperu_deefe | \
  mysql -u root platformv2_dev
```

---

## 🐛 Troubleshooting

### Website Shows 502 Bad Gateway
```bash
# Check if PHP-FPM is running
systemctl status php8.3-fpm
systemctl restart php8.3-fpm
```

### Website Shows Database Error
```bash
# Check MySQL is running
systemctl status mysql

# Verify credentials in wp-config.php
cat /var/www/platformv2-dev/public/wp-config.php | grep "DB_"

# Test database connection
mysql -u wp_platformv2 -p'Yoke2026Platform!' platformv2_dev -e "SHOW TABLES;"
```

### Changes Not Showing
```bash
# Clear Nginx cache
rm -rf /var/cache/nginx/*
systemctl restart nginx

# Clear PHP cache
systemctl restart php8.3-fpm
```

### Git Push Fails
```bash
# Verify SSH key is working
ssh -T git@github.com
# Should see: "Hi mda756! You've successfully authenticated..."

# Check remote URL
cd /var/www/platformv2-dev
git remote -v

# Force push (use carefully!)
git push -f origin master
```

---

## 📝 Next Steps & Maintenance

### Immediate (Optional)
- [ ] Set up SSL certificate with Let's Encrypt
- [ ] Configure custom domain (if desired)
- [ ] Set up automated database backups
- [ ] Install WordPress security plugins

### Regular Maintenance
- [ ] Weekly: Check disk space usage
- [ ] Monthly: Review error logs
- [ ] Monthly: Update WordPress core, plugins, themes
- [ ] Quarterly: Review and optimize database

### Development Workflow
1. Make changes to files on droplet
2. Test changes at http://134.209.186.176/
3. Commit changes: `git add -A && git commit -m "Description"`
4. Push to GitHub: `git push origin master`
5. If issues occur, rollback: `git reset --hard <previous-commit>`

---

## 📚 Useful Commands Reference

```bash
# Quick website check
curl -I http://134.209.186.176/

# Database quick check
ssh root@134.209.186.176 'mysql -u root platformv2_dev -e "SELECT COUNT(*) FROM wp_hbgcjihu_posts;"'

# File permissions fix (if needed)
ssh root@134.209.186.176 'chown -R www-data:www-data /var/www/platformv2-dev/public && chmod -R 755 /var/www/platformv2-dev/public'

# Git status check
ssh root@134.209.186.176 'cd /var/www/platformv2-dev && git status'

# View recent commits
ssh root@134.209.186.176 'cd /var/www/platformv2-dev && git log --oneline -n 5'
```

---

## ✅ Migration Verification Checklist

- [x] Website accessible at http://134.209.186.176/
- [x] WordPress loads without errors
- [x] Database connectivity working
- [x] 79 tables imported successfully
- [x] 14,188 files transferred
- [x] Git repository initialized
- [x] Code pushed to GitHub
- [x] Site URLs updated to droplet IP
- [x] Nginx serving WordPress correctly
- [x] PHP 8.3 executing properly
- [x] MySQL user created with proper permissions
- [x] SSH access working from Windows PC

---

## 🆘 Support & Documentation

### Related Documentation
- **Droplet Setup:** See `DROPLET_COMPLETE_SETUP.md` for general droplet access and usage
- **Git Sync:** See `SETUP_SUMMARY.md` for automated git sync documentation (yoke-assets repo)
- **Credentials:** See `CREDENTIALS_STORE.json` for access credentials

### Getting Help
If you encounter issues:
1. Check the troubleshooting section above
2. Review error logs on the droplet
3. Check git commit history for what changed
4. Test rollback to previous working commit

---

**Document Version:** 1.0
**Last Updated:** 2026-02-10
**Migration Completed By:** Claude Code
**Total Migration Time:** ~2 hours

**✨ Your WordPress Hive platform is now fully operational on the droplet with GitHub version control! ✨**
