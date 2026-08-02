# -*- coding: utf-8 -*-
"""Static site generator — Bruno Vinícius Interior Design.
Builds a multilingual one-page site + blog (EN, ES, IT, FR, PT) with SEO.

Usage: python build.py   (run from project root)
"""
import json
import os
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "scripts"))

from content_site import LANGUAGES, DEFAULT_LANG, SITE, PROJECTS, CONTACT, IMAGES
from content_blog import BLOG as BLOG_EN
from content_blog_es import BLOG as BLOG_ES
from content_blog_it import BLOG as BLOG_IT
from content_blog_fr import BLOG as BLOG_FR
from content_blog_pt import BLOG as BLOG_PT

BLOGS = {"en": BLOG_EN, "es": BLOG_ES, "it": BLOG_IT, "fr": BLOG_FR, "pt": BLOG_PT}

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "site")
ASSETS_SRC = os.path.join(SRC, "assets")

BASE_URL = "https://brunovinicius.design"
YEAR = date.today().year

DOMAIN_EMAIL = CONTACT["email"]


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def lang_path(lang, sub=""):
    prefix = LANGUAGES[lang]["prefix"]
    return (prefix + sub) or "/"


def full_url(lang, sub=""):
    return BASE_URL + (lang_path(lang, sub) if lang_path(lang, sub) != "/" else "/")


# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------

def hreflang_block(lang, sub=""):
    links = []
    for code, meta in LANGUAGES.items():
        h = "x-default" if (code == DEFAULT_LANG and sub == "") else code
        links.append(f'<link rel="alternate" hreflang="{h}" href="{full_url(code, sub)}">')
    cur = full_url(lang, sub)
    return "\n".join(links) + f'\n<link rel="canonical" href="{cur}">'


def og_block(lang, title, desc, url, image):
    img = BASE_URL + IMAGES["og"]
    return (
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:site_name" content="Bruno Vinícius">\n'
        f'<meta property="og:title" content="{esc(title)}">\n'
        f'<meta property="og:description" content="{esc(desc)}">\n'
        f'<meta property="og:url" content="{url}">\n'
f'<meta property="og:image" content="{esc(BASE_URL)}/assets/img/og.jpg">\n'
    f'<meta name="twitter:card" content="summary_large_image">\n'
    f'<meta name="twitter:title" content="{esc(title)}">\n'
    f'<meta name="twitter:description" content="{esc(desc)}">\n'
    f'<meta name="twitter:image" content="{esc(BASE_URL)}/assets/img/og.jpg">'
    )


def head(lang, title, desc, sub="", extra=""):
    meta = LANGUAGES[lang]
    html_lang = meta["html"]
    rel = "assets/css/main.css"
    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Bruno Vinícius">
{hreflang_block(lang, sub)}
{og_block(lang, title, desc, full_url(lang, sub), IMAGES["og"])}
<link rel="icon" type="image/svg+xml" href="/assets/img/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Manrope:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}">
<style>noscript [data-reveal],noscript [data-reveal="late"]{{opacity:1;transform:none}}</style>
{extra}
<script>document.documentElement.classList.add('js-reveal');if(!('IntersectionObserver' in window)){{var all=document.querySelectorAll('[data-reveal]');for(var i=0;i<all.length;i++)all[i].classList.add('revealed')}}</script>
</head>
"""


def nav(lang, onepage=True):
    s = SITE[lang]
    root = LANGUAGES[lang]["root"]
    prefix = LANGUAGES[lang]["prefix"]
    a = lambda anchor: (f"{root}#{anchor}" if onepage else root)
    lang_switcher = ""
    options = "".join(
        f'<option value="{LANGUAGES[code]["root"]}"{" selected" if code == lang else ""}>{meta["native"]}</option>'
        for code, meta in LANGUAGES.items()
    )
    lang_switcher = f'<label class="lang-wrap"><span class="sr-only">Language / Idioma / Lingua / Langue / Idioma</span><select class="lang-switcher" aria-label="Change language">{options}</select></label>'
    links = [
        ("work", s["nav"]["work"]),
        ("about", s["nav"]["about"]),
        ("services", s["nav"]["services"]),
        ("journal", s["nav"]["journal"]),
        ("contact", s["nav"]["contact"]),
    ]
    items = "".join(
        f'<a class="nav-link" href="{a(k)}">{v}</a>' for k, v in links
    )
    return f"""<header class="site-nav" data-nav>
  <div class="container nav-inner">
    <a class="brand" href="{root}" aria-label="Bruno Vinícius — {esc(s['studio'])}">
      <span class="brand-name">{esc(s["brand"])}</span>
      <span class="brand-sub">{esc(s["studio"])}</span>
    </a>
    <nav class="nav-links" aria-label="Primary">
      {items}
      {lang_switcher}
      <a class="btn btn-accent nav-cta" href="{root}#contact">{esc(s["nav"]["cta"])}</a>
      <button class="nav-burger" data-burger aria-label="Menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </nav>
  </div>
  <nav class="mobile-menu" data-mobile aria-hidden="true">
    {items}
    <a class="btn btn-accent" href="{root}#contact">{esc(s["nav"]["cta"])}</a>
  </nav>
