#!/usr/bin/env python3
"""works.json から index.html と works/*/index.html を生成します。

使い方（リポジトリのルートで）:
    python3 tools/build.py

作品を追加するときは works.json に1件足して、
  assets/thumbnails/<slug>.jpg  （表紙・3:4）
  works/<slug>/images/page-001.jpg, page-002.jpg ...
を置いてから、このスクリプトを実行してください。
ページ数は images フォルダ内の page-*.jpg の数から自動で数えます。
"""
import glob, hashlib, html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
e = html.escape

data = json.load(open("works.json", encoding="utf-8"))
site, works, long_works = data["site"], data["works"], data["long_works"]
BASE = site["url"].rstrip("/") + "/"


def ver(path):
    """キャッシュ対策：ファイル内容から短いハッシュを作る"""
    return hashlib.md5(open(path, "rb").read()).hexdigest()[:8]


FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Klee+One:wght@400;600&family=Yomogi&display=swap">"""


def head_common(prefix):
    return f"""{FONTS}
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">"""


def og(title, desc, url, img, typ, alt):
    return f'''<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{typ}">
<meta property="og:site_name" content="{e(site["name"])}">
<meta property="og:locale" content="ja_JP">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(alt)}">
<meta name="twitter:card" content="summary_large_image">'''


# --- ページ数を数える -------------------------------------------------
for w in works:
    n = len(glob.glob(f"works/{w['slug']}/images/page-*.jpg"))
    if n == 0:
        sys.exit(f"エラー: works/{w['slug']}/images/ に page-001.jpg などがありません")
    w["pages"] = n
    w["description"] = w["description"].replace("{pages}", str(n))

V_VIEWER_CSS = ver("css/viewer.css")
V_VIEWER_JS = ver("js/viewer.js")
V_STYLE_CSS = ver("css/style.css")


# --- 作品ページ -------------------------------------------------------
def work_page(i, w):
    nxt = works[(i + 1) % len(works)]
    title = w["title"]
    url = f"{BASE}works/{w['slug']}/"
    pages = "\n".join(
        '<div class="manga-page"><img{lazy} src="images/page-{n:03d}.jpg" alt="{t} ページ {n}"></div>'.format(
            lazy="" if n <= 2 else ' loading="lazy"', n=n, t=e(title))
        for n in range(1, w["pages"] + 1))
    next_link = ""
    if len(works) > 1:
        next_link = f'\n  <a class="primary" href="../{nxt["slug"]}/">次の作品：{e(nxt["title"])}</a>'
    long_links = "".join(f'<a href="{e(l["url"])}">{e(l["title"])}</a>' for l in long_works)
    long_block = f'\n <p class="end-long">長期作品：{long_links}</p>' if long_works else ""
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=5,user-scalable=yes">
<title>{e(title)} | {e(site["name"])}</title>
{og(f"{title} | {site['name']}", w["description"], url, f"{BASE}assets/ogp/{w['slug']}.jpg", "article", f"{title} の表紙")}
{head_common("../../")}
<link rel="stylesheet" href="../../css/viewer.css?v={V_VIEWER_CSS}">
</head>
<body>
<header class="reader-bar">
 <div class="reader-bar-inner">
  <div class="reader-title"><a id="context-back" href="../../">← {e(site["name"])}へ戻る</a><strong>{e(title)}</strong></div>
  <div class="reader-controls"><span id="counter" aria-live="polite"></span><button id="top" type="button">先頭へ</button></div>
 </div>
 <div class="progress" aria-hidden="true"><div id="progress-fill"></div></div>
</header>
<main class="viewer">
{pages}
</main>
<template id="end-template">
<div class="end-card">
 <p class="end-mark">おわり</p>
 <h2><span>{e(title)}</span></h2>
 <p>最後まで読んでいただき、<br>ありがとうございました。</p>
 <div class="end-actions">{next_link}
  <button id="restart" type="button">もう一度読む</button>
  <a href="../../">{e(site["name"])}へ戻る</a>
 </div>{long_block}
</div>
</template>
<script src="../../js/viewer.js?v={V_VIEWER_JS}"></script>
</body>
</html>
'''


# --- トップページ -----------------------------------------------------
PENCIL = """<svg class="doodle-pencil" viewBox="0 0 150 50" aria-hidden="true" fill="none" stroke="#2b2823" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"><g transform="rotate(-12 75 25)"><rect x="8" y="17" width="96" height="17" fill="#f4d86e"/><path d="M104 17 L132 25.5 L104 34 Z" fill="#fffdf6"/><path d="M123 22.7 L132 25.5 L123 28.3 Z" fill="#2b2823"/><line x1="24" y1="17" x2="24" y2="34"/><line x1="30" y1="17" x2="30" y2="34"/></g></svg>"""


def top_page():
    cards = []
    for w in works:
        metas = "".join(f'<p class="meta">{e(m)}</p>' for m in w.get("meta", []))
        blurb = f'<p class="blurb">{e(w["blurb"])}</p>' if w.get("blurb") else ""
        cards.append(f'''<a class="work-card" href="works/{w["slug"]}/" aria-label="{e(w["title"])} を読む">
<span class="tape" aria-hidden="true"></span>
<div class="cover"><img src="assets/thumbnails/{w["slug"]}.jpg" alt="{e(w["title"])} のサムネイル"></div>
<div class="work-info"><h3>{e(w["title"])}</h3><p class="chips"><span>全{w["pages"]}ページ</span></p>{metas}{blurb}<span class="read-button">読む →</span></div>
</a>''')
    long_html = ""
    if long_works:
        notes = "".join(
            f'<a class="note" href="{e(l["url"])}"><strong>{e(l["title"])}</strong>'
            + (f'<small>{e(l["description"])}</small>' if l.get("description") else "")
            + '<em>読みにいく →</em></a>' for l in long_works)
        long_html = f'''<section class="long-works" aria-labelledby="long-title"><h2 id="long-title"><span>SAKUの長期作品</span></h2><div class="long-links">{notes}</div></section>'''
    profile_html = ""
    pr = site.get("profile")
    if pr and (pr.get("text") or pr.get("links")):
        paras = "".join(f"<p>{e(t)}</p>" for t in pr.get("text", "").split("\n") if t.strip())
        links = "".join(f'<a href="{e(l["url"])}">{e(l["label"])}</a>' for l in pr.get("links", []))
        links = f'<div class="profile-links">{links}</div>' if links else ""
        profile_html = f'''<section class="profile" aria-labelledby="profile-title"><h2 id="profile-title"><span>{e(pr.get("title", "SAKUについて"))}</span></h2>{paras}{links}</section>'''
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(site["name"])}</title>
{og(site["name"], site["description"], BASE, f"{BASE}assets/ogp/default.jpg", "website", site["name"])}
{head_common("")}
<link rel="stylesheet" href="css/style.css?v={V_STYLE_CSS}">
</head>
<body>
<header class="site-header"><div class="wrap"><h1><span>{e(site["name"])}</span></h1><p>{e(site["header_text"])}</p>{PENCIL}</div></header>
<main class="wrap">
<section aria-labelledby="works-title"><h2 id="works-title"><span>作品</span></h2>
<div class="works-grid">
{chr(10).join(cards)}
</div></section>
{long_html}
{profile_html}
</main>
<footer><div class="wrap">{e(site["copyright"])}</div></footer>
</body>
</html>
'''


def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    print("生成:", path)


write("index.html", top_page())
for i, w in enumerate(works):
    write(f"works/{w['slug']}/index.html", work_page(i, w))
print("完了")
