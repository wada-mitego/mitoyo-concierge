/* ==========================================================================
   サイトデータ（ダミー）
   実績・お知らせ・miteGoを追加／編集するときは、このファイルだけ触ればOKです。
   画像は images/ 以下のパスを指定してください（例: images/works/cafe-site.jpg）
   ========================================================================== */
window.SITE_DATA = {

  /* ---- WORKS 制作事例 -------------------------------------------------
     category: WEB / miteGo / DESIGN / PHOTO / MOVIE / SNS のいずれか
     tags: 小さく表示されるラベル（任意）
     url : 詳細ページのURL（未作成なら "#works"）                       */
  workCategories: ["WEB", "miteGo", "DESIGN", "PHOTO", "MOVIE", "SNS"],
  works: [
    { category: "WEB",    title: "カフェのホームページ制作",      client: "【三豊市】海辺のカフェ",     image: "images/placeholder/works-01.svg", url: "#works" },
    { category: "SNS",    title: "Instagram運用サポート",        client: "【観音寺市】飲食店",         image: "images/placeholder/works-02.svg", url: "#works" },
    { category: "DESIGN", title: "チラシ・メニュー制作",          client: "【三豊市】美容サロン",       image: "images/placeholder/works-03.svg", url: "#works" },
    { category: "MOVIE",  title: "店舗紹介動画・ドローン撮影",    client: "【観音寺市】工房",           image: "images/placeholder/works-04.svg", url: "#works" },
    { category: "miteGo", title: "miteGo 特集企画・取材",         client: "【三豊・観音寺】地域特集",   image: "images/placeholder/works-05.svg", url: "#works" },
    { category: "WEB",    title: "サロンのホームページ制作",      client: "【三豊市】ヘアサロン",       image: "images/placeholder/works-06.svg", url: "#works" },
    { category: "PHOTO",  title: "メニュー・店内撮影",            client: "【観音寺市】レストラン",     image: "images/placeholder/works-07.svg", url: "#works" },
    { category: "SNS",    title: "LINE公式アカウント立ち上げ",    client: "【三豊市】ベーカリー",       image: "images/placeholder/works-08.svg", url: "#works" }
  ],

  /* ---- PICK UP NEWS（TOPには先頭から最大6件を表示） --------------------
     date: "YYYY.MM.DD"                                                    */
  news: [
    { category: "グルメ",   title: "三豊の新しいカフェがオープンしました！",   date: "2026.10.01", image: "images/placeholder/news-01.svg", url: "#news" },
    { category: "イベント", title: "瀬戸内を楽しむマルシェイベント開催",       date: "2026.09.28", image: "images/placeholder/news-02.svg", url: "#news" },
    { category: "ショップ", title: "地元食材を使った新メニューのご紹介",       date: "2026.09.20", image: "images/placeholder/news-03.svg", url: "#news" },
    { category: "地域",     title: "秋のみかん収穫がはじまります",             date: "2026.09.12", image: "images/placeholder/news-04.svg", url: "#news" },
    { category: "グルメ",   title: "観音寺の人気店が新ランチをスタート",       date: "2026.09.05", image: "images/placeholder/news-05.svg", url: "#news" },
    { category: "風景",     title: "父母ヶ浜の夕景を楽しむ季節です",           date: "2026.08.30", image: "images/placeholder/news-06.svg", url: "#news" }
  ],

  /* ---- miteGo ----------------------------------------------------------
     先頭が「最新号」。url にPDFやデジタルブックのURLを入れるとリンクになります。
     例: url: "https://example.com/mitego/vol12.pdf"                       */
  mitego: [
    { issue: "Vol.12", title: "最新号",  image: "images/placeholder/mitego-latest.svg", url: "#" },
    { issue: "Vol.11", title: "バックナンバー", image: "images/placeholder/mitego-11.svg", url: "#" },
    { issue: "Vol.10", title: "バックナンバー", image: "images/placeholder/mitego-10.svg", url: "#" },
    { issue: "Vol.09", title: "バックナンバー", image: "images/placeholder/mitego-09.svg", url: "#" }
  ]
};