</header>
"""


def footer(lang):
    s = SITE[lang]
    root = LANGUAGES[lang]["root"]
    fb = []
    for code, meta in LANGUAGES.items():
        fb.append(f'<a href="{meta["root"]}">{meta["native"]}</a>')
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div>
        <p class="footer-tagline">{esc(s["footer"]["tagline"])}</p>
        <p class="footer-remote">{esc(s["contact"]["remote"])}</p>
      </div>
      <nav class="footer-nav" aria-label="Footer">
        <p class="footer-h">{esc(s["footer"]["nav"])}</p>
        <a href="{root}#work">{esc(s["nav"]["work"])}</a>
        <a href="{root}#about">{esc(s["nav"]["about"])}</a>
        <a href="{root}#services">{esc(s["nav"]["services"])}</a>
        <a href="{root}#journal">{esc(s["nav"]["journal"])}</a>
        <a href="{root}#contact">{esc(s["nav"]["contact"])}</a>
      </nav>
      <nav class="footer-nav" aria-label="Languages">
        <p class="footer-h">{esc(SITE[lang]["nav"]["journal"] if False else "Languages")}</p>
        {''.join(fb)}
      </nav>
    </div>
    <div class="footer-bottom">
      <span>© {YEAR} {esc(s["brand"])}. {esc(s["footer"]["legal"])}</span>
      <span>{esc(s["footer"]["based"])}</span>
    </div>
  </div>
</footer>
"""


def close():
    return "</body></html>"


def lang_links_for_post(lang, slug):
    items = []
    for code, meta in LANGUAGES.items():
        if code == lang:
            continue
        items.append(f'<a href="{meta["prefix"]}/blog/{slug}.html">{meta["native"]}</a>')
    return " · ".join(items)


def project_image(proj):
    return "/assets/img/" + proj["image"]


# ---------------------------------------------------------------------------
# Sections (onepage)
# ---------------------------------------------------------------------------

def section_hero(lang):
    s = SITE[lang]["hero"]
    root = LANGUAGES[lang]["root"]
    return f"""<section class="hero" id="top">
  <div class="container hero-grid">
    <div class="hero-copy" data-reveal>
      <p class="hero-eyebrow">{esc(s["eyebrow"])}</p>
      <h1 class="hero-title">{esc(s["h1_before"])} <em>{esc(s["h1_em"])}</em></h1>
      <p class="hero-sub">{esc(s["sub"])}</p>
      <div class="hero-ctas">
        <a class="btn btn-accent" href="{root}#contact">{esc(s["cta_primary"])}</a>
        <a class="btn btn-ghost" href="{root}#work">{esc(s["cta_secondary"])}</a>
      </div>
    </div>
    <figure class="hero-media" data-reveal="late">
      <img src="/assets/img/hero.jpg" alt="{esc(SITE[lang]["meta"]["title"])}" width="2000" height="1142" fetchpriority="high">
    </figure>
  </div>
  <a class="hero-scroll" href="#statement" aria-label="{esc(s['scroll'])}"><span></span></a>
</section>
"""


