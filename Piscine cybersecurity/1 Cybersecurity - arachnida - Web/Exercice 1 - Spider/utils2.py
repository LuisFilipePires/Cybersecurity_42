#utils2.py

from pathlib import Path # Path is used to handle file paths and directories
import requests # requests module is used to make HTTP requests

from bs4 import BeautifulSoup # BeautifulSoup is used to parse HTML content

from urllib.parse import urljoin # urljoin is used to construct absolute URLs from relative ones
from pathlib import Path # Path is used to handle file paths and directories
import requests # requests module is used to make HTTP requests
import sys

ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


def parse_terminal(argv):

    recursive = False
    depth = 5
   # path = "./data"
    path = Path("./data")
    path.mkdir(parents=True, exist_ok=True)
    url = None
    valid_flags = {"-r", "-l", "-p"}
    i = 1

    try:
        if (len(argv) <= 1 or len(argv) > 7):
            raise ValueError("\nBAD ENTRY: optional: -r (recursive) -l (+ number of deph) -p (+ path directory)\nMandatory:\t link(http://exemple.com)")
            return
        while i < len(argv):
            arg = argv[i]
            if arg.startswith("-") and arg not in valid_flags:
                raise ValueError(f"Invalid flag: {arg}")
            elif arg == "-r":
                recursive = True
            elif not arg.startswith("-"): #URL its the one starts without -
                if url is None:
                    url = arg
                else:
                    raise ValueError("Multiple URLs not allowed")
            elif arg == "-l":
                if i < len(argv) - 1 and argv[i + 1].isdigit():
                    i += 1
                    depth = int(argv[i])
                else:
                    raise ValueError("-l must be followed by a positive integer")
            elif arg == "-p":
                if i < len(argv) - 1 and argv[i + 1].strip() != "":
                    i += 1
                    path = Path(argv[i])
                else:
                    raise ValueError("-p error: missing path")
            i += 1
        if url is None:
            raise ValueError("Missing URL")
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL format")
        if not recursive:
            print("\nCaution: recursive is off\n-l flag is only valid with -r")
            depth = 0 
        return (url, depth, path)
    except Exception as e:
        print (f"Please enter URL (http://, https://) optional ( -r (recursive), -l + Number (deph), -p + path (path directory)\n{e}")
        return


def download_images(url, soup, path):
    headers = {"User-Agent": "Mozilla/5.0"}

    for img in soup.find_all("img"):
        # pega src, data-src ou srcset
        src = img.get("src") or img.get("data-src") or img.get("srcset")
        if not src or src.strip() == "" or src.startswith("data:"):
            continue

        # se src for srcset, pega só o primeiro link
        if "," in src:
            src = src.split(",")[0].split()[0]

        img_url = urljoin(url, src)

        try:
            response = requests.get(img_url, headers=headers, timeout=5)
            # verifica status
            if response.status_code != 200:
                continue
            # verifica se é imagem
            if "image" not in response.headers.get("Content-Type", ""):
                continue
            # extrai nome do ficheiro
            name = img_url.split("/")[-1].split("?")[0]
            if not name:
                continue
            # filtra por extensões permitidas
            if not name.lower().endswith(ALLOWED_EXT):
                continue
            filename = path / name
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")

def crawl(visited, url, depth, path, count_depth):
    try:
        print(f"Depth: {count_depth} | URL: {url}\n")
        if url in visited:
            print ("alredy visited")
            return
        #only to debugging
        if count_depth > depth:
            print (f"below depth: {count_depth}")
            return
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Spider42/1.0"
            }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"Spider: Link ok:")
        except Exception as e:
            print(f"\nSpider: error URL: {e}")
            return

        visited.add(url)
        #try ?
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            print(f"Skipping {url}: non-HTML content ({content_type})")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")
        download_images(url, soup, path)

        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                next_url = urljoin(url, href)
                if next_url.startswith(("http://", "https://")):
                    crawl(visited, next_url, depth, path, count_depth + 1)
        
    except Exception as e:
            print(f"Error in Crawl: {e}")
    
