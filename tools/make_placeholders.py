#!/usr/bin/env python3
"""
仮画像（プレースホルダー）ジェネレーター
-----------------------------------------
実写真が揃うまでの間、デザイン確認用のイラスト風SVGを images/placeholder/ に書き出します。
実写真に差し替えるときは、このスクリプトは不要です（images/README.md を参照）。

  python3 tools/make_placeholders.py
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "..", "images", "placeholder")
_uid = [0]


def uid(prefix="g"):
    _uid[0] += 1
    return f"{prefix}{_uid[0]}"


def lin(id_, stops, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def wrap(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{body}</svg>')


def nest(scene, x, y, w, h, clip_r=0):
    """別シーンを入れ子にして配置する"""
    sw, sh, body = scene
    cid = uid("c")
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{clip_r}"/></clipPath>'
            f'<g clip-path="url(#{cid})"><svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {sw} {sh}" '
            f'preserveAspectRatio="xMidYMid slice">{body}</svg></g>')


# ------------------------------------------------------------------ 風景
def hills(rng, w, base, amp, n, color, opacity=1):
    step = w / n
    d = f"M0 {base + amp*2} L0 {base}"
    x = 0
    y = base
    for i in range(n):
        nx = x + step
        ny = base - rng.random() * amp
        d += f" Q{x + step/2:.0f} {min(y, ny) - amp*0.5:.0f} {nx:.0f} {ny:.0f}"
        x, y = nx, ny
    d += f" L{w} {base + amp*2} Z"
    return f'<path d="{d}" fill="{color}" opacity="{opacity}"/>'


def seascape(w=1200, h=800, seed=1, sky=("#9fd3f0", "#e8f6fb"), sea=("#4aa3cf", "#1f7bb0"),
             sun=None, island="#5b8f6b", horizon=0.52, town=True, boats=2, clouds=3, season="day"):
    rng = random.Random(seed)
    a, b, c = uid("sky"), uid("sea"), uid("sun")
    defs = lin(a, [(0, sky[0]), (1, sky[1])]) + lin(b, [(0, sea[0]), (1, sea[1])])
    defs += f'<radialGradient id="{c}"><stop offset="0" stop-color="#fff6c8" stop-opacity="1"/><stop offset="1" stop-color="#fff6c8" stop-opacity="0"/></radialGradient>'
    hy = h * horizon
    o = f"<defs>{defs}</defs>"
    o += f'<rect width="{w}" height="{h}" fill="url(#{a})"/>'
    if sun:
        sx, sy, sc = sun
        o += f'<circle cx="{sx*w}" cy="{sy*h}" r="{h*0.32}" fill="url(#{c})"/>'
        o += f'<circle cx="{sx*w}" cy="{sy*h}" r="{h*0.07}" fill="{sc}"/>'
    for i in range(clouds):
        cx, cy = rng.random() * w, rng.random() * hy * 0.55 + 30
        for k in range(4):
            o += f'<ellipse cx="{cx + k*38:.0f}" cy="{cy + (k%2)*8:.0f}" rx="{58 - k*7}" ry="{20 + k*2}" fill="#fff" opacity=".7"/>'
    o += hills(rng, w, hy - 8, 40, 5, "#8fb8a4", .55)
    o += hills(rng, w * 0.62, hy - 2, 55, 3, island)
    o += f'<rect y="{hy}" width="{w}" height="{h-hy}" fill="url(#{b})"/>'
    # 島
    o += f'<path d="M{w*0.55} {hy} Q{w*0.66} {hy-70} {w*0.8} {hy} Z" fill="#6aa089"/>'
    o += f'<path d="M{w*0.74} {hy} Q{w*0.82} {hy-38} {w*0.95} {hy} Z" fill="#7bb09a"/>'
    # 海のきらめき
    for i in range(46):
        x, y = rng.random() * w, hy + 10 + rng.random() * (h - hy - 20)
        l = 10 + rng.random() * 36
        o += f'<rect x="{x:.0f}" y="{y:.0f}" width="{l:.0f}" height="3" rx="1.5" fill="#fff" opacity="{.18 + rng.random()*.35:.2f}"/>'
    for i in range(boats):
        bx, by = w * (0.3 + rng.random() * 0.5), hy + 40 + rng.random() * (h - hy) * 0.4
        o += f'<path d="M{bx:.0f} {by:.0f} h46 l-8 12 h-30 z" fill="#fff"/><path d="M{bx+22:.0f} {by-26:.0f} v26 h18 z" fill="#fff" opacity=".9"/>'
    if town:
        o += f'<path d="M0 {h*0.78} Q{w*0.25} {h*0.62} {w*0.5} {h*0.78} L{w*0.5} {h} L0 {h} Z" fill="#4f7d5b"/>'
        roofs = ["#d9703f", "#5d7893", "#c9553a", "#8a6f5a", "#6c8a9a"]
        for row in range(4):
            for i in range(11):
                x = 14 + i * 46 + (row % 2) * 22 + rng.random() * 8
                y = h * 0.74 + row * 34 + i * (-3.5 if row < 2 else 1.5) + rng.random() * 6
                if x > w * 0.5 - row * 20:
                    continue
                ww, hh = 34 + rng.random() * 8, 20
                o += f'<rect x="{x:.0f}" y="{y:.0f}" width="{ww:.0f}" height="{hh}" fill="#f6efe2"/>'
                o += f'<polygon points="{x-4:.0f},{y:.0f} {x+ww/2:.0f},{y-14:.0f} {x+ww+4:.0f},{y:.0f}" fill="{rng.choice(roofs)}"/>'
    return w, h, o


# ------------------------------------------------------------------ 人物
def person(cx, by, s=1.0, skin="#f2c9a5", hair="#3b2a22", shirt="#e8eef2", cap=None, apron=None,
           long=False, glasses=False):
    g = f'<g transform="translate({cx} {by}) scale({s})">'
    if long:
        g += f'<path d="M-62 -205 C-70 -290 70 -290 62 -205 L70 -120 L-70 -120 Z" fill="{hair}"/>'
    g += f'<path d="M-135 0 C-135 -95 -95 -128 -35 -138 L35 -138 C95 -128 135 -95 135 0 Z" fill="{shirt}"/>'
    if apron:
        g += f'<path d="M-72 0 L-58 -128 L58 -128 L72 0 Z" fill="{apron}"/>'
        g += f'<path d="M-58 -128 L-30 -150 M58 -128 L30 -150" stroke="{apron}" stroke-width="10" stroke-linecap="round"/>'
    g += f'<rect x="-22" y="-168" width="44" height="42" rx="14" fill="{skin}" opacity=".95"/>'
    g += f'<ellipse cx="0" cy="-208" rx="52" ry="60" fill="{skin}"/>'
    if not cap:
        g += f'<path d="M-56 -208 C-62 -280 62 -280 56 -208 C48 -240 -20 -250 -56 -208 Z" fill="{hair}"/>'
    else:
        g += f'<path d="M-58 -222 C-60 -286 60 -286 58 -222 Z" fill="{cap}"/>'
        g += f'<path d="M-58 -222 H92 C90 -212 40 -208 -58 -218 Z" fill="{cap}"/>'
    g += '<circle cx="-19" cy="-202" r="4.5" fill="#2b211c"/><circle cx="19" cy="-202" r="4.5" fill="#2b211c"/>'
    g += '<circle cx="-34" cy="-188" r="9" fill="#f29b8b" opacity=".45"/><circle cx="34" cy="-188" r="9" fill="#f29b8b" opacity=".45"/>'
    g += '<path d="M-14 -182 Q0 -167 14 -182" fill="none" stroke="#9b4a3a" stroke-width="3.5" stroke-linecap="round"/>'
    if glasses:
        g += '<circle cx="-19" cy="-202" r="14" fill="none" stroke="#333" stroke-width="3"/><circle cx="19" cy="-202" r="14" fill="none" stroke="#333" stroke-width="3"/><path d="M-5 -202 h10" stroke="#333" stroke-width="3"/>'
    return g + "</g>"


def camera(cx, cy, s=1.0):
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            '<rect x="-92" y="-48" width="184" height="104" rx="14" fill="#2c2f36"/>'
            '<rect x="-60" y="-66" width="52" height="24" rx="6" fill="#2c2f36"/>'
            '<circle cx="0" cy="6" r="42" fill="#1a1c21"/><circle cx="0" cy="6" r="30" fill="#39465a"/>'
            '<circle cx="-9" cy="-4" r="9" fill="#9fb7d6" opacity=".7"/>'
            '<rect x="56" y="-36" width="22" height="12" rx="3" fill="#e9eaee"/></g>')


# ------------------------------------------------------------------ 料理
def food(w=900, h=700, seed=1, kind="pasta"):
    rng = random.Random(seed)
    wood = uid("w")
    o = f'<defs>{lin(wood, [(0, "#b98a5d"), (1, "#97683f")], 1, 1)}</defs><rect width="{w}" height="{h}" fill="url(#{wood})"/>'
    for i in range(14):
        y = i * h / 13
        o += f'<rect y="{y:.0f}" width="{w}" height="2" fill="#7d5532" opacity=".25"/>'
    cx, cy = w * 0.5, h * 0.5
    o += f'<circle cx="{cx+10}" cy="{cy+14}" r="{h*0.42}" fill="#000" opacity=".16"/>'
    o += f'<circle cx="{cx}" cy="{cy}" r="{h*0.42}" fill="#fbfaf6"/><circle cx="{cx}" cy="{cy}" r="{h*0.33}" fill="#f1ede4"/>'
    if kind == "pasta":
        for r in range(8):
            o += f'<circle cx="{cx}" cy="{cy}" r="{h*0.27 - r*14}" fill="none" stroke="#f1c75b" stroke-width="12" stroke-dasharray="{60+r*8} 14" stroke-linecap="round" transform="rotate({r*40} {cx} {cy})"/>'
        for i in range(12):
            a = rng.random() * 6.28
            rr = rng.random() * h * 0.2
            o += f'<circle cx="{cx+math.cos(a)*rr:.0f}" cy="{cy+math.sin(a)*rr:.0f}" r="{10+rng.random()*10:.0f}" fill="{rng.choice(["#d8473a","#e8643f","#f5b8a0"])}"/>'
    elif kind == "cake":
        o += f'<path d="M{cx-120} {cy+60} L{cx-90} {cy-80} L{cx+120} {cy-30} L{cx+110} {cy+70} Z" fill="#f7e2c6"/>'
        o += f'<path d="M{cx-90} {cy-80} L{cx+120} {cy-30} L{cx+118} {cy-5} L{cx-95} {cy-52} Z" fill="#fff"/>'
        for i in range(7):
            o += f'<circle cx="{cx-70+i*28}" cy="{cy-62+i*7}" r="16" fill="#d8344e"/>'
    else:  # bowl / salad
        for i in range(40):
            a = rng.random() * 6.28
            rr = rng.random() * h * 0.28
            o += f'<ellipse cx="{cx+math.cos(a)*rr:.0f}" cy="{cy+math.sin(a)*rr:.0f}" rx="{18+rng.random()*14:.0f}" ry="{9+rng.random()*7:.0f}" fill="{rng.choice(["#4f9a4f","#7cc06b","#e9742f","#f4d35e","#c9473a"])}" transform="rotate({rng.random()*180:.0f} {cx} {cy})"/>'
    for i in range(5):
        a = rng.random() * 6.28
        rr = h * 0.18 + rng.random() * h * 0.08
        o += f'<ellipse cx="{cx+math.cos(a)*rr:.0f}" cy="{cy+math.sin(a)*rr:.0f}" rx="22" ry="11" fill="#3f8f45" transform="rotate({a*57:.0f} {cx+math.cos(a)*rr:.0f} {cy+math.sin(a)*rr:.0f})"/>'
    # 小皿とグラス
    o += f'<circle cx="{w*0.88}" cy="{h*0.2}" r="{h*0.12}" fill="#f5f2ea"/><circle cx="{w*0.88}" cy="{h*0.2}" r="{h*0.08}" fill="#d5483b" opacity=".85"/>'
    o += f'<circle cx="{w*0.1}" cy="{h*0.82}" r="{h*0.1}" fill="#fff" opacity=".55"/><circle cx="{w*0.1}" cy="{h*0.82}" r="{h*0.07}" fill="#b9dff0" opacity=".7"/>'
    return w, h, o


# ------------------------------------------------------------------ 店内
def cafe(w=1000, h=800, seed=1, wall=("#f1d9b6", "#e4c08f"), staff=True, cap="#9c6b3f"):
    rng = random.Random(seed)
    a, b = uid("wl"), uid("ct")
    o = f'<defs>{lin(a, list(zip((0, 1), wall)))}{lin(b, [(0, "#a97646"), (1, "#7c5230")])}</defs>'
    o += f'<rect width="{w}" height="{h}" fill="url(#{a})"/>'
    # 窓
    o += f'<rect x="{w*0.58}" y="{h*0.08}" width="{w*0.36}" height="{h*0.46}" rx="10" fill="#fff" opacity=".95"/>'
    o += nest(seascape(600, 400, seed + 4, boats=1, clouds=2, town=False), w * 0.59, h * 0.1, w * 0.34, h * 0.42, 6)
    o += f'<rect x="{w*0.755}" y="{h*0.08}" width="6" height="{h*0.46}" fill="#fff"/>'
    # 棚
    for i, y in enumerate((0.22, 0.4)):
        o += f'<rect x="{w*0.04}" y="{h*y}" width="{w*0.42}" height="10" fill="#8a5d36"/>'
        for k in range(7):
            col = rng.choice(["#e07a4f", "#6fa8a0", "#f4d06f", "#8f6bb0", "#fff"])
            hh = 40 + rng.random() * 30
            o += f'<rect x="{w*0.06 + k*w*0.055}" y="{h*y - hh}" width="{w*0.04}" height="{hh}" rx="6" fill="{col}"/>'
    # ペンダントライト
    for x in (0.2, 0.5):
        o += f'<rect x="{w*x}" y="0" width="3" height="{h*0.12}" fill="#444"/><path d="M{w*x-34} {h*0.17} Q{w*x} {h*0.07} {w*x+34} {h*0.17} Z" fill="#f0a64d"/><circle cx="{w*x+1}" cy="{h*0.18}" r="9" fill="#fff3b0"/>'
    # カウンター
    o += f'<rect y="{h*0.72}" width="{w}" height="{h*0.28}" fill="url(#{b})"/><rect y="{h*0.72}" width="{w}" height="12" fill="#c28f5d"/>'
    if staff:
        o += person(w * 0.36, h * 0.74, 1.55, apron="#3f5a4a", cap=cap, shirt="#f4f1ea")
        o += f'<ellipse cx="{w*0.52}" cy="{h*0.77}" rx="70" ry="16" fill="#fbfaf6"/><ellipse cx="{w*0.52}" cy="{h*0.765}" rx="46" ry="9" fill="#e7a45a"/>'
        o += f'<ellipse cx="{w*0.52}" cy="{h*0.755}" rx="26" ry="14" fill="#d8473a"/>'
    return w, h, o


def interview(w=1000, h=760, seed=2):
    a, t = uid("bg"), uid("tb")
    o = f'<defs>{lin(a, [(0, "#e9d9bf"), (1, "#d9c09b")])}{lin(t, [(0, "#b8854f"), (1, "#8c6035")])}</defs>'
    o += f'<rect width="{w}" height="{h}" fill="url(#{a})"/>'
    for i in range(9):
        o += f'<circle cx="{(i*131+60)%w}" cy="{70+(i*53)%160}" r="{26+(i%3)*10}" fill="#fff4cf" opacity=".5"/>'
    o += person(w * 0.28, h * 0.78, 1.45, long=True, hair="#4b3326", shirt="#8fb9a0", apron="#6c9a84")
    o += person(w * 0.74, h * 0.78, 1.45, hair="#2a2a30", shirt="#f1f1f1", glasses=True, skin="#eec19b")
    o += f'<rect y="{h*0.76}" width="{w}" height="{h*0.24}" fill="url(#{t})"/>'
    o += f'<rect x="{w*0.36}" y="{h*0.7}" width="{w*0.28}" height="{h*0.08}" rx="4" fill="#fff" transform="rotate(-3 {w*0.5} {h*0.74})"/>'
    o += f'<rect x="{w*0.4}" y="{h*0.72}" width="{w*0.18}" height="6" fill="#4a90b8" transform="rotate(-3 {w*0.5} {h*0.74})"/>'
    o += f'<ellipse cx="{w*0.13}" cy="{h*0.83}" rx="38" ry="10" fill="#fff"/><rect x="{w*0.115}" y="{h*0.78}" width="30" height="34" rx="6" fill="#fff"/>'
    return w, h, o


def photographer(w=900, h=800, seed=3):
    rng = random.Random(seed)
    a = uid("bg")
    o = f'<defs>{lin(a, [(0, "#d9b98f"), (1, "#b98b5a")])}</defs><rect width="{w}" height="{h}" fill="url(#{a})"/>'
    for i in range(14):
        o += f'<circle cx="{rng.random()*w:.0f}" cy="{rng.random()*h*0.6:.0f}" r="{20+rng.random()*44:.0f}" fill="{rng.choice(["#fff1c2","#ffd99a","#fff"])}" opacity=".35"/>'
    o += person(w * 0.52, h * 1.0, 2.0, hair="#241f1f", shirt="#2f4c63", cap=None)
    o += camera(w * 0.52, h * 0.5, 1.7)
    return w, h, o


# ------------------------------------------------------------------ デバイス
def mini_site(x, y, w, h, accent="#e8643f", seed=1, kind="cafe"):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fffdf8"/>'
    o += f'<rect x="{x}" y="{y}" width="{w}" height="{h*0.1}" fill="#fff"/><rect x="{x+w*0.04}" y="{y+h*0.03}" width="{w*0.18}" height="{h*0.04}" rx="3" fill="{accent}"/>'
    for i in range(4):
        o += f'<rect x="{x+w*0.55+i*w*0.11}" y="{y+h*0.04}" width="{w*0.08}" height="{h*0.025}" rx="2" fill="#bbb"/>'
    sc = seascape(500, 300, seed, boats=1, clouds=1, town=False)
    o += nest(sc, x, y + h * 0.1, w, h * 0.42)
    o += f'<rect x="{x+w*0.08}" y="{y+h*0.62}" width="{w*0.4}" height="{h*0.05}" rx="3" fill="#333"/>'
    o += f'<rect x="{x+w*0.08}" y="{y+h*0.72}" width="{w*0.55}" height="{h*0.03}" rx="2" fill="#bbb"/><rect x="{x+w*0.08}" y="{y+h*0.78}" width="{w*0.45}" height="{h*0.03}" rx="2" fill="#bbb"/>'
    o += f'<rect x="{x+w*0.08}" y="{y+h*0.86}" width="{w*0.24}" height="{h*0.07}" rx="{h*0.035}" fill="{accent}"/>'
    return o


def laptop_scene(w=1000, h=760, accent="#e8643f", seed=5, bg=("#e9f1f5", "#cfdde6")):
    a = uid("d")
    o = f'<defs>{lin(a, list(zip((0, 1), bg)))}</defs><rect width="{w}" height="{h}" fill="url(#{a})"/>'
    o += f'<rect y="{h*0.78}" width="{w}" height="{h*0.22}" fill="#c9a679"/>'
    lx, ly, lw, lh = w * 0.14, h * 0.1, w * 0.62, h * 0.52
    o += f'<rect x="{lx-12}" y="{ly-12}" width="{lw+24}" height="{lh+24}" rx="16" fill="#2b2f36"/>'
    o += mini_site(lx, ly, lw, lh, accent, seed)
    o += f'<path d="M{lx-50} {ly+lh+12} H{lx+lw+50} L{lx+lw+20} {ly+lh+38} H{lx-20} Z" fill="#aab3bd"/>'
    # スマホ
    px, py, pw, ph = w * 0.74, h * 0.3, w * 0.17, h * 0.5
    o += f'<rect x="{px-8}" y="{py-8}" width="{pw+16}" height="{ph+16}" rx="22" fill="#222"/>'
    o += mini_site(px, py, pw, ph, accent, seed + 2)
    o += f'<ellipse cx="{w*0.12}" cy="{h*0.86}" rx="60" ry="16" fill="#fff"/><rect x="{w*0.1}" y="{h*0.8}" width="40" height="44" rx="8" fill="#fff"/>'
    return w, h, o


def phone_scene(w=900, h=800, kind="insta", seed=7):
    bgc = {"insta": ("#f9c8d6", "#f5a77d"), "line": ("#bfe8c6", "#7fcf8f")}[kind]
    a = uid("p")
    o = f'<defs>{lin(a, list(zip((0, 1), bgc)), 1, 1)}</defs><rect width="{w}" height="{h}" fill="url(#{a})"/>'
    pw, ph = w * 0.44, h * 0.9
    px, py = w * 0.28, h * 0.06
    o += f'<rect x="{px-14}" y="{py-14}" width="{pw+28}" height="{ph+28}" rx="44" fill="#1d1f24"/><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="32" fill="#fff"/>'
    if kind == "insta":
        o += f'<circle cx="{px+40}" cy="{py+46}" r="20" fill="#e8643f"/><rect x="{px+72}" y="{py+34}" width="{pw*0.4}" height="14" rx="6" fill="#222"/>'
        cells = [food(300, 300, 1, "pasta"), food(300, 300, 2, "cake"), seascape(300, 300, 3, town=False), food(300, 300, 4, "bowl"),
                 cafe(300, 300, 5, staff=False), seascape(300, 300, 6, sky=("#f7b98a", "#fde7c8"), sun=(.5, .45, "#ff9a4d"), town=False),
                 food(300, 300, 7, "bowl"), food(300, 300, 8, "pasta"), food(300, 300, 9, "cake")]
        cw = (pw - 24) / 3
        for i, s in enumerate(cells):
            o += nest(s, px + 8 + (i % 3) * (cw + 4), py + 90 + (i // 3) * (cw + 4), cw, cw)
    else:
        o += f'<rect x="{px}" y="{py}" width="{pw}" height="70" rx="0" fill="#06c755"/><rect x="{px+24}" y="{py+26}" width="{pw*0.4}" height="16" rx="6" fill="#fff"/>'
        o += nest(food(400, 300, 3, "pasta"), px + 20, py + 100, pw - 40, 200, 14)
        for i in range(3):
            o += f'<rect x="{px+20}" y="{py+330+i*84}" width="{pw*0.78 - (i%2)*40}" height="62" rx="18" fill="{"#e5f7ea" if i%2==0 else "#f1f1f1"}"/>'
        o += f'<rect x="{px+pw*0.3}" y="{py+ph-90}" width="{pw*0.6}" height="48" rx="24" fill="#06c755"/>'
    return w, h, o


def flyer_scene(w=900, h=760, seed=3, a="#f3b24d", b="#e8643f"):
    bg = uid("f")
    o = f'<defs>{lin(bg, [(0, "#efe7da"), (1, "#d9ccb8")])}</defs><rect width="{w}" height="{h}" fill="url(#{bg})"/>'
    def paper(x, y, ww, hh, rot, col, scene):
        s = f'<g transform="rotate({rot} {x+ww/2} {y+hh/2})"><rect x="{x+8}" y="{y+12}" width="{ww}" height="{hh}" fill="#000" opacity=".15"/><rect x="{x}" y="{y}" width="{ww}" height="{hh}" fill="#fff"/>'
        s += nest(scene, x + 14, y + 14, ww - 28, hh * 0.55)
        s += f'<rect x="{x+14}" y="{y+hh*0.65}" width="{ww*0.6}" height="16" rx="4" fill="{col}"/>'
        for i in range(3):
            s += f'<rect x="{x+14}" y="{y+hh*0.73+i*18}" width="{ww*(0.8-i*0.15)}" height="8" rx="3" fill="#cfcfcf"/>'
        return s + "</g>"
    o += paper(w * 0.06, h * 0.12, w * 0.4, h * 0.74, -6, a, food(400, 400, 4, "pasta"))
    o += paper(w * 0.34, h * 0.08, w * 0.34, h * 0.7, 3, b, seascape(400, 400, 8, town=False))
    o += paper(w * 0.62, h * 0.16, w * 0.32, h * 0.7, 8, "#4aa3cf", cafe(400, 400, 6, staff=False))
    return w, h, o


def mikan(w=900, h=800, seed=2):
    rng = random.Random(seed)
    o = nest(seascape(900, 800, seed, sky=("#8fd0ee", "#e6f5fa"), town=False, boats=1), 0, 0, w, h)
    for i in range(7):
        x = w * (0.1 + (i % 4) * 0.25) + rng.random() * 30
        y = h * (0.62 + (i // 4) * 0.2) + rng.random() * 20
        r = 78 + rng.random() * 24
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#f28a1d"/><circle cx="{x-r*0.3:.0f}" cy="{y-r*0.3:.0f}" r="{r*0.3:.0f}" fill="#ffc15a" opacity=".6"/>'
        o += f'<ellipse cx="{x+r*0.1:.0f}" cy="{y-r+4:.0f}" rx="26" ry="11" fill="#3f8f45" transform="rotate(-20 {x:.0f} {y-r:.0f})"/>'
    for i in range(5):
        x, y = rng.random() * w, h * 0.45 + rng.random() * 40
        o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="70" ry="28" fill="#3f8f45" transform="rotate({-30+rng.random()*60:.0f} {x:.0f} {y:.0f})"/>'
    return w, h, o


# ------------------------------------------------------------------ 表紙
def cover(w=600, h=800, issue="Vol.12", color="#1f7bb0", seed=1, accent="#f4d35e", photo=None, label="MITOYO · KANONJI"):
    bg = uid("cv")
    o = f'<defs>{lin(bg, [(0, "#fffdf7"), (1, "#f4ecda")])}</defs><rect width="{w}" height="{h}" fill="url(#{bg})"/>'
    ph = photo or seascape(600, 500, seed, boats=2)
    o += nest(ph, 0, h * 0.16, w, h * 0.62)
    o += f'<rect width="{w}" height="{h*0.18}" fill="#fffdf7" opacity=".92"/>'
    o += f'<text x="34" y="{h*0.118}" font-family="Poppins, Helvetica, Arial, sans-serif" font-weight="800" font-size="{w*0.19}" fill="{color}" letter-spacing="-2">miteGo</text>'
    o += f'<text x="38" y="{h*0.152}" font-family="Helvetica, Arial, sans-serif" font-weight="700" font-size="{w*0.027}" fill="#555" letter-spacing="3">{label}</text>'
    o += f'<rect x="{w*0.7}" y="{h*0.04}" width="{w*0.24}" height="{w*0.075}" rx="6" fill="{accent}"/><text x="{w*0.82}" y="{h*0.04+w*0.052}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-weight="800" font-size="{w*0.045}" fill="#222">{issue}</text>'
    o += f'<rect y="{h*0.78}" width="{w}" height="{h*0.22}" fill="{color}"/>'
    o += f'<text x="34" y="{h*0.855}" font-family="Helvetica, Arial, sans-serif" font-weight="800" font-size="{w*0.075}" fill="#fff">LOCAL MAGAZINE</text>'
    for i in range(3):
        o += f'<rect x="34" y="{h*0.885+i*22}" width="{w*(0.7-i*0.14)}" height="9" rx="4" fill="#fff" opacity=".55"/>'
    o += f'<circle cx="{w*0.84}" cy="{h*0.86}" r="{w*0.08}" fill="{accent}"/><text x="{w*0.84}" y="{h*0.865}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-weight="800" font-size="{w*0.04}" fill="#222">FREE</text>'
    return w, h, o


def mitego_spread(w=1000, h=760):
    o = '<rect width="1000" height="760" fill="#e9f2f6"/>'
    covers = [(cover(issue="Vol.12", color="#1f7bb0", seed=3), 0.06, 0.14, -7),
              (cover(issue="Vol.11", color="#e8643f", seed=9, accent="#9ad0e8", photo=food(600, 500, 3, "pasta")), 0.52, 0.1, 5)]
    for sc, fx, fy, rot in covers:
        x, y, ww, hh = w * fx, h * fy, w * 0.42, w * 0.42 * 800 / 600
        o += f'<g transform="rotate({rot} {x+ww/2} {y+hh/2})"><rect x="{x+10}" y="{y+14}" width="{ww}" height="{hh}" fill="#000" opacity=".18"/>{nest(sc, x, y, ww, hh)}</g>'
    return w, h, o


# ------------------------------------------------------------------ 書き出し
def save(name, scene):
    w, h, body = scene
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(wrap(w, h, body))


def main():
    os.makedirs(OUT, exist_ok=True)
    sunset = dict(sky=("#f6a77a", "#fde3c4"), sea=("#e8a07a", "#6a7fa6"), sun=(.62, .46, "#ff8a3d"), island="#53706a")

    # ヒーロー
    save("hero-landscape", seascape(1600, 900, 11, boats=3, clouds=4))
    save("hero-shop-staff", cafe(900, 760, 3))
    save("hero-photographer", photographer(900, 800))
    save("hero-mitego", mitego_spread(900, 680))
    save("hero-web", laptop_scene(1000, 700))
    save("hero-interview", interview(1000, 760))
    save("hero-mikan", mikan(800, 900, 4))
    save("hero-food", food(900, 700, 5, "pasta"))

    # ABOUT / WHY / RECRUIT / COMPANY
    save("about-interview", interview(1000, 760, 5))
    save("about-photographer", photographer(900, 800, 9))
    save("why-sunset", seascape(1000, 900, 21, **sunset))
    save("recruit", photographer(1000, 760, 12))
    save("company", seascape(1000, 760, 31, boats=2))

    # サービス
    save("service-mitego", mitego_spread(900, 680))
    save("service-web", laptop_scene(900, 680, "#e8643f", 8))
    save("service-sns", phone_scene(900, 680, "insta"))
    save("service-line", phone_scene(900, 680, "line"))
    save("service-photo", photographer(900, 680, 4))
    save("service-design", flyer_scene(900, 680))

    # LOCAL STARTER KIT
    save("starter-kit", cafe(900, 700, 14, staff=True, cap="#4a90b8"))

    # WORKS (8)
    save("works-01", laptop_scene(800, 600, "#d5873a", 3))
    save("works-02", phone_scene(800, 600, "insta"))
    save("works-03", flyer_scene(800, 600, 5))
    save("works-04", seascape(800, 600, 40, sky=("#7ec3ea", "#e4f4fa"), boats=3))
    save("works-05", mitego_spread(800, 600))
    save("works-06", laptop_scene(800, 600, "#d46a8b", 6, ("#f6e6ec", "#ead0da")))
    save("works-07", food(800, 600, 21, "bowl"))
    save("works-08", phone_scene(800, 600, "line"))

    # NEWS (6)
    save("news-01", food(800, 560, 11, "cake"))
    save("news-02", seascape(800, 560, 51, sky=("#7ec3ea", "#e4f4fa"), boats=4))
    save("news-03", cafe(800, 560, 21))
    save("news-04", mikan(800, 560, 6))
    save("news-05", food(800, 560, 13, "bowl"))
    save("news-06", seascape(800, 560, 61, **sunset))

    # miteGo 表紙（最新号 + バックナンバー）
    covers = [("mitego-latest", "Vol.12", "#1f7bb0", 3, None), ("mitego-11", "Vol.11", "#e8643f", 9, food(600, 500, 3, "pasta")),
              ("mitego-10", "Vol.10", "#2a9d8f", 5, mikan(600, 500, 3)), ("mitego-09", "Vol.09", "#8f6bb0", 7, cafe(600, 500, 7)),
              ("mitego-08", "Vol.08", "#d5873a", 2, seascape(600, 500, 62, **sunset))]
    for name, issue, col, seed, ph in covers:
        save(name, cover(600, 800, issue, col, seed, photo=ph))
    print("generated", len(os.listdir(OUT)), "files in", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
