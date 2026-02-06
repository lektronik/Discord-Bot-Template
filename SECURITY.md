# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **Do NOT** open a public issue
2. Email the maintainer directly or use GitHub's private vulnerability reporting
3. Include details about the vulnerability and steps to reproduce

### What to expect:
- Response within 48 hours
- Status update within 7 days
- Credit in security advisory (if desired)

## Security Best Practices

When using this template:

### Environment Variables
- **Never** commit `.env` files with real tokens
- Use `.env.example` as a template only
- Store secrets in Railway/hosting environment variables

### Bot Token Security
- Regenerate your token if exposed
- Use minimal required permissions
- Enable 2FA on your Discord account

### Database
- SQLite database contains user data
- Add to `.gitignore` (already configured)
- Backup regularly in production

## Dependencies

Keep dependencies updated:
```bash
pip install --upgrade -r requirements.txt
```

## Disclosure Policy

We follow responsible disclosure. Fixes will be released before public disclosure.