def section_statement(lang):
    s = SITE[lang]["statement"]
    return f"""<section class="statement" id="statement" data-reveal>
  <div class="container">
    <p class="statement-text">{esc(s["text"])}</p>
  </div>
</section>
"""


def project_card(proj, lang):
    s = SITE[lang]
    name = proj["name"][lang]
    cat = proj["cat"][lang]
    loc = proj["loc"][lang]
    blurb = proj["blurb"][lang]
    tall = "tall" if proj.get("tall") else ""
    return f"""<article class="project {tall}" data-cat="{esc(cat)}" data-reveal>
  <figure class="project-media">
    <img src="{project_image(proj)}" alt="{esc(name)} — {esc(cat)}, {esc(loc)}" loading="lazy" width="940" height="627">
    <figcaption class="project-cap">
      <span class="project-cat">{esc(cat)}</span>
      <span class="project-loc">{esc(loc)} · {proj["year"]}</span>
    </figcaption>
  </figure>
  <div class="project-body">
    <h3 class="project-name">{esc(name)}</h3>
    <p class="project-blurb">{esc(blurb)}</p>
  </div>
</article>
"""


def section_work(lang):
    s = SITE[lang]["work"]
    root = LANGUAGES[lang]["root"]
    cards = "".join(project_card(p, lang) for p in PROJECTS)
    return f"""<section class="work" id="work">
  <div class="container">
    <header class="sec-head" data-reveal>
      <h2 class="sec-title">{esc(s["title"])}</h2>
      <p class="sec-sub">{esc(s["sub"])}</p>
    </header>
    <div class="work-filter" data-reveal aria-label="Filter">
      <button class="chip active" data-filter="all">{esc(s["filter_all"])}</button>
      <button class="chip" data-filter="Residential">{esc(SITE[lang]["nav"]["work"]) if False else "Residential"}</button>
    </div>
    <div class="work-grid">
      {cards}
    </div>
    <p class="work-note">{esc(s["view_all"])}</p>
  </div>
</section>
"""


def section_about(lang):
    s = SITE[lang]["about"]
    root = LANGUAGES[lang]["root"]
    steps = ""
    for i, st in enumerate(s["process"], 1):
        steps += f"""<div class="proc-step" data-reveal>
          <span class="proc-num">{i:02d}</span>
          <div>
            <h3 class="proc-name">{esc(st["t"])}</h3>
            <p class="proc-desc">{esc(st["d"])}</p>
          </div>
        </div>"""
    return f"""<section class="about" id="about">
  <div class="container">
    <div class="about-grid">
      <figure class="about-media" data-reveal>
        <img src="{IMAGES['about']}" alt="Studio — {esc(SITE[lang]["brand"])}" loading="lazy" width="940" height="627">
      </figure>
      <div class="about-copy" data-reveal="late">
        <h2 class="sec-title">{esc(s["heading"])}</h2>
        <p>{esc(s["p1"])}</p>
        <p>{esc(s["p2"])}</p>
        <p>{esc(s["p3"])}</p>
        <p class="about-note">{esc(s["note"])}</p>
      </div>
    </div>
    <div class="process">
      <h3 class="process-title">{esc(s["process_title"])}</h3>
      <div class="process-grid">
        {steps}
      </div>
    </div>
  </div>
</section>
"""


def section_services(lang):
    s = SITE[lang]["services"]
    items = ""
    for i, it in enumerate(s["items"], 1):
        items += f"""<div class="service" data-reveal>
          <span class="service-num">{i:02d}</span>
          <div>
            <h3 class="service-name">{esc(it["t"])}</h3>
            <p class="service-desc">{esc(it["d"])}</p>
          </div>
        </div>"""
    return f"""<section class="services" id="services">
  <div class="container">
    <header class="sec-head" data-reveal>
      <h2 class="sec-title">{esc(s["title"])}</h2>
      <p class="sec-sub">{esc(s["sub"])}</p>
    </header>
    <div class="services-grid">
      {items}
    </div>
  </div>
</section>
"""


