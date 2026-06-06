#spyder.py

from pathlib import Path # Path is used to handle file paths and directories
from colorama import init
import sys # sys module is used to access command-line arguments
from title import print_title, print_spider, print_close
import requests # requests module is used to make HTTP requests
#recursivly downloads images from a given url.
from utils import parse_terminal
from utils import crawl

try:
    args = parse_terminal(sys.argv)
    if args is None:
        print("main EXIT 1")
        sys.exit(1)
    url, depth, path, rec = args
    visited = set() 
    #response = requests.get(url)
    init()
    print_title()

    crawl(visited, url, depth, path, 0)

    print_close()
    sys.exit(1)
except KeyboardInterrupt:
    print("\nClosing crawler… Ctrl+C detected")
    sys.exit(0)

