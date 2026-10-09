#!/usr/bin/env python3
"""Static blog generator for Ship Index Grow.

No dependencies beyond the Python standard library, so it runs anywhere for free.
Each post lives in tools/blog/posts/<lang>/<slug>.html: a JSON metadata block
inside the first HTML comment, followed by the article body HTML.

Run from the repository root:  python3 tools/blog/build.py
It writes blog/, blog/uk/, the RSS feeds and sitemap.xml.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POSTS_DIR = Path(__file__).resolve().parent / "posts"
SITE = "https://shipindexgrow.top"
ORG_ID = f"{SITE}/#organization"
WEBSITE_ID = f"{SITE}/#website"
FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Ccircle cx='32' cy='32' r='32' fill='%230b55ff'/%3E%3Ctext x='32' y='36' "
    "text-anchor='middle' font-family='Arial,sans-serif' font-size='17' font-weight='800' "
    "fill='white'%3ESIG%3C/text%3E%3C/svg%3E"
)

LANG = {
    "en": {
        "blog_path": "/blog/",
        "home_path": "/",
        "home_file": "index.html",
        "locale": "en_US",
        "alt_locale": "uk_UA",
        "blog_title": "Blog: AI product building, SEO/GEO and launch | Ship Index Grow",
        "blog_h1": "Field notes on shipping<br><span>products with AI.</span>",
        "blog_description": "Practical guides on building products with AI, getting found in Google and AI search (SEO/GEO), launching and automating growth. From the Ship Index Grow school.",
        "blog_eyebrow": "SHIP INDEX GROW BLOG",
        "blog_lead": "Practical, current guides from the six-week launch school: build with AI, get indexed and cited, grow and automate.",
        "home": "Home",
        "blog": "Blog",
        "program": "Program",
        "format": "Format",
        "join": "Join the course",
        "read": "Read the guide",
        "min_read": "min read",
        "by": "By",
        "published": "Published",
        "updated": "Updated",
        "related": "Keep reading",
        "faq": "Questions people ask",
        "nav_label": "Primary navigation",
        "lang_label": "Language",
        "crumbs_label": "Breadcrumbs",
        "brand_label": "Ship Index Grow home",
        "skip": "Skip to content",
        "footer_tag": "Build. Index. Grow.",
        "contact": "Contact",
        "cta_eyebrow": "FOUNDING COHORT · 20 SEATS",
        "cta_title": "Stop reading. Ship it with us.",
        "cta_text": "Six live weeks, one real product per participant: idea, UX, AI build, SEO/GEO, launch and automation, with direct founder feedback. $490 for the full program.",
        "cta_more": "See the six-week program",
        "rss": "RSS feed",
        "author": "Oleh Hebel",
        "author_role": "Founder of Ship Index Grow",
    },
    "uk": {
        "blog_path": "/blog/uk/",
        "home_path": "/uk",
        "home_file": "uk.html",
        "locale": "uk_UA",
        "alt_locale": "en_US",
        "blog_title": "Блог: створення продуктів із ШІ, SEO/GEO та запуск | Ship Index Grow",
        "blog_h1": "Практика запуску<br><span>продуктів із ШІ.</span>",
        "blog_description": "Практичні гайди українською: як створити продукт із ШІ, потрапити в Google та ШІ-пошук (SEO/GEO), запуститися й автоматизувати просування. Від школи Ship Index Grow.",
        "blog_eyebrow": "БЛОГ SHIP INDEX GROW",
        "blog_lead": "Актуальні практичні гайди від шеститижневої школи запуску: створюй із ШІ, ставай видимим у пошуку, зростай і автоматизуй.",
        "home": "Головна",
        "blog": "Блог",
        "program": "Програма",
        "format": "Формат",
        "join": "Хочу на програму",
        "read": "Читати гайд",
        "min_read": "хв читання",
        "by": "Автор:",
        "published": "Опубліковано",
        "updated": "Оновлено",
        "related": "Читай також",
        "faq": "Часті запитання",
        "nav_label": "Основна навігація",
        "lang_label": "Мова сайту",
        "crumbs_label": "Навігаційний ланцюжок",
        "brand_label": "Ship Index Grow — головна",
        "skip": "Перейти до змісту",
        "footer_tag": "Створюй. Ставай видимим. Зростай.",
        "contact": "Написати нам",
        "cta_eyebrow": "ПЕРШИЙ НАБІР · 20 МІСЦЬ",
        "cta_title": "Досить читати. Запускай разом із нами.",
        "cta_text": "Шість тижнів практики й один реальний продукт на учасника: ідея, UX, створення з ШІ, SEO/GEO, запуск і автоматизація з прямим фідбеком засновника. 25 000 грн за всю програму.",
        "cta_more": "Подивитися програму на 6 тижнів",
        "rss": "RSS-стрічка",
        "author": "Олег Гебель",
        "author_role": "Засновник Ship Index Grow",
    },
}

MONTHS_UK = ["січня", "лютого", "березня", "квітня", "травня", "червня", "липня",
             "серпня", "вересня", "жовтня", "листопада", "грудня"]


def fmt_date(iso, lang):
    d = date.fromisoformat(iso)
    if lang == "uk":
        return f"{d.day} {MONTHS_UK[d.month - 1]} {d.year}"
    return d.strftime("%B ") + str(d.day) + d.strftime(", %Y")


def esc(text):
    return html.escape(text, quote=True)


def load_posts():
    posts = []
    for path in sorted(POSTS_DIR.glob("*/*.html")):
        raw = path.read_text(encoding="utf-8")
        match = re.match(r"\s*<!--(.*?)-->(.*)", raw, re.S)
        if not match:
            raise SystemExit(f"{path}: missing metadata comment")
        meta = json.loads(match.group(1))
        meta["lang"] = path.parent.name
        meta["slug"] = path.stem
        meta["body"] = match.group(2).strip()
        meta["path"] = f"{LANG[meta['lang']]['blog_path']}{meta['slug']}/"
        meta["url"] = SITE + meta["path"]
        words = len(re.sub(r"<[^>]+>", " ", meta["body"]).split())
        meta["minutes"] = max(3, round(words / 220))
        meta["words"] = words
        posts.append(meta)
    by_key = {(p["lang"], p["slug"]): p for p in posts}
    for p in posts:
        other = "uk" if p["lang"] == "en" else "en"
        p["alt"] = by_key.get((other, p.get("translation", "")))
        if p.get("translation") and not p["alt"]:
            raise SystemExit(f"{p['slug']}: translation {p['translation']} not found")
    posts.sort(key=lambda p: (p["published"], p.get("order", 0)), reverse=True)
    return posts


def rel(from_path, to_path):
    """Relative link from one site path to another, so pages also work on project URLs."""
    depth = from_path.strip("/").count("/") + (1 if from_path.strip("/") else 0)
    prefix = "../" * depth
    target = to_path.lstrip("/")
    return (prefix + target) or "./"


def dialog_markup(lang):
    source = (ROOT / LANG[lang]["home_file"]).read_text(encoding="utf-8")
    match = re.search(r"<dialog id=\"applyDialog\".*?</dialog>", source, re.S)
    if not match:
        raise SystemExit("join dialog not found on the home page")
    return match.group(0)


def head(lang, title, description, canonical, alternates, og_type, schema, page_path, extra=""):
    t = LANG[lang]
    links = "\n".join(
        f'  <link rel="alternate" hreflang="{code}" href="{href}">' for code, href in alternates
    )
    feed = SITE + t["blog_path"] + "feed.xml"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta name="author" content="{esc(t['author'])}">
  <link rel="canonical" href="{canonical}">
{links}
  <link rel="alternate" type="application/rss+xml" title="Ship Index Grow — {esc(t['blog'])}" href="{feed}">
  <meta name="theme-color" content="#0b55ff">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Ship Index Grow">
  <meta property="og:locale" content="{t['locale']}">
  <meta property="og:locale:alternate" content="{t['alt_locale']}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
{extra}  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <link rel="icon" type="image/svg+xml" href="{FAVICON}">
  <link rel="stylesheet" href="{rel(page_path, '/styles.css')}">
  <script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
</script>
</head>"""


