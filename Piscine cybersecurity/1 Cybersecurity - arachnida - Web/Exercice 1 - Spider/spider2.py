from pathlib import Path # Path is used to handle file paths and directories
from colorama import init
import sys # sys module is used to access command-line arguments
from title import print_title, print_spider, print_close
import requests # requests module is used to make HTTP requests


#recursivly downloads images from a given url.

from utils2 import parse_terminal
from utils2 import crawl

ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

url, depth, path  = parse_terminal(sys.argv)

visited = set()   # create an empty set
count_depth = 0
#response = requests.get(url)
init()
print_title()

crawl(visited, url, depth, path, count_depth)

print_close()
sys.exit(1)




