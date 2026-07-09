# 03 - Hidden Directories / Password Hash

## Discovering hidden directories

From the previous flag, I checked the website's `robots.txt` file.

`robots.txt` is a public file used by website administrators to tell search engines (Google, Bing, etc.) which pages or directories should **not** be indexed. It does **not** prevent users from accessing those locations directly.

> **Note:** IP addresses shown in this write-up are fictitious.

```
`curl http://10.18.200.104/robots.txt`
```

Output:

```
`User-agent: \*`

`Disallow: /whatever`

`Disallow: /.hidden`
```

Browsing to `/whatever` downloaded a file containing:

```
`root:437394baff5aa33daa618be47b75cb49`
```

This appears to be a username (`root`) followed by a password hash.


## Identifying the hash

Since a 32-character hexadecimal hash can represent several algorithms (MD5, NTLM, MD4, etc.), I used a few hash identification tools.

### `hashid`

Save the hash into a file:

```
`437394baff5aa33daa618be47b75cb49`
```

Run:

```
`hashid hash.txt`
```

Possible results:

- MD5

- MD4

- NTLM

- LM

- RIPEMD-128

- Domain Cached Credentials

- ...


### `hash-identifier`

```
`hash-identifier 437394baff5aa33daa618be47b75cb49`
```

Most likely result:

- MD5

Other possible matches include NTLM and MD4.


### `name-that-hash`

```
`nth -f hash.txt`
```

Top results:

1. MD5

2. MD4

3. NTLM

4. Domain Cached Credentials

Since this is a web challenge, **MD5** was the most likely candidate.


## Common hash lengths

| Length | **Common hash types** |
| -: | :-: |
| 32 | MD5, MD4, NTLM, LM |
| 40 | SHA-1 |
| 56 | SHA-224 |
| 64 | SHA-256 |
| 96 | SHA-384 |
| 128 | SHA-512 |

> **Note:** Hash length alone is not enough to identify the algorithm, but it helps narrow down the possibilities.


## Cracking the hash with John the Ripper

John the Ripper stores previously cracked hashes in `~/.john/john.pot`. To ignore cached results:

```
`john --pot=NONE --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt`
```

Or remove the pot file:

```
`rm ~/.john/john.pot`
```

Run John:

```
`john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt`
```

Recovered password:

```
`qwerty123@`
```

> **Note:** Password hashes are **cracked**, not **decrypted**. John compares the hash against candidate passwords from the wordlist until it finds a match.


## Finding the login page

The downloaded file contained:

```
`root:437394baff5aa33daa618be47b75cb49`
```

I assumed `root` was the username.

I first tried:

```
`http://\<IP\>/root`
```

but that page did not exist.

Next, I tried:

```
`http://\<IP\>/admin`
```

which presented a login page.

Using:

- **Username:** `root`

- **Password:** `qwerty123@`

I successfully authenticated and obtained the next flag.

## Flag found ✅

The recovered credentials allowed access to the administrator login page, revealing the next challenge flag.


---


## \*\*\* Mitigation \*\*\*

To reduce the risk of this type of attack:

- **Do not use `robots.txt` to hide sensitive content.** The file is publicly accessible and only tells search engines what not to index. Sensitive directories should be protected with proper authentication or removed from public access.

- **Never expose password hashes publicly.** Configuration files, backups, and database exports should not be accessible from the web server.

- **Use strong password hashing algorithms.** Store passwords using algorithms such as **Argon2**, **bcrypt**, or **scrypt** instead of fast hashes like MD5 or SHA-1.

- **Enforce strong passwords.** Weak passwords (e.g., `qwerty123@`) are easily cracked using common wordlists such as `rockyou.txt`.

- **Restrict access to administrative interfaces.** Protect admin pages with strong authentication, multi-factor authentication (MFA), IP restrictions when appropriate, and rate limiting to reduce brute-force attacks.

- **Perform regular security audits.** Periodically check for exposed files, sensitive directories, and weak credentials.