def header(lang, page_path, switch_href_en, switch_href_uk):
    t = LANG[lang]
    home = rel(page_path, t["home_path"])
    blog = rel(page_path, t["blog_path"])
    cur_en = ' aria-current="page"' if lang == "en" else ""
    cur_uk = ' aria-current="page"' if lang == "uk" else ""
    return f"""<body class="blog-page">
  <a class="skip" href="#main">{t['skip']}</a>
  <header class="nav">
    <a class="brand" href="{home}" aria-label="{esc(t['brand_label'])}"><span class="brand-mark">SIG</span><span>SHIP INDEX GROW</span></a>
    <nav aria-label="{esc(t['nav_label'])}">
      <a href="{home}#program">{t['program']}</a><a href="{home}#format">{t['format']}</a><a href="{blog}">{t['blog']}</a>
    </nav>
    <div class="nav-actions"><button class="button button-small js-open">{t['join']}</button><nav class="language-switch" aria-label="{esc(t['lang_label'])}"><a href="{switch_href_en}" lang="en" hreflang="en"{cur_en}>English</a><a href="{switch_href_uk}" lang="uk" hreflang="uk"{cur_uk}>Ukrainian</a></nav></div>
  </header>
"""


def cta(lang, page_path):
    t = LANG[lang]
    home = rel(page_path, t["home_path"])
    return f"""<aside class="blog-cta" aria-label="{esc(t['cta_eyebrow'])}">
        <p class="eyebrow">{t['cta_eyebrow']}</p>
        <h2>{t['cta_title']}</h2>
        <p>{t['cta_text']}</p>
        <div class="hero-actions"><button class="button button-light js-open">{t['join']} <span>↗</span></button><a class="text-link" href="{home}#program">{t['cta_more']} →</a></div>
      </aside>"""


