import os, sys, urllib.request
BASE = r"C:\Users\Admin\Desktop\Projetos\bruno-vinicius-interiores"
VAULT = r"C:\Users\Admin\Desktop\TS Digitais\IA\.ia-config\credentials\.env.master"
SERVER = r"C:\Users\Admin\Desktop\TS Digitais\IA\.ia-config\mcp-servers\image-search-mcp\server.py"
sys.path.insert(0, os.path.dirname(SERVER))
def load_vault(p):
    env={}
    for line in open(p,encoding="utf-8"):
        line=line.strip()
        if not line or line.startswith("#") or "=" not in line: continue
        k,_,v=line.partition("="); env[k.strip()]=v.strip().strip("\"'")
    return env
for k,v in load_vault(VAULT).items(): os.environ.setdefault(k,v)
import server as imgmcp
UA={"User-Agent":"Mozilla/5.0"}
res=imgmcp.search_images("modern luxury living room interior with sofa", source="pexels", page=1, per_page=20)
best=None
for im in res.get("images",[]):
    w,h=im.get("width",0),im.get("height",0)
    if not w or not h: continue
    ratio=w/h
    if 1.7<=ratio<=2.1 and (best is None or w>best[1]["width"]):
        best=(ratio,im)
im=best[1]
out=os.path.join(BASE,"src","assets","img","hero.jpg")
req=urllib.request.Request(im["download_url"],headers=UA)
with urllib.request.urlopen(req,timeout=90) as r: data=r.read()
open(out,"wb").write(data)
print("saved", len(data), "ratio", best[0], im["description"], "|", im["author"], im["download_url"])
from PIL import Image
p=Image.open(out); print("orig", p.size)
if p.width>2000:
    p=p.resize((2000,int(p.height*2000/p.width)), Image.LANCZOS)
p.save(out,"JPEG",quality=78,optimize=True,progressive=True)
print("final", Image.open(out).size)
