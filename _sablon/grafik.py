"""Ortak grafik yardımcıları — Altın Emlak Gaziosmanpaşa sosyal medya şablonları."""
import math

Y = "#F3BD48"
AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

def up(s): return s.replace("i", "İ").replace("ı", "I").upper()
def ab(m): return up(m)[:3]
def num(v, d=1): return f"{v:.{d}f}".replace(".", ",")
def pct(v, d=1, sign=False):
    s = num(abs(v), d)
    return ("+" if v > 0 else "−" if v < 0 else "") + "%" + s if sign else ("−" if v < 0 else "") + "%" + s
def thou(v):
    return f"{int(round(v)):,}".replace(",", ".")

CSS = """
.rate{font-weight:900;line-height:.86;letter-spacing:-.03em}
.rate small{font-size:.5em;letter-spacing:0;margin-right:.06em;vertical-align:.42em}
.c svg{width:100%;height:auto}
.foot svg{width:34px!important;height:34px!important}
"""

def _smooth(pts):
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i else pts[i]; p1 = pts[i]; p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d

_gid = [0]
def lines(labels, series, W, H, txt="#fff", grid="rgba(255,255,255,.14)", fs=22, dotbg="#000", fmt=lambda v: pct(v), area=True):
    """series: [(ad, [değerler], renk)] — ilk seri vurgulu. Etiketler: her serinin son değeri."""
    allv = [v for _, vs, _ in series for v in vs]
    lo, hi = min(allv), max(allv); r = max(hi - lo, .5)
    lo -= r * .15; hi += r * .2
    pl, pr, pt, pb = 30, 130, fs * 1.6, fs * 2.2
    n = len(labels)
    X = lambda i: pl + i * (W - pl - pr) / max(n - 1, 1)
    Yp = lambda v: pt + (hi - v) / (hi - lo) * (H - pt - pb)
    base = H - pb
    out = "".join(f'<line x1="{pl}" x2="{W-pr}" y1="{pt + k*(base-pt)/3:.1f}" y2="{pt + k*(base-pt)/3:.1f}" stroke="{grid}" stroke-width="2" stroke-dasharray="6 8"/>' for k in range(4))
    defs = ""
    for si, (name, vs, col) in enumerate(series):
        pts = [(X(i), Yp(v)) for i, v in enumerate(vs)]
        path = _smooth(pts)
        if area and si == 0:
            _gid[0] += 1; gid = f"lg{_gid[0]}"
            defs += f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity=".35"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient>'
            out += f'<path d="{path} L{pts[-1][0]:.1f},{base} L{pts[0][0]:.1f},{base} Z" fill="url(#{gid})"/>'
        out += f'<path d="{path}" fill="none" stroke="{col}" stroke-width="{fs*.28:.1f}" stroke-linecap="round"/>'
        for i, (x, y) in enumerate(pts):
            out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{fs*(.5 if i == len(pts)-1 else .3)}" fill="{dotbg}" stroke="{col}" stroke-width="5"/>'
        x, y = pts[-1]
        out += f'<text x="{x + fs*1.1:.1f}" y="{y + fs*.4:.1f}" font-size="{fs*1.15}" font-weight="900" fill="{col}">{fmt(vs[-1])}</text>'
        out += f'<text x="{x + fs*1.1:.1f}" y="{y + fs*1.5:.1f}" font-size="{fs*.75}" font-weight="700" fill="{txt}" opacity=".75">{name}</text>'
    for i, l in enumerate(labels):
        out += f'<text x="{X(i):.1f}" y="{H - fs*.5:.1f}" text-anchor="middle" font-size="{fs*.85}" font-weight="{900 if i == n-1 else 700}" fill="{txt}" opacity="{1 if i == n-1 else .7}" letter-spacing="1">{l}</text>'
    return f'<svg viewBox="0 0 {W} {H}" style="overflow:visible;font-family:Canaro;width:{W}px;height:{H}px"><defs>{defs}</defs>{out}</svg>'