def footer(lang, page_path):
    t = LANG[lang]
    home = rel(page_path, t["home_path"])
    blog = rel(page_path, t["blog_path"])
    return f"""  <footer><a class="brand" href="{home}"><span class="brand-mark">SIG</span><span>SHIP INDEX GROW</span></a><p>{t['footer_tag']}</p><a class="footer-link" href="{blog}">{t['blog']}</a><a class="footer-link" href="mailto:doctorgebel@gmail.com">{t['contact']}</a><a class="footer-link footer-social" href="https://www.linkedin.com/in/olehhebel/" target="_blank" rel="noopener">LinkedIn</a><span>© 2026 SHIP INDEX GROW</span></footer>

  {dialog_markup(lang)}
  <script src="{rel(page_path, '/app.js')}" defer></script>
</body>
</html>
"""


def person(lang):
    t = LANG[lang]
    return {
        "@type": "Person",
        "@id": f"{SITE}/#founder",
        "name": t["author"],
        "jobTitle": t["author_role"],
        "url": "https://www.linkedin.com/in/olehhebel/",
        "sameAs": ["https://www.linkedin.com/in/olehhebel/"],
    }


def course_id(lang):
    return f"{SITE}/#course" if lang == "en" else f"{SITE}/uk#course"


def build_post(p, posts):
    lang, t = p["lang"], LANG[p["lang"]]
    page_path = p["path"]
    alternates = [(lang, p["url"])]
    if p["alt"]:
        alternates.append((p["alt"]["lang"], p["alt"]["url"]))
    en_url = p["url"] if lang == "en" else (p["alt"]["url"] if p["alt"] else SITE + "/blog/")
    alternates.append(("x-default", en_url))
    alternates.sort(key=lambda a: {"en": 0, "uk": 1, "x-default": 2}[a[0]])

    faq = p.get("faq", [])
    graph = [
        {
            "@type": "BlogPosting",
            "@id": p["url"] + "#article",
            "headline": p["title"],
            "description": p["description"],
            "datePublished": p["published"],
            "dateModified": p.get("updated", p["published"]),
            "inLanguage": lang,
            "wordCount": p["words"],
            "keywords": p.get("keywords", []),
            "articleSection": p.get("section", t["blog"]),
            "mainEntityOfPage": {"@type": "WebPage", "@id": p["url"]},
            "author": person(lang),
            "publisher": {"@id": ORG_ID},
            "isPartOf": {"@id": WEBSITE_ID},
            "about": {"@id": course_id(lang)},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE + t["home_path"]},
                {"@type": "ListItem", "position": 2, "name": t["blog"], "item": SITE + t["blog_path"]},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": p["url"]},
            ],
        },
    ]
    if faq:
        graph.append({
            "@type": "FAQPage",
            "@id": p["url"] + "#faq",
            "inLanguage": lang,
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq
            ],
        })
    schema = {"@context": "https://schema.org", "@graph": graph}

    extra = (
        f'  <meta property="article:published_time" content="{p["published"]}">\n'
        f'  <meta property="article:modified_time" content="{p.get("updated", p["published"])}">\n'
        f'  <meta property="article:author" content="https://www.linkedin.com/in/olehhebel/">\n'
    )
    out = [head(lang, p["seo_title"], p["description"], p["url"], alternates, "article", schema, page_path, extra)]

    en_href = rel(page_path, p["alt"]["path"] if lang == "uk" and p["alt"] else ("/blog/" if lang == "uk" else page_path))
    uk_href = rel(page_path, p["alt"]["path"] if lang == "en" and p["alt"] else ("/blog/uk/" if lang == "en" else page_path))
    out.append(header(lang, page_path, en_href, uk_href))

    home = rel(page_path, t["home_path"])
    blog = rel(page_path, t["blog_path"])
    toc = "".join(
        f'<li><a href="#{anchor}">{label}</a></li>'
        for anchor, label in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', p["body"])
    )
    body = p["body"].replace("<!--cta-->", cta(lang, page_path))
    faq_html = ""
    if faq:
        items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faq)
        faq_html = f'<section class="post-faq" id="faq"><h2>{t["faq"]}</h2>{items}</section>'
    related = [r for r in posts if r["lang"] == lang and r["slug"] != p["slug"]][:3]
    related_html = "".join(
        f'<a href="{rel(page_path, r["path"])}"><span>{esc(r.get("section", t["blog"])).upper()}</span><h3>{esc(r["title"])}</h3><i>{t["read"]} →</i></a>'
        for r in related
    )
    updated = ""
    if p.get("updated") and p["updated"] != p["published"]:
        updated = f' · {t["updated"]} <time datetime="{p["updated"]}">{fmt_date(p["updated"], lang)}</time>'

    out.append(f"""
  <main id="main">
    <article class="post">
      <header class="post-head">
        <nav class="crumbs" aria-label="{esc(t['crumbs_label'])}"><a href="{home}">{t['home']}</a> / <a href="{blog}">{t['blog']}</a></nav>
        <p class="eyebrow">{esc(p.get('section', t['blog'])).upper()}</p>
        <h1>{esc(p['title'])}</h1>
        <p class="post-lead">{p['lead']}</p>
        <p class="post-meta">{t['by']} <a href="https://www.linkedin.com/in/olehhebel/" target="_blank" rel="noopener author">{t['author']}</a> · {t['published']} <time datetime="{p['published']}">{fmt_date(p['published'], lang)}</time>{updated} · {p['minutes']} {t['min_read']}</p>
      </header>
      <div class="post-layout">
        <nav class="post-toc" aria-label="{esc(p.get('toc_label', 'Contents' if lang == 'en' else 'Зміст'))}"><p>{'Contents' if lang == 'en' else 'Зміст'}</p><ol>{toc}</ol></nav>
        <div class="post-body">
{body}
          {faq_html}
        </div>
      </div>
      {cta(lang, page_path)}
    </article>
    <section class="section related" aria-labelledby="related-title">
      <p class="eyebrow" id="related-title">{t['related']}</p>
      <div class="proof-grid post-cards">{related_html}</div>
    </section>
  </main>

""")
    out.append(footer(lang, page_path))
    return "".join(out)


