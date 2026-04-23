from pathlib import Path # Path is used to handle file paths and directories
import requests # requests module is used to make HTTP requests

from urllib.parse import urljoin # urljoin is used to construct absolute URLs from relative ones
from pathlib import Path # Path is used to handle file paths and directories
import requests # requests module is used to make HTTP requests
import sys

ALLOWED_EXT = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


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
    if not recusive:
        print("\nCaution: recursive is off\n-l flag is only valid with -r")
        depth = 0 
    return (url, recursive, depth, path)