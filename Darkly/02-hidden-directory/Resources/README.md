# 02 - Hidden directories

## robots.txt

`robots.txt` is a public file used by website administrators to tell search engines (Google, Bing, etc.) which pages or directories should not be indexed.

I used 

$ curl http://10.18.200.104/robots.txt
User-agent: *
Disallow: /whatever
Disallow: /.hidden

At http://10.18.200.104/whatever, downloads a file to download  with : root 437394baff5aa33daa618be47b75cb49, its a 32 hexadecimal number probably a MD5


at 