def bars3(groups, W, H, txt="#fff", muted="#3a3a3a", hi=Y, fs=22):
    """groups: [(başlık, [(etiket, değer), (etiket, değer), (etiket, değer)])] — son çubuk vurgulu, her grup kendi ölçeğinde."""
    gw = W / len(groups); out = ""
    for gi, (title, items) in enumerate(groups):
        mx = max(v for _, v in items) * 1.08
        bw = gw * .2; gap = gw * .06; x0 = gi * gw + (gw - (3 * bw + 2 * gap)) / 2
        top = fs * 3.2; base = H - fs * 2.6
        for k, (lab, v) in enumerate(items):
            h = (base - top) * v / mx; x = x0 + k * (bw + gap); last = k == len(items) - 1
            out += f'<rect x="{x:.1f}" y="{base-h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="8" fill="{hi if last else muted}"/>'
            out += f'<text x="{x+bw/2:.1f}" y="{base-h-fs*.5:.1f}" text-anchor="middle" font-size="{fs*(.9 if last else .7)}" font-weight="{900 if last else 700}" fill="{hi if last else txt}">{thou(v)}</text>'
            out += f'<text x="{x+bw/2:.1f}" y="{base+fs*1.2:.1f}" text-anchor="middle" font-size="{fs*.62}" font-weight="700" fill="{txt}" opacity="{1 if last else .65}">{lab}</text>'
        out += f'<text x="{gi*gw + gw/2:.1f}" y="{fs*1.2:.1f}" text-anchor="middle" font-size="{fs*1.15}" font-weight="900" fill="{txt}">{title}</text>'
    return f'<svg viewBox="0 0 {W} {H}" style="font-family:Canaro;width:{W}px;height:{H}px">{out}</svg>'

def hbars(rows, W, rh=64, txt="#fff", muted="#3a3a3a", hi=Y, fs=26, lw=250, vw=170):
    """rows: [(etiket, değer(adet), yıllık değişim %, vurgulu?)]"""
    mx = max(r[1] for r in rows); out = ""
    for i, (lab, v, ch, on) in enumerate(rows):
        y = i * rh; bwid = (W - lw - vw - 20) * v / mx
        c = hi if on else muted; tc = hi if on else txt
        out += f'<text x="0" y="{y+rh*.6:.1f}" font-size="{fs}" font-weight="{900 if on else 700}" fill="{tc}">{lab}</text>'
        out += f'<rect x="{lw}" y="{y+rh*.18:.1f}" width="{bwid:.1f}" height="{rh*.5:.1f}" rx="7" fill="{c}"/>'
        out += f'<text x="{lw+bwid+12:.1f}" y="{y+rh*.6:.1f}" font-size="{fs*.85}" font-weight="800" fill="{tc}">{thou(v)}</text>'
        if ch is not None:
            cc = "#5BD08A" if ch > 0 else "#FF6B5B"
            out += f'<text x="{W}" y="{y+rh*.6:.1f}" text-anchor="end" font-size="{fs*.85}" font-weight="900" fill="{cc}">{pct(ch, 1, True)}</text>'
    return f'<svg viewBox="0 0 {W} {len(rows)*rh}" style="font-family:Canaro;width:{W}px;height:{len(rows)*rh}px">{out}</svg>'

def donut(parts, D, txt="#fff", center="", sub="", sw=70):
    """parts: [(etiket, değer, renk)]"""
    tot = sum(p[1] for p in parts); r = D / 2 - sw / 2 - 4; c = D / 2; acc = 0; out = ""
    for lab, v, col in parts:
        frac = v / tot * 100
        out += (f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}" pathLength="100" '
                f'stroke-dasharray="{frac:.2f} {100-frac:.2f}" stroke-dashoffset="{-acc+25:.2f}"/>')
        acc += frac
    out += f'<text x="{c}" y="{c+10}" text-anchor="middle" font-size="{D*.16:.0f}" font-weight="900" fill="{txt}">{center}</text>'
    out += f'<text x="{c}" y="{c+D*.12:.0f}" text-anchor="middle" font-size="{D*.055:.0f}" font-weight="600" fill="{txt}" opacity=".7">{sub}</text>'
    return f'<svg viewBox="0 0 {D} {D}" style="font-family:Canaro;width:{D}px;height:{D}px">{out}</svg>'

