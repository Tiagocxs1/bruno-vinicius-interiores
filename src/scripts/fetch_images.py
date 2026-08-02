"""Fetch real interior-design photos via the image-search MCP engine and download them locally."""
import json
import os
import sys
import urllib.request

BASE = r"C:\Users\Admin\Desktop\Projetos\bruno-vinicius-interiores"
VAULT = r"C:\Users\Admin\Desktop\TS Digitais\IA\.ia-config\credentials\.env.master"
SERVER = r"C:\Users\Admin\Desktop\TS Digitais\IA\.ia-config\mcp-servers\image-search-mcp\server.py"

sys.path.insert(0, os.path.dirname(SERVER))


def load_vault(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip("\"'")
    return env


for k, v in load_vault(VAULT).items():
    os.environ.setdefault(k, v)

import server as imgmcp

QUERIES = {
    "hero": ("luxury modern living room interior design", "pexels", 1, 6),
    "project-sala": ("elegant scandinavian living room interior", "pexels", 1, 6),
    "project-cozinha": ("modern minimalist kitchen interior design", "pexels", 1, 6),
    "project-quarto": ("serene bedroom interior design", "pexels", 1, 6),
    "project-escritorio": ("modern home office interior design", "pexels", 1, 6),
    "project-restaurante": ("hotel lobby luxury interior", "pexels", 1, 6),
    "project-luminaria": ("warm ambient lighting lamp interior", "pexels", 1, 6),
    "detalhe-textura": ("architectural interior natural light detail", "pexels", 1, 6),
    "detalhe-marmore": ("marble interior texture detail", "pexels", 1, 6),
    "detalhe-veludo": ("velvet sofa detail interior", "pexels", 1, 6),
    "studio-1": ("interior designer studio workspace", "pexels", 1, 5),
    "blog-1": ("small apartment interior design", "pexels", 1, 5),
    "blog-2": ("colorful interior decor palette", "pexels", 1, 5),
    "blog-3": ("bedroom lighting design cozy", "pexels", 1, 5),
    "blog-4": ("modern interior design trend", "pexels", 1, 5),
    "blog-5": ("minimalist interior design process", "pexels", 1, 5),
    "blog-6": ("interior design mistake renovation", "pexels", 1, 5),
    "og": ("contemporary interior design mood", "unsplash", 1, 6),
}

OUT = os.path.join(BASE, "src", "assets", "img")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) image-fetch/1.0"}


def pick(results, preferred_keyword):
    images = results.get("images", [])
    if not images:
        return None
    if preferred_keyword:
        for im in images:
            desc = (im.get("description") or "").lower()
            if preferred_keyword in desc:
                return im
    return images[0]


def download(url, path):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
        return len(data)
    except Exception as e:
        print("  DL FAIL", path, e)
        return 0


manifest = {}
os.makedirs(OUT, exist_ok=True)
for name, (q, src, page, n) in QUERIES.items():
    res = imgmcp.search_images(q, source=src, page=page, per_page=n)
    if "error" in res or "_error" in res:
        print(f"[{name}] ERROR {res}")
        continue
    im = pick(res, None)
    if not im:
        print(f"[{name}] no results")
        continue
    url = im["download_url"] if name in ("og",) else im["url"]
    if not url:
        url = im["url"]
    fname = f"{name}.jpg"
    size = download(url, os.path.join(OUT, fname))
    manifest[name] = {
        "file": fname,
        "source": res.get("source"),
        "author": im.get("author"),
        "author_url": im.get("author_url"),
        "license": im.get("license"),
        "description": im.get("description"),
        "bytes": size,
        "url": url,
    }
    print(f"[{name}] ok {size} bytes <- {res.get('source')} {im.get('description')}")

with open(os.path.join(BASE, "src", "assets", "data", "images.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print("DONE", json.dumps(manifest, ensure_ascii=False, indent=2))
