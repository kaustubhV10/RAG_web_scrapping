import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import re

SEED = "https://docs.github.com/en/rest"
DOMAIN = "docs.github.com"
OUTFILE = "github_docs.jsonl"

def normalize_text(s):
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_sections(soup, url):
    results = []
    container = soup.find('main') or soup.find('article') or soup
    headers = container.find_all(['h1','h2','h3','h4'])
    if not headers:
        titles = soup.title.string if soup.title else ""
        text = normalize_text(container.get_text(" ", strip=True))
        if text:
            results.append({'url':url, 'heading':titles, "text":text})
        return results
    
    for h in headers:
        texts = []
        node = h.next_sibling
        while node:
            if getattr(node, 'name', None) in ['h1','h2','h3','h4']:
                break

            if getattr(node, 'get_text', None):
                txt = node.get_text(" ", strip=True)
                if txt:
                    texts.append(txt)
            
            node = node.next_sibling
        combined = normalize_text(' '.join(texts))
        heading = normalize_text(h.get_text(" ", strip = True))
        if combined:
            results.append({"url": url, "heading": heading, "text": combined})

    return results

def crawl(seed, max_pages= 100):
    visited = set()
    q = [seed]
    out_f = open(OUTFILE, 'w', encoding='utf8')
    while q and len(visited) < max_pages:
        url = q.pop(0)
        base = url.split('#')[0]
        if base in visited:
            continue
        visited.add(base)
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            soup = BeautifulSoup(r.text,'html.parser')
            sections = extract_sections(soup, url)
            for s in sections:
                out_f.write(json.dumps(s, ensure_ascii=False) + "\n")
            for a in soup.find_all("a", href = True):
                href = a['href']
                if not href.startswith('hhtp'):
                    href = urljoin(url, href)
                if DOMAIN in urlparse(href).netloc and href.split('#')[0] not in visited:
                    q.append(href)
        except Exception as e:
            print(f"falied {url} : {e}")
            continue
    out_f.close()

if __name__ == "__main__":
    crawl(SEED)