def section_testimonials(lang):
    s = SITE[lang]["testimonials"]
    items = "".join(
        f"""<figure class="quote" data-reveal>
          <blockquote>{esc(t["q"])}</blockquote>
          <figcaption><strong>{esc(t["a"])}</strong><span>{esc(t["r"])}</span></figcaption>
        </figure>"""
        for t in s["items"]
    )
    return f"""<section class="testimonials" id="testimonials">
  <div class="container">
    <header class="sec-head" data-reveal>
      <h2 class="sec-title">{esc(s["title"])}</h2>
    </header>
    <div class="quotes-grid">
      {items}
    </div>
  </div>
</section>
"""


def journal_card(post, lang):
    s = SITE[lang]["journal"]
    blog = SITE[lang]["blog"]
    prefix = LANGUAGES[lang]["prefix"]
    cat = post["category"]
    url = f"{prefix}/blog/{post['slug']}.html"
    return f"""<article class="jcard" data-reveal>
  <a href="{url}" class="jcard-link">
    <figure class="jcard-media">
      <img src="/assets/img/{post['image']}" alt="{esc(post['title'])}" loading="lazy" width="940" height="627">
    </figure>
    <div class="jcard-meta"><span>{esc(cat)}</span><span>{post["read_time"]} min</span></div>
    <h3 class="jcard-title">{esc(post["title"])}</h3>
    <p class="jcard-excerpt">{esc(post["excerpt"])}</p>
    <span class="jcard-more">{esc(blog["read_more"])} →</span>
  </a>
</article>
"""


def section_journal(lang):
    s = SITE[lang]["journal"]
    prefix = LANGUAGES[lang]["prefix"]
    posts = BLOGS[lang][:3]
    cards = "".join(journal_card(p, lang) for p in posts)
    return f"""<section class="journal" id="journal">
  <div class="container">
    <header class="sec-head" data-reveal>
      <h2 class="sec-title">{esc(s["title"])}</h2>
      <p class="sec-sub">{esc(s["sub"])}</p>
    </header>
    <div class="jgrid">
      {cards}
    </div>
    <p class="journal-all"><a href="{prefix}/blog/index.html">{esc(s["all"])} →</a></p>
  </div>
</section>
"""


def section_contact(lang):
    s = SITE[lang]["contact"]
    return f"""<section class="contact" id="contact">
  <div class="container contact-grid">
    <div class="contact-copy" data-reveal>
      <h2 class="sec-title">{esc(s["title"])}</h2>
      <p class="contact-sub">{esc(s["sub"])}</p>
      <div class="contact-channels">
        <a href="mailto:{DOMAIN_EMAIL}" class="contact-mail">{DOMAIN_EMAIL}</a>
        <a href="{CONTACT['instagram_url']}" target="_blank" rel="noopener">{esc(s["ig"])} — @{CONTACT["instagram"]}</a>
      </div>
      <p class="contact-remote">{esc(s["remote"])}</p>
    </div>
    <form class="contact-form" data-form data-reveal="late" novalidate>
      <div class="field">
        <label for="f-name">{esc(s["name"])}</label>
        <input id="f-name" name="name" type="text" autocomplete="name" required>
      </div>
      <div class="field">
        <label for="f-email">{esc(s["email"])}</label>
        <input id="f-email" name="email" type="email" autocomplete="email" required>
      </div>
      <div class="field">
        <label for="f-type">{esc(s["type"])}</label>
        <input id="f-type" name="type" type="text" placeholder="{esc(s['type_placeholder'])}">
      </div>
      <div class="field">
        <label for="f-msg">{esc(s["message"])}</label>
        <textarea id="f-msg" name="message" rows="5" required></textarea>
      </div>
      <button type="submit" class="btn btn-accent btn-submit">{esc(s["submit"])}</button>
      <p class="form-feedback" role="status" aria-live="polite"></p>
      <p class="form-direct">{esc(s["direct"])}: <a href="mailto:{DOMAIN_EMAIL}">{DOMAIN_EMAIL}</a></p>
    </form>
  </div>
</section>
"""


