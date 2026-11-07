#!/usr/bin/env python3
"""works.json から SNS共有用の画像（1200x630）を assets/ogp/ に生成します。

必要なもの: Python 3 と Pillow（pip install pillow）、日本語フォント
使い方（リポジトリのルートで）:
    python3 tools/make_ogp.py
フォントが見つからないときは、環境変数 OGP_FONT にフォントファイルのパスを指定してください。
    例) OGP_FONT="C:/Windows/Fonts/meiryo.ttc" python3 tools/make_ogp.py
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CANDIDATES = [
    os.environ.get("OGP_FONT", ""),
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "C:/Windows/Fonts/YuGothB.ttc",
    "C:/Windows/Fonts/meiryob.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
]
FONT = next((p for p in CANDIDATES if p and os.path.exists(p)), None)
if not FONT:
    sys.exit("日本語フォントが見つかりません。環境変数 OGP_FONT でフォントファイルを指定してください。")


REGULAR = FONT.replace("Bold", "Regular").replace("W6", "W3")
if not os.path.exists(REGULAR):
    REGULAR = FONT


def thumb(slug):
    for ext in ("webp", "jpg"):
        p = f"assets/thumbnails/{slug}.{ext}"
        if os.path.exists(p):
            return p
    sys.exit(f"assets/thumbnails/{slug}.webp（または .jpg）がありません")


def font(size, bold=True):
    return ImageFont.truetype(FONT if bold else REGULAR, size, index=0)


PAPER, INK, SUB, LINE = (247, 243, 232), (41, 39, 34), (107, 101, 89), (216, 208, 191)
W, H = 1200, 630


def cover(canvas, path, h, x, y):
    im = Image.open(path).convert("RGB")
    w = int(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    sh = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((30, 36, 30 + w, 36 + h), fill=(70, 60, 40, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    canvas.paste(sh, (x - 30, y - 30), sh)
    bd = Image.new("RGB", (w + 4, h + 4), LINE)
    bd.paste(im, (2, 2))
    canvas.paste(bd, (x - 2, y - 2))
    return w


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=f) > maxw and cur:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    return lines + [cur]


def work_image(w, site_name, out):
    c = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 10), fill=INK)
    cover(c, thumb(w['slug']), 520, 90, 55)
    x, maxw = 540, W - 540 - 70
    d.text((x, 90), site_name, font=font(30, False), fill=SUB)
    size = 64
    title = w["title"]
    lines = title.split(" ") if " " in title else wrap(d, title, font(size), maxw)
    while len(lines) > 3 and size > 40:
        size -= 4
        lines = wrap(d, title, font(size), maxw)
    y = 165
    for l in lines:
        d.text((x, y), l, font=font(size), fill=INK)
        y += int(size * 1.3)
    y += 14
    d.line((x, y, x + 90, y), fill=INK, width=4)
    y += 30
    for l in w.get("ogp_lines", []):
        d.text((x, y), l.replace("{pages}", str(w["pages"])), font=font(32, False), fill=SUB)
        y += 48
    d.text((x, H - 80), "マンガを読む →", font=font(30), fill=INK)
    c.save(out, quality=88, optimize=True)


def default_image(works, site_name, out):
    c = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 10), fill=INK)
    x = 640
    for w in works[:2]:
        x += cover(c, thumb(w['slug']), 430, x, 100) + 40
    d.text((80, 200), site_name, font=font(76), fill=INK)
    d.line((84, 310, 174, 310), fill=INK, width=4)
    d.text((84, 336), "SAKUが描いてきた", font=font(32, False), fill=SUB)
    d.text((84, 384), "短編・読切・過去作品", font=font(32, False), fill=SUB)
    c.save(out, quality=88, optimize=True)


data = json.load(open("works.json", encoding="utf-8"))
os.makedirs("assets/ogp", exist_ok=True)
import glob
for w in data["works"]:
    w["pages"] = len(glob.glob(f"works/{w['slug']}/images/page-*.webp")) or len(glob.glob(f"works/{w['slug']}/images/page-*.jpg"))
    work_image(w, data["site"]["name"], f"assets/ogp/{w['slug']}.jpg")
    print("生成:", f"assets/ogp/{w['slug']}.jpg")
default_image(data["works"], data["site"]["name"], "assets/ogp/default.jpg")
print("生成: assets/ogp/default.jpg")