def build_index(lang, posts):
    t = LANG[lang]
    page_path = t["blog_path"]
    url = SITE + page_path
    own = [p for p in posts if p["lang"] == lang]
    alternates = [("en", SITE + "/blog/"), ("uk", SITE + "/blog/uk/"), ("x-default", SITE + "/blog/")]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "@id": url + "#blog",
                "url": url,
                "name": "Ship Index Grow — " + t["blog"],
                "description": t["blog_description"],
                "inLanguage": lang,
                "publisher": {"@id": ORG_ID},
                "isPartOf": {"@id": WEBSITE_ID},
                "blogPost": [
                    {"@type": "BlogPosting", "headline": p["title"], "url": p["url"], "datePublished": p["published"]}
                    for p in own
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": t["home"], "item": SITE + t["home_path"]},
                    {"@type": "ListItem", "position": 2, "name": t["blog"], "item": url},
                ],
            },
        ],
    }
    out = [head(lang, t["blog_title"], t["blog_description"], url, alternates, "website", schema, page_path)]
    out.append(header(lang, page_path, rel(page_path, "/blog/"), rel(page_path, "/blog/uk/")))
    cards = "".join(
        f'<a href="{rel(page_path, p["path"])}"><span>{esc(p.get("section", t["blog"])).upper()} · {p["minutes"]} {t["min_read"].upper()}</span><h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p><i>{t["read"]} →</i></a>'
        for p in own
    )
    out.append(f"""
  <main id="main">
    <section class="hero blog-hero" id="top">
      <p class="eyebrow">{t['blog_eyebrow']}</p>
      <h1>{t['blog_h1']}</h1>
      <p class="hero-copy">{t['blog_lead']}</p>
      <p><a class="text-link" href="feed.xml">{t['rss']} ↗</a></p>
    </section>
    <section class="section blog-list" aria-label="{esc(t['blog'])}">
      <div class="proof-grid post-cards">{cards}</div>
    </section>
    <div class="section">{cta(lang, page_path)}</div>
  </main>

""")
    out.append(footer(lang, page_path))
    return "".join(out)


