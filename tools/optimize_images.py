#!/usr/bin/env python3
"""作品の画像を WebP に変換して、容量を軽くします（見た目はほぼ変わりません）。

対象:
  works/<slug>/images/ の page-*.jpg / page-*.png
  assets/thumbnails/ の *.jpg / *.png

必要なもの: Python 3 と Pillow（pip install pillow）
使い方（リポジトリのルートで）:
    python3 tools/optimize_images.py                     # WebPを作る（元の画像は残す）
    python3 tools/optimize_images.py --delete-originals  # 変換できたら元の画像を消す

新しい作品の画像を置いたら、これを実行してから tools/build.py を実行してください。
OGP用の assets/ogp/*.jpg は、SNSの互換性のため JPG のままにしてあります（変換しません）。
"""
import glob, os, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
QUALITY = 85
delete = "--delete-originals" in sys.argv

targets = []
for ext in ("jpg", "jpeg", "png"):
    targets += glob.glob(f"works/*/images/page-*.{ext}")
    targets += glob.glob(f"assets/thumbnails/*.{ext}")

before = after = 0
for src in sorted(targets):
    dst = os.path.splitext(src)[0] + ".webp"
    im = Image.open(src)
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    before += os.path.getsize(src)
    after += os.path.getsize(dst)
    print(f"変換: {src} -> {os.path.basename(dst)}")
    if delete:
        os.remove(src)

if targets:
    print(f"\n{len(targets)}枚: {before/1e6:.2f}MB -> {after/1e6:.2f}MB（{after/before:.0%}）")
else:
    print("変換する画像はありませんでした。")
