#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for Home.Watch (standard library only).

Renders every page into the repository root so GitHub Pages can serve the
main branch directly. Run:  python3 scripts/build.py
"""
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from content.guides import GUIDES  # noqa: E402
from content.regions import REGIONS  # noqa: E402
from content.cities import CITIES  # noqa: E402
from content import pages as P  # noqa: E402

SITE = "https://home.watch"
NAME = "Home.Watch"
ADSENSE = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/'
           'adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>')
FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800"
         "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400&display=swap")
NOW = datetime.datetime.now(datetime.timezone.utc)
TODAY = NOW.date().isoformat()
VERSION = NOW.strftime("%Y%m%d%H")

SITEMAP = []   # (path, lastmod, priority)
SEARCH = []    # search index entries


def esc(s):
    return html.escape(str(s), quote=True)


def load(name, default):
    path = os.path.join(ROOT, "data", name)
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return default


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "section"


def fmt_date(iso):
    try:
        d = datetime.date.fromisoformat(str(iso)[:10])
        return d.strftime("%b %-d, %Y")
    except Exception:
        return str(iso)[:10]


# ---------------------------------------------------------------- markdown-lite
def inline(text, root):
    t = esc(text)

    def link(m):
        label, url = m.group(1), m.group(2).replace("{{root}}", root)
        ext = url.startswith("http")
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        return '<a href="%s"%s>%s</a>' % (url, attrs, label)

    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    return t


def md(body, root):
    """Return (html, toc) for the markdown subset used in content modules."""
    out, toc = [], []
    lines = body.strip("\n").split("\n")
    i = 0
    para = []

    def flush():
        if para:
            out.append("<p>%s</p>" % inline(" ".join(para), root))
            para.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            flush(); i += 1; continue
        if line.startswith("## ") or line.startswith("### "):
            flush()
            level = 2 if line.startswith("## ") else 3
            text = line[level + 1:].strip()
            hid = slugify(text)
            if level == 2:
                toc.append((hid, text))
            out.append('<h%d id="%s">%s</h%d>' % (level, hid, inline(text, root), level))
            i += 1; continue
        if line.startswith("- "):
            flush(); items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append("<li>%s</li>" % inline(lines[i][2:], root)); i += 1
            out.append("<ul>%s</ul>" % "".join(items)); continue
        if re.match(r"^\d+\. ", line):
            flush(); items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append("<li>%s</li>" % inline(re.sub(r"^\d+\. ", "", lines[i]), root)); i += 1
            out.append('<ol class="steps">%s</ol>' % "".join(items)); continue
        if line.startswith("!> "):
            flush()
            out.append('<aside class="note note-warn"><p>%s</p></aside>' % inline(line[3:], root))
            i += 1; continue
        if line.startswith("> "):
            flush()
            out.append('<aside class="note"><p>%s</p></aside>' % inline(line[2:], root))
            i += 1; continue
        if line.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            head, data = cells[0], [r for r in cells[1:] if not set("".join(r)) <= set("-: ")]
            th = "".join("<th scope=\"col\">%s</th>" % inline(c, root) for c in head)
            trs = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c, root) for c in r) for r in data)
            out.append('<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, trs))
            continue
        para.append(line.strip()); i += 1
    flush()
    return "\n".join(out), toc


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


# ---------------------------------------------------------------- layout
NAV = [
    ("tools/index.html", "Tools", "tools"),
    ("guides/index.html", "Guides", "guides"),
    ("regions/index.html", "Regions", "regions"),
    ("alerts.html", "Live alerts", "alerts"),
    ("videos.html", "Videos", "videos"),
    ("for-pros.html", "For pros", "pros"),
]

LOGO = ('<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true" focusable="false">'
        '<path d="M6 19 20 7l14 12v15a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2Z" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round"/>'
        '<rect x="15" y="20" width="10" height="9" rx="1.2" class="logo-window"/>'
        '<path d="M20 20v9M15 24.5h10" stroke="var(--night)" stroke-width="1.4"/></svg>')


def header(root, active):
    links = "".join(
        '<li><a href="%s%s"%s>%s</a></li>' % (root, href, ' aria-current="page"' if key == active else "", label)
        for href, label, key in NAV)
    return """
<div class="topbar"><a href="https://web.works/contact" target="_blank" rel="noopener">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership</a></div>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="{root}index.html" aria-label="Home.Watch home">{logo}<span class="brand-name">Home<span class="brand-dot">.</span>Watch</span></a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>{links}</ul>
    </nav>
    <div class="header-actions">
      <button class="icon-btn" type="button" data-open-search aria-label="Search the site"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="m16 16 4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch dark or light mode"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5Z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg></button>
      <a class="btn btn-window btn-sm header-cta" href="{root}find-a-pro.html">Get matched</a>
      <button class="icon-btn menu-btn" type="button" aria-controls="main-nav" aria-expanded="false" data-menu-toggle aria-label="Open menu"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    </div>
  </div>
