# 画像の差し替え方

`images/placeholder/` の仮画像（SVG）を、実写真（JPG/WebP推奨）に置き換えます。

## 方法
1. 写真を `images/` 配下に保存（例: `images/hero/cafe.jpg`）。
2. `index.html`（固定部分）または `js/data.js`（WORKS / NEWS / miteGo）の `src` / `image` パスを書き換える。
   同じファイル名・同じ縦横比で上書きしても差し替え可能（拡張子を変える場合はパスも変更）。
3. `object-fit: cover` でトリミングされるので、多少の縦横比違いは問題ありません。

## 画像スロットと推奨サイズ
| ファイル | 場所 | 推奨 |
|---|---|---|
| hero-landscape | ファーストビュー背景（三豊・観音寺の風景） | 1600×900 以上 |
| hero-shop-staff / hero-photographer / hero-mitego / hero-web / hero-interview / hero-mikan | ファーストビューのコラージュ | 横900〜1000px程度 |
| about-interview / about-photographer | ABOUT（打ち合わせ・取材風景） | 4:3 / 1:1 |
| service-*（6点） | OUR BUSINESS カード | 4:3 |
| why-sunset | WHY US 左の写真 | 縦長〜正方形 |
| starter-kit | LOCAL STARTER KIT 用（現在未使用・拡張用） | 4:3 |
| works-01〜08 | WORKS | 4:3 |
| news-01〜06 | PICK UP NEWS | 16:10 |
| mitego-latest / mitego-11 など | miteGo 表紙 | 3:4（縦長） |
| recruit / company | RECRUIT / COMPANY | 4:3 前後 |

仮画像を再生成したい場合: `python3 tools/make_placeholders.py`
