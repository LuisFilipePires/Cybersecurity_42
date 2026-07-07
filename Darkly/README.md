# DARKLY

This project is organized into folders numbered from 1 to 14.

Each folder contains a directory called `Resources`, which includes:
- a `README.md` file explaining the vulnerability found, where it was located, and how it was exploited;
- a `flag` file containing the flag obtained after successfully completing the challenge.

The vulnerabilities covered in this project are based on common web security issues, especially those listed in the **OWASP Top 10**.

The OWASP Top 10 is a list of the ten most critical security risks affecting web applications.

### Common examples include:
- SQL Injection
- Broken Authentication
- Cross-Site Scripting (XSS)
- Broken Access Control
- Security Misconfiguration

### Project Overview

In this exercise, I identified 14 vulnerabilities, documented their locations, explained how they could be exploited, and described possible mitigation techniques.

## Challenges

### 1 - HTTP Headers

**Vulnerability:** HTTP Header Manipulation

**Description:**  
The application relies on HTTP headers such as `User-Agent` and `Referer` to validate requests. By modifying these headers, it is possible to bypass certain restrictions and access hidden information.

**Mitigation:**  
Do not rely on client-controlled headers for authentication or authorization decisions. Always validate permissions on the server side.

---

# 02 - Hidden directories

## robots.txt

`robots.txt` is a public file used by website administrators to tell search engines (Google, Bing, etc.) which pages or directories should not be indexed.

Example:
User-agent: *
Disallow: /admin/
Disallow: /backup/
Disallow: /.hidden/


Although it is not designed for security, administrators sometimes accidentally reveal interesting paths by putting them in `robots.txt`.

A common mistake is thinking that:

"Disallow" = "hidden"

This is false. It only tells search engine crawlers not to index those paths. Anyone can still access them if they know the URL.

---

## Checking robots.txt

Try:
http://site.com/robots.txt
or
curl http://site.com/robots.txt
or
wget -qO- http://site.com/robots.txt

Example:
curl http://10.18.200.104/robots.txt

User-agent: *
Disallow: /whatever
Disallow: /.hidden

The file reveals the directory:

http://10.18.200.104/.hidden/

Download recursively

If directory listing is enabled, we can download the entire directory tree.

Using:

wget -r http://site.com/.hidden/

-r means recursive download.

A cleaner method:

wget -r -np -nH http://site.com/.hidden/

Options:

-r → recursive download (go through subdirectories)
-np → no parent (do not move to directories above the target)
-nH → no host directory (do not create a folder named after the website)

---

## Search for the flag

After downloading:

grep -R "flag" .hidden/

or search all README files:

find . -name README -exec grep -H "flag" {} \;

The flag can be hidden inside one of the many text files.1