</header>""".format(root=root, logo=LOGO, links=links)


def footer(root):
    col = lambda title, items: '<div class="foot-col"><h2>%s</h2><ul>%s</ul></div>' % (
        title, "".join('<li><a href="%s%s">%s</a></li>' % (root, h, t) for h, t in items))
    cols = "".join([
        col("Homeowners", [("find-a-pro.html", "Get matched with a pro"), ("tools/cost-estimator.html", "Cost estimator"),
                           ("tools/departure-checklist.html", "Departure checklist"), ("tools/weather-watch.html", "Weather watch"),
                           ("guides/index.html", "All guides"), ("regions/index.html", "Regions")]),
        col("Home watch pros", [("for-pros.html", "List your business"), ("tools/visit-report.html", "Visit report builder"),
                                ("guides/starting-a-home-watch-business.html", "Start a home watch business"),
                                ("advertise.html", "Advertise & sponsor")]),
        col("Community", [("support.html", "Support Home.Watch"), ("contests.html", "Contests & prizes"),
                          ("careers.html", "Careers & talent"), ("videos.html", "Video library"), ("alerts.html", "Live alerts")]),
        col("About", [("about.html", "About us"), ("contact.html", "Contact"), ("faq.html", "FAQ"),
                      ("editorial-policy.html", "Editorial policy"), ("privacy.html", "Privacy policy"), ("terms.html", "Terms of use"),
                      ("disclaimer.html", "Disclaimer"), ("cookies.html", "Cookie policy"), ("trademark.html", "Trademark & copyright"),
                      ("sitemap.html", "Sitemap")]),
    ])
    year = NOW.year
    return """
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <a class="brand" href="{root}index.html">{logo}<span class="brand-name">Home<span class="brand-dot">.</span>Watch</span></a>
        <p>Free tools, guides and live alerts for homes that sit empty — and a fast way to find a home watch professional you can trust.</p>
        <form class="inline-form" data-form="newsletter" data-subject="Home.Watch newsletter signup" novalidate>
          <label for="nl-email">Get the monthly away-home briefing</label>
          <div class="inline-row">
            <input id="nl-email" name="email" type="email" required autocomplete="email" placeholder="you@example.com">
            <button class="btn btn-window" type="submit">Subscribe</button>
          </div>
          <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <p class="form-status" role="status" aria-live="polite"></p>
        </form>
      </div>
      {cols}
    </div>
    <div class="foot-legal">
      <p><strong>Trademark & copyright notice.</strong> Home.Watch is an independent information and referral website. It is not affiliated with, endorsed by or sponsored by any franchise, home care company, security company, trade association, insurer or product brand, including any business whose name contains the words &ldquo;home watch&rdquo;. All third-party names, logos and trademarks belong to their owners and are used for identification only. Content &copy; {year} Home.Watch. All rights reserved. <a href="{root}trademark.html">Read the full notice</a>.</p>
      <p>Home.Watch provides general information only — not insurance, legal, financial or professional advice. Providers matched through this site are independent businesses. See our <a href="{root}disclaimer.html">disclaimer</a>.</p>
    </div>
  </div>
</footer>
<div class="search-dialog" id="search-dialog" role="dialog" aria-modal="true" aria-label="Search Home.Watch" hidden>
  <div class="search-panel">
    <div class="search-head"><label for="search-input" class="sr-only">Search</label><input id="search-input" type="search" placeholder="Search guides, tools and regions" autocomplete="off"><button class="icon-btn" type="button" data-close-search aria-label="Close search"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button></div>
    <ul class="search-results" id="search-results"></ul>
  </div>
</div>
<div class="cookie-banner" id="cookie-banner" hidden>
  <p>We use cookies for essential features and, with Google AdSense, to show ads. See our <a href="{root}cookies.html">cookie policy</a>.</p>
  <div class="cookie-actions"><button class="btn btn-ghost btn-sm" type="button" data-cookie="essential">Essential only</button><button class="btn btn-window btn-sm" type="button" data-cookie="all">Accept all</button></div>
</div>
<aside class="slidein" id="slidein" hidden aria-label="Departure reminder offer">
  <button class="icon-btn slidein-close" type="button" data-close-slidein aria-label="Close"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
  <p class="slidein-title">Leaving for the season?</p>
  <p>Get a free departure checklist and a reminder two weeks before you go.</p>
  <a class="btn btn-window btn-sm" href="{root}index.html#reminder">Set my reminder</a>
