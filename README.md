# SAKU作品集

SAKUの短編・読切・過去作品を公開するGitHub Pagesサイトです。

## フォルダ構成

| 場所 | 役割 |
|---|---|
| `works.json` | 作品の一覧と、サイト全体の設定（**ここを編集します**） |
| `tools/build.py` | `works.json` からトップと各作品ページを生成します |
| `tools/make_ogp.py` | SNS共有用の画像を `assets/ogp/` に生成します |
| `css/viewer.css`, `js/viewer.js` | マンガリーダー（全作品共通） |
| `css/style.css` | トップページのデザイン |
| `index.html`, `works/*/index.html` | **自動生成されるので直接編集しません** |

## 作品を追加する手順

1. 画像を置く
   - 表紙: `assets/thumbnails/<slug>.jpg`（3:4）
   - 本文: `works/<slug>/images/page-001.jpg`, `page-002.jpg` …（連番）
   - `<slug>` は半角英数字とハイフンの作品名（例: `new-story`）
2. `works.json` の `works` に1件追加する
   ```json
   {
     "slug": "new-story",
     "title": "作品タイトル",
     "description": "SAKUの短編マンガ「作品タイトル」（全{pages}ページ）。",
     "meta": ["ひとこと紹介", "2026年11月発行"],
     "ogp_lines": ["SAKUの短編マンガ", "全{pages}ページ"]
   }
   ```
   `{pages}` はページ数に自動で置き換わります。`meta` は空（`[]`）でも構いません。
3. ページを生成する
   ```
   python3 tools/make_ogp.py   # 共有用画像（Pillow が必要: pip install pillow）
   python3 tools/build.py      # HTML生成
   ```
4. 変更したファイルをGitHubにアップロードする

## 任意で足せる項目（`works.json`）

書いた項目だけ表示されます。空のままなら何も出ません。

```json
"works": [{ "...": "...", "blurb": "カードに出るあらすじ（1〜2行）" }],
"long_works": [{ "title": "...", "url": "...", "description": "付せんに出るひとこと説明" }],
"site": {
  "profile": {
    "title": "SAKUについて",
    "text": "自己紹介の文章。\n改行すると段落が分かれます。",
    "links": [{ "label": "X", "url": "https://..." }]
  }
}
```

## デザインについて

- トップはスケッチブック風です。色や質感は `css/style.css` 先頭の `:root`（`--paper`、`--ink`、`--hl` など）で変えられます。
- 見出しは Google Fonts の「Yomogi」、本文は「Klee One」です。読み込めない環境では、システムの日本語フォントで表示されます。
- ファビコンは `assets/favicon.svg` です。

## 公開URLを変えたとき

`works.json` の `site.url` を新しいURLにして、`python3 tools/build.py` をやり直してください。
