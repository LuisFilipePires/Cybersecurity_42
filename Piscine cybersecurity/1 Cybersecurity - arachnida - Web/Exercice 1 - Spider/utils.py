#utils.py

ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
#ALLOWED_EXT = (".jpg", ".jpeg")


from bs4 import BeautifulSoup # BeautifulSoup is used to parse HTML content
from urllib.parse import urljoin # urljoin is used to construct absolute URLs from relative ones
from pathlib import Path # Path is used to handle file paths and directories
import requests # requests module is used to make HTTP requests
import sys
'''
#the best choice to parse

import argparse

parser = argparse.ArgumentParser(description="Spider program")
parser.add_argument("url", help="Starting URL")
parser.add_argument("-r", action="store_true", help="Enable recursion")
parser.add_argument("-l", type=int, default=5, help="Max depth (default=5)")
parser.add_argument("-p", default="./data/", help="Download path")
args = parser.parse_args()
print(f"URL: {args.url}")
print(f"Recursive: {args.r}")
print(f"Depth: {args.l}")
print(f"Path: {args.p}")
'''

def parse_terminal(argv):

    recursive = False
    depth = 5
    path = "./data"
    url = None
    valid_flags = {"-r", "-l", "-p"}
    i = 1

    if (len(argv) <= 1 or len(argv) > 7):
        raise ValueError("\nBAD ENTRY: optional: -r (recursive) -l (+ number of deph) -p (+ path directory)\nMandatory:\t link(http://exemple.com)")

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
    return (url, recursive, depth, path)

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


def crawl(visited, url, depth, recursive, path):
    if depth == 0 or url in visited:
        return

    visited.add(url)
    print(f"\nVisiting: {url} | Depth: {depth}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Spider42/1.0"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code >= 400:
            print(f"Skipping {url}: HTTP {response.status_code}")
            return

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            print(f"Skipping {url}: non-HTML content ({content_type})")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Download images
        download_images(url, soup, path)

        # Recursion
        if recursive:
            found_links = 0
            for link in soup.find_all("a"):
                href = link.get("href")

                if href:
                    next_url = urljoin(url, href)

                    if next_url.startswith(("http://", "https://")):
                        found_links += 1
                        crawl(visited, next_url, depth - 1, recursive, path)

            if found_links == 0:
                print(f"No valid links to recurse from: {url}")

    except requests.exceptions.RequestException:
        print(f"Failed to access {url}")


#Save all html in a .txt file, to avoid 
#save in RAM I used a function 
#agent to prevent robot detection, and to avoid 403 forbidden error
'''
def download1(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Spider42/1.0"
        }

        response = requests.get(url, headers=headers)
        print("Response Type: ")
        print(type(response))

        print(f"Status code: {response.status_code}")

        html = response.text

        with open("page_html.txt", "w", encoding="utf-8") as f:
            f.write(html)

    except Exception as e:
        print("\nBye Bye Spider man\n")
        raise ValueError(f"URL error: {e}")
'''