</aside>
<a class="to-top" href="#top" aria-label="Back to top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 14 6-6 6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
""".format(root=root, logo=LOGO, cols=cols, year=year)


def page(path, title, desc, body, active="", schema=None, scripts=(), og_type="website",
         priority="0.6", crumbs=None, search_text="", index=True, body_class="", base_script=""):
    depth = path.count("/")
    root = "../" * depth
    canonical = SITE + "/" + ("" if path == "index.html" else path)
    full_title = title if path == "index.html" else "%s | %s" % (title, NAME)
    ld = [
        {"@context": "https://schema.org", "@type": "Organization", "name": NAME, "url": SITE,
         "logo": SITE + "/assets/img/icon-512.png"},
    ]
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
        for n, (label, href) in enumerate(crumbs, start=2):
            items.append({"@type": "ListItem", "position": n, "name": label, "item": SITE + "/" + href})
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if schema:
        ld.extend(schema if isinstance(schema, list) else [schema])
    ld_html = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    crumb_html = ""
    if crumbs:
        parts = ['<a href="%sindex.html">Home</a>' % root]
        for label, href in crumbs[:-1]:
            parts.append('<a href="%s%s">%s</a>' % (root, href, esc(label)))
        parts.append('<span aria-current="page">%s</span>' % esc(crumbs[-1][0]))
        crumb_html = '<nav class="crumbs wrap" aria-label="Breadcrumb">%s</nav>' % '<span class="sep" aria-hidden="true">/</span>'.join(parts)
    script_tags = "".join('<script src="%sassets/js/%s?v=%s" defer></script>' % (root, s, VERSION) for s in scripts)
    robots = "index,follow,max-image-preview:large" if index else "noindex,follow"
    doc = """<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">{base_script}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#1B2440">