def build_feed(lang, posts):
    t = LANG[lang]
    own = [p for p in posts if p["lang"] == lang]
    items = "".join(
        f"""
    <item>
      <title>{esc(p['title'])}</title>
      <link>{p['url']}</link>
      <guid isPermaLink="true">{p['url']}</guid>
      <pubDate>{date.fromisoformat(p['published']).strftime('%a, %d %b %Y')} 09:00:00 +0000</pubDate>
      <description>{esc(p['description'])}</description>
    </item>"""
        for p in own
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Ship Index Grow — {esc(t['blog'])}</title>
    <link>{SITE}{t['blog_path']}</link>
    <atom:link href="{SITE}{t['blog_path']}feed.xml" rel="self" type="application/rss+xml"/>
    <description>{esc(t['blog_description'])}</description>
    <language>{lang}</language>{items}
  </channel>
</rss>
"""


def build_sitemap(posts, home_lastmod):
    newest = max(p.get("updated", p["published"]) for p in posts)

    def entry(loc, lastmod, alts):
        links = "".join(
            f'\n    <xhtml:link rel="alternate" hreflang="{code}" href="{href}"/>' for code, href in alts
        )
        return f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>{links}\n  </url>\n"

    home_alts = [("en", SITE + "/"), ("uk", SITE + "/uk"), ("x-default", SITE + "/")]
    blog_alts = [("en", SITE + "/blog/"), ("uk", SITE + "/blog/uk/"), ("x-default", SITE + "/blog/")]
    parts = [
        entry(SITE + "/", home_lastmod, home_alts),
        entry(SITE + "/uk", home_lastmod, home_alts),
        entry(SITE + "/blog/", newest, blog_alts),
        entry(SITE + "/blog/uk/", newest, blog_alts),
    ]
    for p in sorted(posts, key=lambda p: (p["lang"], p["slug"])):
        alts = [(p["lang"], p["url"])]
        if p["alt"]:
            alts.append((p["alt"]["lang"], p["alt"]["url"]))
            alts.sort()
            en = p["url"] if p["lang"] == "en" else p["alt"]["url"]
            alts.append(("x-default", en))
        parts.append(entry(p["url"], p.get("updated", p["published"]), alts))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(parts) + "</urlset>\n"
    )


HOME_BLOCK = {
    "en": ("FROM THE BLOG", "Guides for shipping<br>and getting found."),
    "uk": ("З БЛОГУ", "Гайди про запуск<br>і видимість у пошуку."),
}


def update_home(lang, posts):
    """Refresh the latest-posts block between the blog markers on the home page."""
    t = LANG[lang]
    path = ROOT / t["home_file"]
    source = path.read_text(encoding="utf-8")
    eyebrow, title = HOME_BLOCK[lang]
    cards = "".join(
        f'<a href="{p["path"].lstrip("/")}"><span>{esc(p.get("section", t["blog"])).upper()}</span><h3>{esc(p["title"])}</h3><i>{t["read"]} →</i></a>'
        for p in posts if p["lang"] == lang
    )
    block = (
        f'<!--blog:start--><section class="section home-blog" id="blog"><div class="section-head"><p class="eyebrow">{eyebrow}</p>'
        f'<h2>{title}</h2></div><div class="proof-grid post-cards">{cards}</div>'
        f'<p><a class="text-link" href="{t["blog_path"].lstrip("/")}">{t["blog"]} →</a></p></section><!--blog:end-->'
    )
    updated, count = re.subn(r"<!--blog:start-->.*?<!--blog:end-->", lambda m: block, source, flags=re.S)
    if count != 1:
        raise SystemExit(f"{path.name}: blog markers not found")
    path.write_text(updated, encoding="utf-8")


def main():
    posts = load_posts()
    for p in posts:
        target = ROOT / p["path"].strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(build_post(p, posts), encoding="utf-8")
    for lang in LANG:
        folder = ROOT / LANG[lang]["blog_path"].strip("/")
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text(build_index(lang, posts), encoding="utf-8")
        (folder / "feed.xml").write_text(build_feed(lang, posts), encoding="utf-8")
    for lang in LANG:
        update_home(lang, posts)
    home_lastmod = max(p["published"] for p in posts)
    (ROOT / "sitemap.xml").write_text(build_sitemap(posts, home_lastmod), encoding="utf-8")
    print(f"Built {len(posts)} posts")


if __name__ == "__main__":
    main()