def arrow_svg(c, down=True):
    d = "M12 4v16M5 13l7 7 7-7" if down else "M12 20V4M5 11l7-7 7 7"
    return f'<svg viewBox="0 0 24 24" style="width:1em;height:1em" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>'

def badge(v, txt, bg, fg, fs=28, unit="%"):
    val = (num(abs(v)) + " puan") if unit == "puan" else ("%" + num(abs(v)))
    return (f'<span style="display:inline-flex;align-items:center;gap:12px;background:{bg};color:{fg};font-weight:800;'
            f'font-size:{fs}px;padding:{fs*.4:.0f}px {fs*.8:.0f}px;border-radius:999px">{arrow_svg(fg, v < 0)}'
            f'{val} <span style="font-weight:500;opacity:.8">{txt}</span></span>')

ICONS = {
 "pct": '<path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
 "cal": '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/>',
 "trend": '<path d="M3 6l6 6 4-4 8 8"/><path d="M15 16h6v-6"/>',
 "trendup": '<path d="M3 18l6-6 4 4 8-8"/><path d="M15 8h6v6"/>',
 "home": '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
 "key": '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3L20 3M16 7l3 3M14 9l2 2"/>',
 "bank": '<path d="M3 10h18L12 4z"/><path d="M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
 "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
}
def icon(k, c="#000", s=56):
    return f'<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

def house(c, W):
    return (f'<svg viewBox="0 0 200 180" style="width:{W}px;height:{W*.9:.0f}px" fill="none" stroke="{c}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round">'
            f'<path d="M14 84 L100 14 L186 84"/><path d="M144 50 V22 h20 v44"/><path d="M34 70 V170 H166 V70"/>'
            f'<rect x="84" y="118" width="32" height="52"/><path d="M56 96 h22 v22 h-22z M122 96 h22 v22 h-22z"/></svg>')

def card(k, v, sub, dark=True, accent=False, w="100%"):
    bg = "#161616" if dark else "#fff"; fg = "#fff" if dark else "#000"
    bd = Y if accent else ("#2c2c2c" if dark else "#000")
    vc = Y if (accent and dark) else fg
    return (f'<div style="width:{w};background:{bg};color:{fg};border:3px solid {bd};border-radius:18px;padding:26px 28px">'
            f'<div style="font-size:21px;font-weight:800;letter-spacing:.1em;opacity:.7">{k}</div>'
            f'<div style="font-size:58px;font-weight:900;line-height:1.05;margin-top:8px;color:{vc}">{v}</div>'
            f'<div style="font-size:22px;font-weight:600;margin-top:8px">{sub}</div></div>')

def chg(v, good_up=True):
    if v is None: return ""
    col = "#3BB273" if (v > 0) == good_up else "#E5533D"
    return f'<span style="color:{col};font-weight:900">{pct(v, 1, True)}</span>'


# ---------------- DİKKAT ÇEKİCİ KAPAK ----------------
def sunburst(W, H, cx, cy, n=28, col=Y, op=.07):
    import math
    R = max(W, H) * 1.5; out = ""
    for i in range(0, n, 2):
        a1 = 2 * math.pi * i / n; a2 = 2 * math.pi * (i + 1) / n
        out += (f'<path d="M{cx},{cy} L{cx+R*math.cos(a1):.0f},{cy+R*math.sin(a1):.0f} '
                f'L{cx+R*math.cos(a2):.0f},{cy+R*math.sin(a2):.0f} Z" fill="{col}" opacity="{op}"/>')
    return f'<svg viewBox="0 0 {W} {H}" style="position:absolute;inset:0;width:{W}px;height:{H}px">{out}</svg>'