def render_home(lang):
    s = SITE[lang]
    body = "".join([
        nav(lang, onepage=True),
        section_hero(lang),
        section_statement(lang),
        section_work(lang),
        section_about(lang),
        section_services(lang),
        section_testimonials(lang),
        section_journal(lang),
        section_contact(lang),
        footer(lang),
    ])
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": f"{s['brand']} — {s['studio']}",
        "description": s["meta"]["description"],
        "url": full_url(lang),
        "image": BASE_URL + IMAGES["og"],
        "email": DOMAIN_EMAIL,
        "sameAs": [CONTACT["instagram_url"]],
        "priceRange": "$$",
        "areaServed": "Worldwide",
        "founder": {"@type": "Person", "name": s["brand"]},
    }, ensure_ascii=False)
    return head(lang, s["meta"]["title"], s["meta"]["description"]) + (
        f'<script type="application/ld+json">{schema}</script>\n'
        f'<body class="home">\n{body}\n'
        f'<script src="assets/js/main.js" defer></script>\n{close()}'
    )


# ---------------------------------------------------------------------------
# Blog pages
# ---------------------------------------------------------------------------

def render_blocks(blocks):
    out = []
    for b in blocks:
        t = b["t"]
        c = b["c"]
        if t == "h2":
            out.append(f"<h2>{esc(c)}</h2>")
        elif t == "p":
            out.append(f"<p>{esc(c)}</p>")
        elif t == "quote":
            out.append(f"<blockquote>{esc(c)}</blockquote>")
        elif t == "ul":
            lis = "".join(f"<li>{esc(x)}</li>" for x in c)
            out.append(f"<ul>{lis}</ul>")
    return "\n".join(out)


def render_blog_index(lang):
    s = SITE[lang]
    blog = s["blog"]
    posts = BLOGS[lang]
    prefix = LANGUAGES[lang]["prefix"]
    cards = "".join(journal_card(p, lang) for p in posts)
    body = "".join([
        nav(lang, onepage=False),
        f"""<main class="blog-index">
          <div class="container">
            <header class="blog-head" data-reveal>
              <h1 class="blog-title">{esc(blog["title"])}</h1>
              <p class="blog-sub">{esc(blog["sub"])}</p>
            </header>
            <div class="jgrid blog-grid">{cards}</div>
          </div>
        </main>""",
        footer(lang),
    ])
    return head(lang, f"{blog['title']} — {s['brand']} · {s['studio']}", blog["sub"], sub="/blog/index.html") + (
        f'<body class="inner">\n{body}\n'
        f'<script src="assets/js/main.js" defer></script>\n{close()}'
    )


