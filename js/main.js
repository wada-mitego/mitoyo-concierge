/* ==========================================================================
   三豊コンシェルジュセンター  main.js
   1. ユーティリティ
   2. データ描画（WORKS / NEWS / miteGo）
   3. WORKS カテゴリーフィルター
   4. ヘッダー・モバイルメニュー
   5. スクロールアニメーション
   ========================================================================== */
(function () {
  "use strict";

  var data = window.SITE_DATA || { works: [], news: [], mitego: [], workCategories: [] };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- 1. ユーティリティ ---------- */
  function esc(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  var ARROW = '<svg class="ico"><use href="#i-arrow"/></svg>';

  /* ---------- 2. データ描画 ---------- */
  function renderWorks(filter) {
    var grid = $("#worksGrid");
    if (!grid) return;
    var list = data.works.filter(function (w) { return !filter || filter === "all" || w.category === filter; });
    if (!filter || filter === "all") list = list.slice(0, 8);
    grid.innerHTML = list.map(function (w) {
      return '<li class="work-card"><a href="' + esc(w.url) + '">' +
        '<span class="work-img"><img src="' + esc(w.image) + '" alt="" width="800" height="600" loading="lazy">' +
        '<span class="work-tag en">' + esc(w.category) + '</span></span>' +
        '<span class="work-title">' + esc(w.title) + '</span>' +
        '<span class="work-client">' + esc(w.client) + '</span></a></li>';
    }).join("") || '<li class="empty">このカテゴリーの実績は準備中です。</li>';
  }

  function renderTabs() {
    var wrap = $("#workTabs");
    if (!wrap) return;
    var cats = ["all"].concat(data.workCategories);
    wrap.innerHTML = cats.map(function (c, i) {
      return '<button type="button" role="tab" class="tab en' + (i === 0 ? " is-active" : "") + '" data-cat="' + esc(c) + '" aria-selected="' + (i === 0) + '">' +
        (c === "all" ? "すべて" : esc(c)) + '</button>';
    }).join("");
    wrap.addEventListener("click", function (e) {
      var btn = e.target.closest(".tab");
      if (!btn) return;
      $$(".tab", wrap).forEach(function (t) {
        var on = t === btn;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", on);
      });
      renderWorks(btn.getAttribute("data-cat"));
    });
  }

  function renderNews() {
    var grid = $("#newsGrid");
    if (!grid) return;
    grid.innerHTML = data.news.slice(0, 6).map(function (n) {
      return '<li class="news-card"><a href="' + esc(n.url) + '">' +
        '<span class="news-img"><img src="' + esc(n.image) + '" alt="" width="800" height="560" loading="lazy"></span>' +
        '<span class="news-body"><span class="news-meta"><span class="news-cat">' + esc(n.category) + '</span>' +
        '<time class="en">' + esc(n.date) + '</time></span>' +
        '<span class="news-title">' + esc(n.title) + '</span></span></a></li>';
    }).join("");
  }

  function renderMitego() {
    var shelf = $("#mitegoShelf");
    if (!shelf || !data.mitego.length) return;
    var latest = data.mitego[0];
    var back = data.mitego.slice(1, 4);
    var html = '<a class="cover cover-latest" href="' + esc(latest.url) + '"><img src="' + esc(latest.image) + '" alt="miteGo ' + esc(latest.issue) + ' 表紙" width="600" height="800" loading="lazy"><span class="cover-label en">LATEST ' + esc(latest.issue) + '</span></a>';
    html += '<div class="backnumbers"><p class="back-head en">BACK NUMBER</p><ul>' + back.map(function (b) {
      return '<li><a class="cover" href="' + esc(b.url) + '"><img src="' + esc(b.image) + '" alt="miteGo ' + esc(b.issue) + ' 表紙" width="600" height="800" loading="lazy"><span class="en">' + esc(b.issue) + '</span></a></li>';
    }).join("") + '</ul></div>';
    shelf.innerHTML = html;
    var cta = $("#mitegoCta");
    if (cta) cta.setAttribute("href", latest.url);
  }

  /* ---------- 3. 初期描画 ---------- */
  renderTabs();
  renderWorks("all");
  renderNews();
  renderMitego();

  /* ---------- 4. ヘッダー・モバイルメニュー ---------- */
  var header = $(".site-header");
  var btn = $("#menuBtn");
  function setMenu(open) {
    document.body.classList.toggle("menu-open", open);
    btn.setAttribute("aria-expanded", open);
    btn.setAttribute("aria-label", open ? "メニューを閉じる" : "メニューを開く");
  }
  if (btn) {
    btn.addEventListener("click", function () { setMenu(!document.body.classList.contains("menu-open")); });
    $$("#gnav a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
  }
  function onScroll() { header.classList.toggle("is-scrolled", window.scrollY > 10); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* スマホ固定CTAは、CONTACTセクションが見えている間は隠す */
  var contact = $("#contact");
  if (contact && "IntersectionObserver" in window) {
    new IntersectionObserver(function (en) {
      document.body.classList.toggle("contact-visible", en[0].isIntersecting);
    }).observe(contact);
  }

  /* ---------- 5. スクロールアニメーション ---------- */
  var targets = $$(".reveal");
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    document.documentElement.classList.add("js-reveal");
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add("is-in"); });
  }
})();