def iso_house(W, down=True):
    arrow = ('<path d="M20 60 L150 150 L190 115 L330 235" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
             '<path d="M300 250 L360 255 L345 195 Z" fill="#fff"/>') if down else \
            ('<path d="M20 250 L150 160 L190 195 L330 75" fill="none" stroke="#fff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>'
             '<path d="M300 60 L360 55 L345 115 Z" fill="#fff"/>')
    return (f'<svg viewBox="0 0 400 420" style="width:{W}px;height:{W*1.05:.0f}px;overflow:visible">'
            '<ellipse cx="200" cy="392" rx="170" ry="26" fill="#000" opacity=".55"/>'
            '<polygon points="60,200 200,280 200,380 60,300" fill="#C99528"/>'
            '<polygon points="60,200 200,280 130,160" fill="#B5861F"/>'
            '<polygon points="200,280 340,200 340,300 200,380" fill="#F3BD48"/>'
            '<polygon points="130,160 270,80 340,200 200,280" fill="#FFD978"/>'
            '<polygon points="130,160 270,80 278,94 138,174" fill="#fff" opacity=".5"/>'
            '<polygon points="240,122 262,110 262,70 240,82" fill="#C99528"/><polygon points="262,110 278,120 278,80 262,70" fill="#F3BD48"/>'
            '<polygon points="115,262 145,279 145,331 115,314" fill="#000" opacity=".8"/>'
            '<polygon points="225,282 255,265 255,297 225,314" fill="#000" opacity=".8"/>'
            '<polygon points="285,248 315,231 315,263 285,280" fill="#000" opacity=".8"/>'
            f'<g transform="translate(20,40)">{arrow}</g></svg>')

def sticker(lines, small, size=210, rot=-12):
    inner = "".join(f'<div style="font-size:{size*.2:.0f}px;font-weight:900;line-height:.95">{l}</div>' for l in lines)
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:#fff;color:#000;transform:rotate({rot}deg);'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;'
            f'box-shadow:0 0 0 10px #000,0 0 0 16px {Y},0 20px 40px rgba(0,0,0,.5)">'
            f'<div style="font-size:{size*.09:.0f}px;font-weight:800;letter-spacing:.14em;margin-bottom:6px">{small}</div>{inner}</div>')

HERO_CSS = """
.hero-num{font-weight:900;line-height:.85;letter-spacing:-.03em;color:#F3BD48;
 text-shadow:1px 1px 0 #B5861F,2px 2px 0 #B5861F,3px 3px 0 #B5861F,4px 4px 0 #A87A17,5px 5px 0 #A87A17,6px 6px 0 #A87A17,7px 7px 0 #8F6A1C,8px 8px 0 #8F6A1C,9px 9px 0 #8F6A1C,10px 10px 0 #7A5A16,11px 11px 0 #7A5A16,12px 12px 0 #6B4F13,16px 20px 30px rgba(0,0,0,.6)}
.hero-num small{font-size:.48em;vertical-align:.5em;margin-right:.04em}
.hero-title{font-weight:900;line-height:.92;letter-spacing:-.01em;color:#fff}
.hero-title span{background:#F3BD48;color:#000;padding:0 .14em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
"""

