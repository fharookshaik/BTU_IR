from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import re

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.current_tag = None
        self.skip_tags = {'script', 'style', 'noscript', 'head', 'title', 'meta', 'link'}
        self.whitespace_re = re.compile(r'\s+')
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag.lower()
        if self.current_tag in self.skip_tags:
            self.text.append(' ')
    
    def handle_endtag(self, tag):
        if tag.lower() in {'p','br','li','div','h1','h2','h3','h4','h5','h6','ul','ol'}:
            self.text.append('\n')
        self.current_tag = None
    
    def handle_data(self, data):
        if self.current_tag not in self.skip_tags and data.strip():
            clean_data = self.whitespace_re.sub(' ', data.strip())
            self.text.append(clean_data)
    
    def get_text(self):
        return ''.join(self.text).strip()


def fetch_text_from_url(url, timeout=10, user_agent=None):
    headers = {'User-Agent': user_agent or 'Mozilla/5.0 (compatible; TextExtractor/1.0)'}

    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError(f"Invalid URL: {url}")
       
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as response:
            if response.status != 200:
                raise HTTPError(url, response.status, "HTTP request failed", response.headers, None)
            
            content_type = response.headers.get('Content-Type', '').lower()
            if 'html' not in content_type:
                raise ValueError(f"Unsupported Content Type: {content_type}")
            
            html_content = response.read().decode('utf-8', errors='replace')

            parser = HTMLTextExtractor()
            parser.feed(html_content)
            return parser.get_text()
    except (URLError, HTTPError, ValueError, TimeoutError) as e:
        print(f"Error processing {url}: {e}")
        return None


urls = []

with open('data/cs_ds_articles.txt','r') as source:
    for line in source.readlines():
        urls.append(line.strip())

documents = [fetch_text_from_url(url) for url in urls]

print(documents[0:10])