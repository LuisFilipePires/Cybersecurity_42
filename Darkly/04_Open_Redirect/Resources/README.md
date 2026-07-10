# Open Redirect

## Description

An Open Redirect vulnerability occurs when a web application allows the user to control the destination of a redirect without properly validating the target URL.

This can be abused to redirect users from a trusted domain to a malicious website.

## Discovery

The vulnerability was identified by inspecting the HTML source code using browser developer tools.

A redirect parameter was found in the social media links. The destination URL could be modified by changing the redirect parameter.

Example:

Before:

https://target.com/redirect?url=https://facebook.com

After modification:

https://target.com/redirect?url=https://malicious-site.com

The application accepted the modified destination without validation.

## Exploitation

By modifying the redirect destination, the application redirected to an unintended location and revealed the flag.

Flag:

b9e775a0291fed784a2d9680fcfad7edd6b8cdf87648da647aaf4bba288bcab3

## Impact

An attacker could abuse this vulnerability to:

- Redirect users to phishing pages.
- Make malicious links appear to come from a trusted domain.
- Abuse the reputation of the legitimate website.

---

## Mitigation

- Do not allow users to control redirect destinations directly.
- Use an allowlist of approved URLs.
- Validate and sanitize all redirect parameters server-side.
- Prefer internal identifiers instead of accepting arbitrary URLs.

Example:

Instead of:

redirect.php?url=https://facebook.com

Use:

redirect.php?site=facebook

```
php
Here the facebook.com becomes a key

$sites = [
    "facebook" => "https://facebook.com",
    "twitter" => "https://twitter.com",
    "instagram" => "https://instagram.com"
];

if (isset($sites[$_GET['site']])) {
    header("Location: " . $sites[$_GET['site']]);
} else {
    die("Invalid redirect");
}
```

Then validate on the server:

facebook -> https://facebook.com
twitter  -> https://twitter.com

Only approved destinations should be allowed.

## References

OWASP Top 10 - Unvalidated Redirects and Forwards
