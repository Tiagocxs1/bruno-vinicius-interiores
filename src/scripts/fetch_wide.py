import json, os, sys, urllib.request
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
def grab(url,path):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=40) as r: data=r.read()
    open(path,"wb").write(data); return len(data)

OUT=os.path.join(BASE,"src","assets","img")
queries = [
    ("hero", "wide modern luxury living room interior", "pexels"),
    ("hero2", "elegant apartment interior wide", "pexels"),
]
for name,q,src in queries:
    best=None
    for page in (1,2,3):
        res=imgmcp.search_images(q,source=src,page=page,per_page=15)
        for im in res.get("images",[]):
            w,h=im.get("width",0),im.get("height",0)
            if not w or not h: continue
            ratio=w/h
            if 1.5 <= ratio <= 2.2 and (best is None or ratio>best[0]):
                best=(ratio,im)
        if best: break
    if best:
        im=best[1]
        sz=grab(im["url"], os.path.join(OUT,f"{name}.jpg"))
        print(name, best[0], sz, im.get("description"), im["author"], im["url"])
    else:
        print(name, "no wide found")
