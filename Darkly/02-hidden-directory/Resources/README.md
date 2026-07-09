# 02 - Hidden directories

## robots.txt

`robots.txt` is a public file used by website administrators to tell search engines (Google, Bing, etc.) which pages or directories should not be indexed.

I used

$ curl [http://10.18.200.104/robots.txt](http://10.18.200.104/robots.txt) User-agent: \* Disallow: /whatever Disallow: /.hidden


typing  [http://10.18.200.104/.hidden](http://10.18.200.104/.hidden) I found a  directory and the tree contains many README files. Recursively downloading and searching those text files reveals the flag.



