# 三豊コンシェルジュセンター 公式サイト（トップページ・デザインプレビュー版）

HTML / CSS / JavaScript のみの静的サイトです（フレームワーク・ビルド不要）。
`index.html` をブラウザで開くだけで確認できます。

```
index.html            トップページ（全セクション）
css/style.css         スタイル（冒頭に目次あり。色・余白は :root のトークンで一括調整）
js/main.js            メニュー / WORKSフィルター / スクロール演出 / データ描画
js/data.js            WORKS・NEWS・miteGo のデータ（ここを編集すると表示が増える）
images/               ロゴ・ファビコン
images/placeholder/   仮画像（SVG）。実写真に差し替える
tools/                仮画像の生成スクリプト（実写真が揃えば不要）
```

## 修正の目安
| 変えたいもの | 場所 |
|---|---|
| 色・フォント・余白 | `css/style.css` の `00. Design tokens` |
| 文字サイズ | 各セクションの `font-size`（スマホは `@media (max-width: 720px)` 内） |
| 制作実績・お知らせ・miteGo号 | `js/data.js` |
| 写真 | `images/README.md` 参照 |
| 問い合わせ先 | `index.html` の `TODO` コメント（メール・電話） |

## 公開前のTODO
- 問い合わせボタン（`mailto:info@example.com` / `tel:0000000000`）を実際の連絡先・フォームへ差し替え
- 仮画像を実写真へ差し替え、`alt` を内容に合わせて調整
- WORKS / NEWS をSEO用に静的HTML化するか検討（現状は `js/data.js` から描画）
- OGP画像・favicon・meta description の最終調整
- 各「詳しく見る」「一覧」リンクの遷移先ページ作成
