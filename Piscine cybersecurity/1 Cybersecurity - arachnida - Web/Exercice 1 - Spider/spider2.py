from pathlib import Path # Path is used to handle file paths and directories
from colorama import init
import sys # sys module is used to access command-line arguments
from title import print_title, print_spider, print_close
import requests # requests module is used to make HTTP requests


#recursivly downloads images from a given url.

from utils2 import parse_terminal

ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

url, recursive, depth, path  = parse_terminal(sys.argv)

visited = set()   # create an empty set
#response = requests.get(url)

def crawl(url, depth):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Spider42/1.0"
        }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"Spider: Link ok:")
        
    except Exception as e:
        print(f"\nSpider: error URL: {e}")
        if depth  == 0:
            print_close()
            sys.exit(1)
    

