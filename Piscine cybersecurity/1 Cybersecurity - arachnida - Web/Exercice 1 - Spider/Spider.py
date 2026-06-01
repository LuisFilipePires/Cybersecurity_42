#spider.py
'''
1. Parse command-line arguments (-r, -l N, -p PATH, URL)
2. Create folder if it doesn’t exist
3. Initialize visited set: visited = set()
4. Define crawl(url, depth) function:
   4a. Stop if depth == 0 or url in visited
   4b. Add url to visited
   4c. Download page
   4d. Extract images
       - Download each image if it matches allowed extensions
   4e. Extract links
       - For each valid link, call crawl(link, depth-1) if -r flag is set
5. Start crawl() with URL and depth
'''

from utils import parse_terminal, download_images, crawl
from title import print_title, print_spider, print_close
import sys # sys module is used to access command-line arguments
import requests # requests module is used to make HTTP requests
#from title import title
from colorama import init
#from bs4 import BeautifulSoup # BeautifulSoup is used to parse HTML content
#from urllib.parse import urljoin # urljoin is used to construct absolute URLs from relative ones
from pathlib import Path # Path is used to handle file paths and directories

#if len(sys)
try:
    url, recursive, depth, path  = parse_terminal(sys.argv)
except Exception as e:
    print_spider()
    print(f"\nError parsing arguments: {e}")
    print("Usage: ./Spider 'URL' -r -l N -p PATH\n\n")
    print_close()
    sys.exit(1)

try:
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"Response objects: {response}")
except requests.exceptions.RequestException as e:
    print(f"Spider error: {e}")
    print(f"\nBye Bye Spider man\n")
    raise ValueError("URL error: ")

'''
try:
    download1(url)
except Exception as e:
    print(f"\nMain: Request Error: {e}")
    sys.exit(1)
'''

init()
print_title()


path = Path(path)
path.mkdir(parents=True, exist_ok=True)
print (f"Images will be saved in: {path}")
'''
From a page:

Extract all <img src="...">
Filter by extension (.jpg, .png, etc.)
Fix URLs (relative → absolute)
'''
#main code for recursion


visited = set()   # create an empty set

#if url in visited:
#    return
#visited.add(url)

try:
    crawl(visited, url, depth, recursive, path)
except KeyboardInterrupt:
    print("\nSaindo do programa de forma limpa.")
    print_close()
    sys.exit(0)


print (f"\n\nVisited {len(visited)} page(s)----------")
print("All visited sites")
for url in visited:
    print(url)


