#utils.py
#parse_terminal with repeted code, but its good for now

from pathlib import Path # Path is used to handle file paths and directories
import requests # requests module is used to make HTTP requests
from bs4 import BeautifulSoup # BeautifulSoup is used to parse HTML content
from urllib.parse import urljoin, urlparse, urlunparse # urljoin is used to construct absolute URLs from relative ones
from pathlib import Path # Path is used to handle file paths and directories
import requests # requests module is used to make HTTP requests
import sys

ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
DOMAIN = None

def normalize(url):
    parts = urlparse(url)
    # remove fragment e query
    clean = parts._replace(fragment='', query='')
    return urlunparse(clean).rstrip('/')

def set_domain(url):
    global DOMAIN
    DOMAIN = urlparse(url).netloc


def _parse_depth(argv, i):
    if i == len(argv) - 1:
        raise ValueError("Missing depth")
    i += 1
    if not argv[i].isdigit():
        raise ValueError("Depth must be a number")
    return int(argv[i]), i


def _parse_path (argv, i):
    if i == len(argv) - 1:
        raise ValueError("Missing path")
    i += 1
    path = Path(argv[i]).resolve()
    if path.suffix:
        raise ValueError(f"Path is a file: {path.name}")
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception:
        raise ValueError(f"Invalid Path: {path.resolve()}")
    return path, i

def parse_terminal(argv):
    
    url = None
    rec = False
    path = Path("./data")
    depth = 5
    count_url = 0
    valid_flags = {"-r", "-l", "-p", "-rl", "-rp"}
    i = 1

    try:
        while i < len(argv):
            if argv[i].startswith(("http://", "https://")):
                url = argv[i]
                if url is None:
                    raise ValueError("Missing URL")
                count_url += 1
                if count_url > 1:
                    raise ValueError("Mulplipe URL's")
            elif argv[i].startswith("-rl"):
                rec = True
                depth, i = _parse_depth(argv, i)
            elif argv[i].startswith("-rp"):
                rec = True
                path, i = _parse_path(argv, i)
            elif argv[i].startswith("-l"):
                depth, i = _parse_depth(argv, i)
            elif argv[i].startswith("-p"):
                path, i = _parse_path(argv, i)
            elif argv[i].startswith("-r"):
                rec = True
            #elif argv[i].startswith("-"):
            elif argv[i] not in valid_flags:
                    raise ValueError("flag")
                    
            i += 1
        print (f"URL: {url}\nRecursivety: {rec}\nPath: {path}\nDepth: {depth}")
        set_domain(url)   #change global var
        return(url, depth, path, rec)
        
    except Exception as e:
        print ("Error: please enter : URL (http://, https://)")
        print (f"Options: -r (recursive), -l + Number (lenght depth), -p + path (save images directory)\n\nError: >>> {e} <<<")
        return None

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
        url = normalize(url)
        if url in visited:
            #print ("alredy visited")
            return
        visited.add(url)
        #only to debugging
        if count_depth >= depth:
            #print (f"below depth: {count_depth}")
            return
        
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Spider42/1.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"Spider: Link ok:")
        except Exception as e:
            print(f"\nSpider: error URL: {e}")
            return

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
                next_domain = urlparse(next_url).netloc
                if next_domain != DOMAIN:
                    continue
                if next_url.startswith(("http://", "https://")):
                    crawl(visited, next_url, depth, path, count_depth + 1)
        
    except Exception as e:
            print(f"Error in Crawl: {e}")
    
