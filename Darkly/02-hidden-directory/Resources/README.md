# 02 - Hidden directories

## robots.txt

`robots.txt` is a public file used by website administrators to tell search engines (Google, Bing, etc.) which pages or directories should not be indexed.

I used

$ curl [http://10.18.200.104/robots.txt](http://10.18.200.104/robots.txt) User-agent: \* Disallow: /whatever Disallow: /.hidden


typing  [http://10.18.200.104/.hidden](http://10.18.200.104/.hidden) I found a  directory and the tree contains many README files. Recursively downloading and searching those text files reveals the flag.


## 1- reconnaissance 
	find < IP >/.hidden | head
	or tree < IP >/.hidden | head -50
	
Are there many directories? are there a patern?
- How many ?
	find 10.12.200.238/.hidden -type f | wc -l                        

```$ 36558```

- How many extensions?
 find .hidden -type f | sed 's/.*\.//' | sort | uniq -c

```$ 18279 html```

## 2- README

All subdirectories have a README file

so lets grep "flag"
	
grep -R "flag" < IP >.hidden, or grep -Ri "password" /.hidden, or "key", "congrat", "secret"
	
	$ grep -R "flag" 10.12.200.238/.hidden
	
10.12.200.238/.hidden/whtccjokayshttvxycsvykxcfm/igeemtxnvexvxezqwntmzjltkt/lmpanswobhwcozdqixbowvbrhw/README:Hey, here is your flag : ```***d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466***```


-if doesnt work let see all the comments in readme files 

find < IP >/.hidden readme then

then

find < IP >/.hidden -name README -exec cat {} \;

or save in a file -> find < IP >.hidden -name README -exec cat {} \; > readmes.txt

search for something different 

or - grep -i flag readmes.txt

---

## Mitigation: 

Do not rely on robots.txt to hide sensitive directories. Remove sensitive files from the web root and configure proper server-side access controls to restrict unauthorized access. Ensure private resources require authentication and authorization.