def hero_cover(W, H, logo_src, dots_html, title_html, num_html, sub, sticker_lines, sticker_small, badge_html, down=True, cta="KAYDIRIN →"):
    story = H > 1500
    return f"""
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 55% at 75% 62%, rgba(243,189,72,.32), rgba(0,0,0,0) 70%),#000"></div>
{sunburst(W, H, W*.74, H*.64)}
<div style="position:absolute;right:{10 if not story else 20}px;bottom:{150 if not story else 300}px">{iso_house(470 if not story else 560, down)}</div>
<div style="position:absolute;right:56px;top:{230 if not story else 380}px">{sticker(sticker_lines, sticker_small, 200 if not story else 230)}</div>
<div style="position:relative;padding:{72 if not story else 150}px 64px 0;display:flex;justify-content:space-between;align-items:center">
  <img src="{logo_src}" style="height:{110 if not story else 120}px;margin-left:-12px">{dots_html}</div>
<div style="position:relative;padding:0 64px;margin-top:{70 if not story else 120}px">
  <div class="hero-title" style="font-size:{108 if not story else 124}px;max-width:720px">{title_html}</div>
  <div class="hero-num" style="font-size:{250 if not story else 290}px;margin-top:{44 if not story else 70}px">{num_html}</div>
  <div style="font-size:{30 if not story else 36}px;font-weight:700;color:#fff;margin-top:22px;max-width:560px;line-height:1.3">{sub}</div>
  <div style="margin-top:24px">{badge_html}</div>
</div>
<div style="position:absolute;left:-40px;right:-40px;bottom:{46 if not story else 120}px;height:{96 if not story else 120}px;background:#F3BD48;transform:rotate(-3deg);display:flex;align-items:center;justify-content:space-between;padding:0 104px;color:#000;font-weight:900;font-size:{34 if not story else 40}px;letter-spacing:.08em;box-shadow:0 -10px 30px rgba(0,0,0,.4)">
  <span>@altinemlakgop</span><span>{cta}</span></div>"""


# ---------------- TEK TESPİT SAYFASI (yorum carousel'leri) ----------------
def insight_slide(page_fn, css, logo_fn, dots_fn, footer_fn, idx, n, y, grup, no, toplam, dark):
    bg = "k" if dark else "y"; fg = "#fff" if dark else "#000"; acc = Y if dark else "#000"
    lg = logo_fn('yatay_siyah-zemin' if dark else 'yatay_sari-zemin')
    numcls = "hero-num" if dark else ""
    numstyle = "" if dark else "font-weight:900;line-height:.9;letter-spacing:-.02em;color:#000"
    head = (f'<div style="position:relative;padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">'
            f'<img src="{lg}" style="height:{110}px;margin-left:-12px"><span style="color:{Y if dark else "#000"}">{dots_fn(n, idx)}</span></div>')
    return page_fn(1080, 1350, bg, f"""
{'' if not dark else sunburst(1080, 1350, 900, 1150, op=.05)}
{head}
<div style="position:absolute;right:-90px;top:250px;width:520px;height:520px;border-radius:50%;background:{'#161616' if dark else '#000'};opacity:{1 if dark else .07}"></div>
<div style="position:absolute;right:70px;top:330px;width:250px;height:250px;border-radius:56px;background:{Y if dark else '#000'};display:flex;align-items:center;justify-content:center;transform:rotate(-8deg);box-shadow:0 30px 60px rgba(0,0,0,.35)">{icon(y['ikon'], '#000' if dark else Y, 150)}</div>
<div style="position:relative;padding:0 64px;margin-top:70px">
  <span class="tag" style="background:{Y if dark else '#000'};color:{'#000' if dark else Y}">{grup} · {no}/{toplam}</span>
  <div style="font-size:24px;font-weight:800;letter-spacing:.12em;margin-top:34px;color:{acc};opacity:.85">{y['etiket']}</div>
  <h1 style="font-weight:900;font-size:84px;line-height:1.0;margin-top:14px;max-width:640px;color:{fg}">{y['baslik']}</h1>
</div>
<div style="position:relative;padding:0 64px;margin-top:60px">
  <div class="{numcls}" style="font-size:{170 if len(y['deger']) <= 7 else 120}px;{numstyle}">{y['deger']}</div>
  <div style="font-size:28px;font-weight:700;margin-top:22px;color:{fg};opacity:.85;max-width:900px">{y['aciklama']}</div>
</div>
<div style="position:absolute;left:64px;right:64px;bottom:140px;border-left:10px solid {Y if dark else '#000'};padding:6px 0 6px 28px;font-size:32px;font-weight:600;line-height:1.35;color:{fg}">
  <span style="font-weight:900">Yorumum:</span> {y.get('yorum','')}</div>
{footer_fn('fy' if dark else 'fk', 100, addr=False)}""", css)
