# SAKU作品集

SAKUの短編・読切・過去作品を公開するGitHub Pagesサイトです。

## フォルダ構成

| 場所 | 役割 |
|---|---|
| `works.json` | 作品の一覧と、サイト全体の設定（**ここを編集します**） |
| `tools/build.py` | `works.json` からトップと各作品ページを生成します |
| `tools/optimize_images.py` | 画像をWebPに変換して軽くします |
| `tools/make_ogp.py` | SNS共有用の画像を `assets/ogp/` に生成します |
| `css/viewer.css`, `js/viewer.js` | マンガリーダー（全作品共通） |
| `css/style.css` | トップページのデザイン |
| `index.html`, `404.html`, `works/*/index.html` | **自動生成されるので直接編集しません** |

## 作品を追加する手順

1. 画像を置く
   - 表紙: `assets/thumbnails/<slug>.jpg`（3:4）
   - 本文: `works/<slug>/images/page-001.jpg`, `page-002.jpg` …（連番）
   - JPG／PNGのまま置いて大丈夫です。次の手順3で WebP に変換します。
   - `<slug>` は半角英数字とハイフンの作品名（例: `new-story`）
2. `works.json` の `works` に1件追加する
   ```json
   {
     "slug": "new-story",
     "title": "作品タイトル",
     "description": "SAKUの短編マンガ「作品タイトル」（全{pages}ページ）。",
     "meta": ["ひとこと紹介", "2026年11月発行"],
     "ogp_lines": ["SAKUの短編マンガ", "全{pages}ページ"],
     "alts": ["表紙。〜が描かれている", "男の子が〜している", "…ページ順に1つずつ"]
   }
   ```
   `{pages}` はページ数に自動で置き換わります。`meta` は空（`[]`）でも構いません。
   `alts` は各ページの絵の説明（読み上げソフトや、画像が出ないときに使われます）です。書かなくても動き、その場合は「作品名 ページ3」になります。
3. ページを生成する
   ```
   python3 tools/optimize_images.py --delete-originals   # 画像をWebPに変換（元のJPG/PNGは消えます）
   python3 tools/make_ogp.py                             # 共有用画像
   python3 tools/build.py                                # HTML生成
   ```
   （`optimize_images.py` と `make_ogp.py` は Pillow が必要です: `pip install pillow`）
   元の画像を残したいときは `--delete-originals` を付けずに実行してください。
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

## リーダーの機能

- **続きから読む**: 読みかけの位置を、読者の端末（ブラウザの `localStorage`）に保存します。次に開くと「◯ページ目まで読んでいます［続きから］［最初から］」と表示します。最後まで読むと保存は消えます。サーバーには何も送りません。
- **初回の操作ヒント**: 初めて開いたときだけ数秒表示します（スマホは「右へスワイプ」、PCは「左側クリック／←キー」）。
- **PCではクリックでもめくれます**: 画面の左30%で次のページ、右30%で前のページです。
- 変更は `js/viewer.js` と `css/viewer.css` です。

## デザインについて

- トップはスケッチブック風です。色や質感は `css/style.css` 先頭の `:root`（`--paper`、`--ink`、`--hl` など）で変えられます。
- 見出しは Google Fonts の「Yomogi」、本文は「Klee One」です。読み込めない環境では、システムの日本語フォントで表示されます。
- ファビコンは `assets/favicon.svg` です。

## 404ページ

`404.html` が、存在しないURLを開いたときに表示されます（GitHub Pages が自動で使います）。`tools/build.py` が生成します。

## 公開URLを変えたとき

`works.json` の `site.url` を新しいURLにして、`python3 tools/build.py` をやり直してください。
