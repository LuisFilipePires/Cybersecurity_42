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
