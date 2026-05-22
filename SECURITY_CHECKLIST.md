  
# EntreSkill Hub - Security Checklist

## Before Production Deployment

### Django Settings
- [ ] Set DEBUG=False
- [ ] Change SECRET_KEY to random 50+ char string
- [ ] Set ALLOWED_HOSTS to your domain
- [ ] Enable SECURE_SSL_REDIRECT=True
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Set CSRF_COOKIE_SECURE=True
- [ ] Set SECURE_HSTS_SECONDS=31536000
- [ ] Set SECURE_HSTS_INCLUDE_SUBDOMAINS=True

### Database
- [ ] Use PostgreSQL, not SQLite
- [ ] Create dedicated DB user with limited privileges
- [ ] Enable PostgreSQL SSL connections
- [ ] Set strong DB password
- [ ] Enable automatic backups

### Media Files
- [ ] Validate file uploads by type and size
- [ ] Store media outside web root or behind Nginx
- [ ] Disable directory listing on media folder
- [ ] Scan uploaded files for malware

### Authentication
- [ ] Enable password validators in settings
- [ ] Set PASSWORD_HASHERS to use PBKDF2 or Argon2
- [ ] Implement rate limiting on login endpoint
- [ ] Enable 2FA for admin users

### API Keys
- [ ] Never commit.env file to git
- [ ] Rotate OpenAI, Stripe, Twilio keys before launch
- [ ] Store secrets in environment variables or vault

### Dependencies
- [ ] Run `pip-audit` or `safety check` on requirements.txt
- [ ] Pin all versions in requirements.txt
- [ ] Update Django to latest patch version

### Nginx
- [ ] Disable server_tokens
- [ ] Set client_max_body_size to reasonable limit
- [ ] Enable SSL with strong ciphers
- [ ] Add security headers

### Celery
- [ ] Use Redis password authentication
- [ ] Restrict Redis to localhost only
- [ ] Monitor Celery task failures

### Monitoring
- [ ] Set up error logging with Sentry
- [ ] Enable Django admin email on 500 errors
- [ ] Monitor disk space for media folder
- [ ] Set uptime monitoring

### Backups
- [ ] Daily PostgreSQL backup via backup_db.bat
- [ ] Offsite backup to S3 or similar
- [ ] Test restore procedure monthly