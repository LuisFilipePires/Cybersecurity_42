# Cybersecurity - Spider

```
Utils:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
```

Run the program

``` 
./Spider	https://www.example.com
```

By default, the program creates a folder named data/ in the current directory to store all downloaded images.

It downloads all images found on the main page of the given URL.

If the -r option is used, the program will download images recursively from linked pages.

By default, the maximum depth is 5 if no depth is specified with the -l option.

``` -l option followed by a number to set the depth. ```

If -p option is specified, the new path location must be defined.

```
Usage examples:

``` ./Spider https://www.example.com ``` → Downloads images from the main page only (no recursion).
``` ./Spider -r https://www.example.com ``` → Enables recursive download of linked pages with a default depth of 5
``` ./Spider -r -l 7 https://www.example.com ``` → Enables a recursion with a maximum depth of 7
``` ./Spider -r -l 8 -p “./images/all_images”  https://www.example.com ``` → Enables recursion with depth 8 and saves in the custom path (“./image/all_images”)

```	
./Spider -r -l 4 -p “./images”  https://www.example.com
```

### Command Specifications


``` import requests ``` requests module used to make HTTP requests

```text

response = requests.get(url)
The HTML is stored at RAM memory
To extract text, use: variable = response.text
To Save in .txt file
html = response.text
with open("page_html.txt", "w", encoding="utf-8") as f: f.write(html)
The response variable is a object from the Requests library
Successful responses 200 OK
<Response [200]>
	The request succeeded. The result and meaning of "success" depends on the HTTP method:

GET: The resource has been fetched and transmitted in the message body.
HEAD: Representation headers are included in the response without any message body.
PUT or POST: The resource describing the result of the action is transmitted in the message body.
TRACE: The message body contains the request as received by the server.
Inside response
    • response.text → HTML (text from the page) 
    • response.content → raw content (bytes, used  for images, PDF s, etc.) 
    • response.status_code → code HTTP (200, 404, etc.) 
    • response.headers → headers from response
set()
visited = set(), creates a together (conjunto) like a list. To saves all the links hurl’s
visited.add(url) add at
visdited.remove(url)

```

### Spider Project - Workflow Overview

```text
1. Command Line Parsing
The program starts by parsing the command-line arguments:
    • URL (mandatory) 
    • -r : enable recursive crawling 
    • -l <depth> : define recursion depth 
    • -p <path> : define the image download directory 
The parser validates:
    • URL format (http:// or https://) 
    • depth value 
    • destination path 
    • duplicate URLs 
    • invalid flags 
The target domain is extracted and stored globally to prevent the crawler from leaving the original website.

```


### 2. Domain Restriction

```
The crawler only visits pages belonging to the original domain.
Example:
https://example.com
Allowed:
https://example.com/about
https://example.com/contact
Ignored:
https://google.com
https://github.com
This prevents the crawler from traversing the entire internet.
```


### 3. URL Normalization

```
Before storing a URL in the visited set, it is normalized:
    • query parameters are removed 
    • fragments are removed 
    • trailing slashes are removed 
Example:
https://example.com/page?id=123#section
becomes:
https://example.com/page
This helps avoid revisiting the same page multiple times.
```


### 4. HTTP Requests

```
The crawler uses the Python requests library to retrieve web pages.
A custom User-Agent header is sent:
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Spider42/1.0"
}
Why?
Many websites reject requests that look like automated bots.
Using a browser-like User-Agent makes the request appear similar to a normal web browser and improves compatibility with websites.
```

### 5. HTML Validation

```
After downloading a page, the program checks its Content-Type:
Content-Type: text/html
Only HTML documents are processed.
Other content types such as:
image/jpeg
application/pdf
video/mp4
are ignored.
```


### 6. HTML Parsing

```
The HTML document is parsed using BeautifulSoup:
soup = BeautifulSoup(response.text, "html.parser")
BeautifulSoup allows the crawler to:
    • extract images (<img>) 
    • extract hyperlinks (<a>) 
    • navigate through the HTML structure 
```

### 7. Image Downloading

```
For every image tag found:
<img src="image.jpg">
The crawler:
    1. Extracts the image URL 
    2. Converts relative URLs into absolute URLs using urljoin() 
    3. Downloads the image 
    4. Verifies that the content is actually an image 
    5. Saves it to the destination directory 
Supported image formats:
(".jpg", ".jpeg", ".png", ".gif", ".bmp")
```


### 8. Recursive Crawling

```
Every hyperlink found on the page is processed:
<a href="/about">
The crawler:
    1. Builds the absolute URL 
    2. Checks if it belongs to the original domain 
    3. Checks if it was already visited 
    4. Verifies that the maximum depth has not been reached 
    5. Recursively calls crawl() 
This creates a depth-first traversal of the website.
```


### 9. Visited URL Tracking

```
A Python set is used to store previously visited URLs:
visited = set()
Before visiting a page:
if url in visited:
    return
This prevents:
    • infinite loops 
    • duplicate requests 
    • unnecessary network traffic 
```


### 10. Program Termination

```
The crawler handles Ctrl+C gracefully:
except KeyboardInterrupt:
    print("Closing crawler… Ctrl+C detected")
This allows the user to stop the crawl safely without displaying a Python traceback.
```


### Technologies Used

```
    • Python 3 
    • Requests 
    • BeautifulSoup4 
    • Pathlib 
    • urllib.parse 
    • Colorama 
General Workflow
Parse Arguments
       ↓
Validate Input
       ↓
Set Original Domain
       ↓
Download Page
       ↓
Check Content-Type
       ↓
Parse HTML
       ↓
Download Images
       ↓
Extract Links
       ↓
Domain Check
       ↓
Visited Check
       ↓
Recursive Crawl
       ↓
Stop at Max Depth
```