<meta property="og:site_name" content="Home.Watch">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/img/icon-180.png">
<link rel="manifest" href="{root}manifest.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Home.Watch guides" href="{root}feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="{root}assets/css/site.css?v={ver}">
<script>(function(){{try{{var t=localStorage.getItem('hw-theme');if(!t&&window.matchMedia('(prefers-color-scheme: dark)').matches)t='dark';if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
{adsense}
{ld}
</head>
<body id="top" class="{body_class}" data-root="{root}">
<a class="skip" href="#main">Skip to content</a>
{header}
{crumbs}
<main id="main">
{body}
</main>
{footer}
<script src="{root}assets/js/config.js?v={ver}" defer></script>
<script src="{root}assets/js/site.js?v={ver}" defer></script>
{scripts}
</body>
</html>
""".format(base_script=base_script, title=esc(full_title), desc=esc(desc), robots=robots, canonical=canonical, og_type=og_type,
           site=SITE, root=root, fonts=FONTS, ver=VERSION, adsense=ADSENSE, ld=ld_html,
           body_class=body_class, header=header(root, active), crumbs=crumb_html, body=body,
           footer=footer(root), scripts=script_tags)
    write(path, doc)
    if index:
        SITEMAP.append((path, TODAY, priority))
        SEARCH.append({"t": title, "u": path, "d": desc, "k": (search_text or strip_tags(body))[:600]})


# ---------------------------------------------------------------- shared renderers
def render_recalls(recalls, root, limit=6):
    if not recalls:
        return '<p class="empty">Recall data refreshes daily. Check back soon.</p>'
    items = []
    for r in recalls[:limit]:
        items.append('<li><a href="%s" target="_blank" rel="noopener">%s</a><span class="meta">%s%s</span></li>' % (
            esc(r.get("url", "#")), esc(r.get("title", "")), esc(fmt_date(r.get("date", ""))),
            (" — " + esc(r["hazard"])) if r.get("hazard") else ""))
    return '<ul class="feed-list">%s</ul>' % "".join(items)


def render_fema(fema, root, limit=6):
    if not fema:
        return '<p class="empty">Disaster declaration data refreshes daily.</p>'
    items = []
    for d in fema[:limit]:
        url = "https://www.fema.gov/disaster/%s" % esc(d.get("number", ""))
        items.append('<li><a href="%s" target="_blank" rel="noopener">%s</a><span class="meta">%s, %s — %s</span></li>' % (
            url, esc(d.get("title", "")), esc(d.get("state", "")), esc(fmt_date(d.get("date", ""))), esc(d.get("type", ""))))
    return '<ul class="feed-list">%s</ul>' % "".join(items)


def render_news(news, limit=8):
    if not news:
        return '<p class="empty">Headlines refresh daily.</p>'
    items = []
    for n in news[:limit]:
        items.append('<li><a href="%s" target="_blank" rel="noopener nofollow">%s</a><span class="meta">%s%s</span></li>' % (
            esc(n.get("url", "#")), esc(n.get("title", "")), esc(n.get("source", "")),
            (" — " + esc(fmt_date(n.get("date", "")))) if n.get("date") else ""))
    return '<ul class="feed-list">%s</ul>' % "".join(items)


def render_board(board, limit=None, role=None):
    rows = [c for c in board.get("cities", []) if not role or c.get("role") in role]
    if limit:
        rows = rows[:limit]
    if not rows:
        return '<p class="empty">The freeze and heat board refreshes every morning.</p>'
    trs = []
    for c in rows:
        flags = []
        if c.get("freeze_days"):
            flags.append('<span class="flag flag-freeze">Freeze %d day%s</span>' % (c["freeze_days"], "" if c["freeze_days"] == 1 else "s"))
        if c.get("hard_freeze"):
            flags.append('<span class="flag flag-issue">Hard freeze</span>')
        if c.get("heat_days"):
            flags.append('<span class="flag flag-heat">Heat %d day%s</span>' % (c["heat_days"], "" if c["heat_days"] == 1 else "s"))
        if not flags:
            flags.append('<span class="flag flag-clear">All clear</span>')
        trs.append("<tr><th scope=\"row\">%s <span class=\"muted\">%s</span></th><td>%s°F / %s°C</td><td>%s°F / %s°C</td><td>%s</td></tr>" % (
            esc(c["name"]), esc(c["region"]), c.get("min_f", "–"), c.get("min_c", "–"), c.get("max_f", "–"), c.get("max_c", "–"), " ".join(flags)))
    return ('<div class="table-wrap"><table class="board"><thead><tr><th scope="col">City</th><th scope="col">7-day low</th>'
            '<th scope="col">7-day high</th><th scope="col">Watch</th></tr></thead><tbody>%s</tbody></table></div>'
            % "".join(trs))


def lite_video(v, root):
    vid = esc(v["id"])
    return ('<figure class="video"><button class="lite-yt" type="button" data-yt="%s" aria-label="Play video: %s">'
            '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">'
            '<span class="play" aria-hidden="true"></span></button><figcaption>%s<span class="muted">%s</span></figcaption></figure>') % (
        vid, esc(v.get("title", "")), vid, esc(v.get("title", "")), esc(v.get("author", "")))


CTX = {}


def build():
    data = {
        "recalls": load("recalls.json", {}).get("items", []),
        "fema": load("fema.json", {}).get("items", []),
        "news": load("news.json", {}).get("items", []),
        "board": load("citywatch.json", {}),
        "videos": load("videos.json", {}).get("items", []),
        "season": load("season.json", {}),
    }
    CTX.update(data)
    R = dict(esc=esc, md=md, page=page, render_recalls=render_recalls, render_fema=render_fema,
             render_news=render_news, render_board=render_board, lite_video=lite_video, fmt_date=fmt_date,
             GUIDES=GUIDES, REGIONS=REGIONS, CITIES=CITIES, data=data, TODAY=TODAY, SITE=SITE, strip_tags=strip_tags)
    P.build_all(R)

    # cities for the weather tool
    write("data/cities.json", json.dumps([dict(zip(["name", "region", "country", "lat", "lon", "role"], c)) for c in CITIES],
                                         ensure_ascii=False, separators=(",", ":")))
    # search index
    write("search-index.json", json.dumps(SEARCH, ensure_ascii=False, separators=(",", ":")))
    # sitemap
    urls = "".join("<url><loc>%s/%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (
        SITE, "" if p == "index.html" else p, lm, pr) for p, lm, pr in SITEMAP)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)
    # RSS feed of guides
    items = "".join(
        "<item><title>%s</title><link>%s/guides/%s.html</link><guid>%s/guides/%s.html</guid><description>%s</description><pubDate>%s</pubDate></item>" % (
            esc(g["title"]), SITE, g["slug"], SITE, g["slug"], esc(g["desc"]),
            datetime.datetime.fromisoformat(g["updated"]).strftime("%a, %d %b %Y 08:00:00 GMT")) for g in GUIDES)
    write("feed.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Home.Watch guides</title><link>%s/</link>'
          '<description>Guides for homes that sit empty.</description><lastBuildDate>%s</lastBuildDate>%s</channel></rss>\n' % (
              SITE, NOW.strftime("%a, %d %b %Y %H:%M:%S GMT"), items))
    write("robots.txt", "User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
    write("ads.txt", "google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    write(".nojekyll", "")
    write("manifest.webmanifest", json.dumps({
        "name": "Home.Watch", "short_name": "Home.Watch", "start_url": "./index.html", "display": "standalone",
        "background_color": "#F4F6FA", "theme_color": "#1B2440", "description": "Tools, guides and live alerts for homes that sit empty.",
        "icons": [{"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
    print("Built %d pages, %d search entries." % (len(SITEMAP) + 1, len(SEARCH)))


if __name__ == "__main__":
    build()