def render_blog_post(lang, index):
    s = SITE[lang]
    blog = s["blog"]
    posts = BLOGS[lang]
    post = posts[index]
    prefix = LANGUAGES[lang]["prefix"]
    prev = posts[index - 1] if index > 0 else None
    nxt = posts[index + 1] if index < len(posts) - 1 else None

    meta = post.get("meta") or post["excerpt"]
    url = full_url(lang, f"/blog/{post['slug']}.html")
    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post["excerpt"],
        "image": BASE_URL + "/assets/img/" + post["image"],
        "datePublished": post["date"],
        "author": {"@type": "Person", "name": "Bruno Vinícius"},
        "publisher": {"@type": "ProfessionalService", "name": s["brand"]},
        "mainEntityOfPage": url,
        "inLanguage": LANGUAGES[lang]["html"],
    }, ensure_ascii=False)

    pager = ""
    if prev:
        pager += f'<a class="pager" href="{prefix}/blog/{prev["slug"]}.html"><span>{esc(blog["prev"])}</span><strong>{esc(prev["title"])}</strong></a>'
    if nxt:
        pager += f'<a class="pager pager-next" href="{prefix}/blog/{nxt["slug"]}.html"><span>{esc(blog["next"])}</span><strong>{esc(nxt["title"])}</strong></a>'

    body = "".join([
        nav(lang, onepage=False),
        f"""<main class="post">
          <div class="container post-container">
            <article>
              <header class="post-head" data-reveal>
                <p class="post-meta"><span>{esc(post["category"])}</span><span>{esc(blog["by"])}</span><span>{post["read_time"]} min</span></p>
                <h1 class="post-title">{esc(post["title"])}</h1>
                <p class="post-excerpt">{esc(post["excerpt"])}</p>
              </header>
              <figure class="post-hero" data-reveal>
                <img src="/assets/img/{post['image']}" alt="{esc(post['title'])}" width="940" height="627">
              </figure>
              <div class="post-body" data-reveal>
                {render_blocks(post["blocks"])}
              </div>
            </article>
            <aside class="post-langs">
              <p>{esc(blog["other_langs"])}</p>
              <p>{lang_links_for_post(lang, post["slug"])}</p>
            </aside>
            <nav class="pager-wrap" aria-label="Pagination">
              {pager}
            </nav>
            <p class="post-back"><a href="{prefix}/blog/index.html">← {esc(blog["back"])}</a></p>
          </div>
        </main>""",
        footer(lang),
    ])
    return head(lang, f"{post['title']} — {s['brand']}", meta, sub=f"/blog/{post['slug']}.html",
                extra=f'<script type="application/ld+json">{article_schema}</script>') + (
        f'<body class="inner">\n{body}\n'
        f'<script src="assets/js/main.js" defer></script>\n{close()}'
    )


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    # assets
    shutil.copytree(ASSETS_SRC, os.path.join(OUT, "assets"))

    urls = []
    lang_pairs = []
    for lang in LANGUAGES:
        ldir = os.path.join(OUT, lang) if lang != DEFAULT_LANG else OUT
        os.makedirs(os.path.join(ldir, "blog"), exist_ok=True)
        lroot = LANGUAGES[lang]["root"]

        with open(os.path.join(ldir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_home(lang))
        urls.append(lroot)
        lang_pairs.append((lang, "/"))

        with open(os.path.join(ldir, "blog", "index.html"), "w", encoding="utf-8") as f:
            f.write(render_blog_index(lang))
        urls.append(f"{lroot}blog/index.html")

        for i, post in enumerate(BLOGS[lang]):
            fname = os.path.join(ldir, "blog", f"{post['slug']}.html")
            with open(fname, "w", encoding="utf-8") as f:
                f.write(render_blog_post(lang, i))
            urls.append(f"{lroot}blog/{post['slug']}.html")

    # 404 (root)
    en = SITE[DEFAULT_LANG]
    notfound = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>404 — {esc(en['404']['title'])}</title>
<link rel="stylesheet" href="assets/css/main.css">
<meta http-equiv="refresh" content="0; url=/">
</head>
<body class="inner">
<main class="nf">
  <h1 class="nf-title">404</h1>
  <p>{esc(en['404']['text'])}</p>
  <a class="btn btn-accent" href="/">{esc(en['404']['back'])}</a>
</main>
</body></html>"""
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(notfound)

    # robots.txt
    robots = "User-agent: *\nAllow: /\nDisallow: /assets/\n\nSitemap: " + BASE_URL + "/sitemap.xml\n"
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    # sitemap.xml
    locs = "".join(
        f"  <url><loc>{full_url_for(l)}</loc></url>\n" for l in urls
    )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{locs}</urlset>
"""
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    # report
    count = sum(len(v) for v in BLOGS.values())
    print(f"Built {OUT}")
    print(f"Languages: {list(LANGUAGES)} | Articles per language: {len(BLOG_EN)} | Total pages incl. blog: {len(urls)}")
    print(f"Blog articles total: {count}")


def full_url_for(l):
    if l.startswith("http"):
        return l
    return BASE_URL + (l if l != "/" else "/")


if __name__ == "__main__":
    main()
