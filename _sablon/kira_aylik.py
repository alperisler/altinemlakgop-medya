"""Aylık kira artış oranı seti — Altın Emlak Gaziosmanpaşa.

Veri: kira_veri.json (son eleman = yeni açıklanan ay). Kullanım:
    python3 kira_aylik.py <çıktı_klasörü>
12 PNG üretir: 4:5, kare, 5'li carousel, 3 story + geçmiş 12 ay post + story.
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import page, footer, dots, logo, render, PH, IGI, PIN, PHONE, IG, ADDR

KIT = pathlib.Path(__file__).parent
D = json.loads((KIT / "kira_veri.json").read_text(encoding="utf-8"))
OR = D["oranlar"]; SA = D["son_aciklama"]
CUR, PREV = OR[-1], OR[-2]
AY, YIL, R = CUR["ay"], CUR["yil"], CUR["oran"]
UP = R > PREV["oran"]

TRMAP = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
SLUG = f"kira-{AY.translate(TRMAP).lower()}-{YIL}"
FOLDER = f"Kira Artış {AY} {YIL}"

def num(v, d=2): return f"{v:.{d}f}".replace(".", ",")
def pct(v): return "%" + num(v)
def tl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s[:-3] if s.endswith(",00") else s
def up(s): return s.replace("i", "İ").replace("ı", "I").upper()
def ab(m): return up(m)[:3]

RATE = num(R)
MULT = f"{1 + R/100:.4f}".replace(".", ",")
TABLE = [(a, round(a * (1 + R/100), 2)) for a in (15000, 20000, 25000, 30000, 40000)]
LAST6 = OR[-6:]
YON = "geriledi" if not UP else "yükseldi"

EXTRA = """
.rate{font-weight:900;line-height:.86;letter-spacing:-.03em}
.rate small{font-size:.5em;letter-spacing:0;margin-right:.06em;vertical-align:.42em}
.c svg{width:100%;height:auto}
.foot svg{width:34px!important;height:34px!important}
table{border-collapse:collapse;width:100%}
th{font-weight:800;font-size:24px;letter-spacing:.12em;text-align:left;padding:20px 24px}
td{font-size:36px;font-weight:500;padding:20px 24px;border-bottom:3px solid #000}
td.n{font-weight:900}
.bars{display:flex;align-items:flex-end;gap:22px}
.bar{display:flex;flex-direction:column;align-items:center;gap:12px;flex:1}
.bar .v{font-weight:800;font-size:28px}
.bar .m{font-weight:800;font-size:26px;letter-spacing:.1em}
.row{display:flex;align-items:center;gap:20px}
.row .mo{flex:none;font-weight:700;letter-spacing:.02em}
.row .mo span{font-weight:400;opacity:.55;margin-left:8px}
.row .tr{flex:1}
.row .b{background:#3a3a3a}
.row .v{flex:none;font-weight:800;text-align:right}
.row.on .b{background:var(--y)} .row.on .mo,.row.on .v{color:var(--y)}
.row.first .b{background:#fff}
"""


# ---------------- GRAFİK YARDIMCILARI ----------------
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
def line_chart(items, W, H, line="#000", txt="#000", hi="#000", grid="rgba(0,0,0,.15)", fs=22, dotbg="#F3BD48", show_all=False):
    _gid[0] += 1; gid = f"g{_gid[0]}"
    vals = [x["oran"] for x in items]
    lo, hi_v = min(vals), max(vals); r = max(hi_v - lo, .5)
    lo -= r * .12; hi_v += r * .18
    pl, pr, pt, pb = 30, 30, fs * 2.6, fs * 2.2
    n = len(vals)
    xs = [pl + i * (W - pl - pr) / (n - 1) for i in range(n)]
    ys = [pt + (hi_v - v) / (hi_v - lo) * (H - pt - pb) for v in vals]
    pts = list(zip(xs, ys)); path = _smooth(pts)
    base = H - pb
    area = path + f" L{xs[-1]:.1f},{base} L{xs[0]:.1f},{base} Z"
    g = "".join(f'<line x1="{pl}" x2="{W-pr}" y1="{pt + k*(base-pt)/3:.1f}" y2="{pt + k*(base-pt)/3:.1f}" stroke="{grid}" stroke-width="2" stroke-dasharray="6 8"/>' for k in range(4))
    dots, labs = "", ""
    for i, (x, y) in enumerate(pts):
        last = i == n - 1
        if last:
            dots += f'<circle cx="{x}" cy="{y}" r="{fs*1.05}" fill="{line}" opacity=".18"/><circle cx="{x}" cy="{y}" r="{fs*.55}" fill="{line}"/><circle cx="{x}" cy="{y}" r="{fs*.25}" fill="{dotbg}"/>'
        else:
            dots += f'<circle cx="{x}" cy="{y}" r="{fs*.3}" fill="{dotbg}" stroke="{line}" stroke-width="4"/>'
        if show_all or i in (0, n - 1) or vals[i] == max(vals):
            anchor = "start" if i == 0 else ("end" if last else "middle")
            labs += f'<text x="{x}" y="{y - fs*1.25:.1f}" text-anchor="{anchor}" font-size="{fs*(1.25 if last else 1)}" font-weight="{900 if last else 800}" fill="{hi if last else txt}">{pct(vals[i])}</text>'
        labs += f'<text x="{x}" y="{H - fs*.5:.1f}" text-anchor="middle" font-size="{fs*.85}" font-weight="{900 if last else 700}" fill="{hi if last else txt}" opacity="{1 if last else .7}" letter-spacing="1">{ab(items[i]["ay"])}</text>'
    return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="overflow:visible;font-family:Canaro">'
            f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{line}" stop-opacity=".35"/><stop offset="1" stop-color="{line}" stop-opacity="0"/></linearGradient></defs>'
            f'{g}<path d="{area}" fill="url(#{gid})"/><path d="{path}" fill="none" stroke="{line}" stroke-width="{fs*.28:.1f}" stroke-linecap="round"/>{dots}{labs}</svg>')

def gauge(v, W, track="#2a2a2a", fill="#F3BD48", txt="#fff", vmax=50):
    R = W / 2 - 40; cx = W / 2; cy = R + 40; sw = 56; H = cy + sw/2 + 50
    arc = f"M{cx-R},{cy} A{R},{R} 0 0 1 {cx+R},{cy}"
    import math
    ticks = (f'<text x="{cx-R}" y="{cy+sw/2+40}" text-anchor="middle" font-size="24" font-weight="700" fill="{txt}" opacity=".55">%0</text>'
             f'<text x="{cx+R}" y="{cy+sw/2+40}" text-anchor="middle" font-size="24" font-weight="700" fill="{txt}" opacity=".55">%{vmax}</text>')
    a = math.pi * (1 - v / vmax)
    nx, ny = cx + R * math.cos(a), cy - R * math.sin(a)
    return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="font-family:Canaro;width:{W}px;height:{H}px">'
            f'<path d="{arc}" fill="none" stroke="{track}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path d="{arc}" fill="none" stroke="{fill}" stroke-width="{sw}" stroke-linecap="round" pathLength="100" stroke-dasharray="{v/vmax*100:.2f} 200"/>'
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{sw*.62}" fill="{fill}" stroke="{txt}" stroke-width="8"/>{ticks}</svg>')

def arrow_svg(c, down=True):
    d = "M12 4v16M5 13l7 7 7-7" if down else "M12 20V4M5 11l7-7 7 7"
    return f'<svg viewBox="0 0 24 24" style="width:1em;height:1em" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg>'

def delta(bg, fg, fs=30):
    dv = R - PREV["oran"]
    return (f'<span style="display:inline-flex;align-items:center;gap:12px;background:{bg};color:{fg};font-weight:800;'
            f'font-size:{fs}px;padding:{fs*.4:.0f}px {fs*.8:.0f}px;border-radius:999px">{arrow_svg(fg, dv < 0)}'
            f'{PREV["ay"]} ayında <span style="font-weight:900">{pct(PREV["oran"])}</span> idi</span>')

ICONS = {
 "pct": '<path d="M19 5L5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
 "cal": '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/><path d="M7 14h3M14 14h3M7 17h3"/>',
 "trend": '<path d="M3 6l6 6 4-4 8 8"/><path d="M15 16h6v-6"/>',
 "trendup": '<path d="M3 18l6-6 4 4 8-8"/><path d="M15 8h6v6"/>',
}
def icon(k, c="#000", s=56):
    return f'<svg viewBox="0 0 24 24" style="width:{s}px;height:{s}px" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg>'

def house(c, W):
    return (f'<svg viewBox="0 0 200 180" width="{W}" fill="none" stroke="{c}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round">'
            f'<path d="M14 84 L100 14 L186 84"/><path d="M144 50 V22 h20 v44"/><path d="M34 70 V170 H166 V70"/>'
            f'<rect x="84" y="118" width="32" height="52"/><path d="M56 96 h22 v22 h-22z M122 96 h22 v22 h-22z"/></svg>')

def P(w, h, cls, inner): return page(w, h, cls, inner, EXTRA)

def head(lg, n=None, i=None, tag=None, h=110, ml=-12, col=""):
    right = (f'<span class="tag" style="background:#000;color:var(--y)">{tag}</span>' if tag
             else (f'<span style="{col}">{dots(n, i)}</span>' if n else ""))
    return (f'<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">'
            f'<img src="{logo(lg)}" style="height:{h}px;margin-left:{ml}px">{right}</div>')

def span(vals, pad):
    lo, hi = min(vals), max(vals); r = max(hi - lo, 0.5)
    return lo - r * pad, hi + r * 0.1

def bars(maxh):
    lo, hi = span([x["oran"] for x in LAST6], 0.45)
    out = ""
    for k, x in enumerate(LAST6):
        on = k == len(LAST6) - 1
        hh = int((x["oran"] - lo) / (hi - lo) * maxh)
        c = "var(--y)" if on else "#fff"
        out += (f'<div class="bar"><div class="v" style="color:{c}">{pct(x["oran"])}</div>'
                f'<div style="width:100%;height:{hh}px;background:{"var(--y)" if on else "#3a3a3a"}"></div>'
                f'<div class="m" style="color:{c}">{ab(x["ay"])}</div></div>')
    return f'<div class="bars">{out}</div>'

def table():
    rows = "".join(f'<tr><td>{tl(a)} TL</td><td>+{tl(b-a)} TL</td><td class="n">{tl(b)} TL</td></tr>' for a, b in TABLE)
    return f'<table><tr style="background:#000;color:var(--y)"><th>MEVCUT KİRA</th><th>ARTIŞ</th><th>YENİ KİRA</th></tr>{rows}</table>'

def hist_rows(rh, bh, fs, mow, vw):
    data = OR[-13:]
    lo, hi = span([x["oran"] for x in data], 0.35)
    out = ""
    for i, x in enumerate(data):
        cls = "on" if i == len(data) - 1 else ("first" if i == 0 else "")
        w = (x["oran"] - lo) / (hi - lo) * 100
        out += (f'<div class="row {cls}" style="height:{rh}px">'
                f'<div class="mo" style="width:{mow}px;font-size:{fs}px">{x["ay"]}<span>{str(x["yil"])[2:]}</span></div>'
                f'<div class="tr"><div class="b" style="width:{w:.1f}%;height:{bh}px"></div></div>'
                f'<div class="v" style="width:{vw}px;font-size:{fs+2}px">{pct(x["oran"])}</div></div>')
    return out

H0 = OR[-13]["oran"] if len(OR) >= 13 else OR[0]["oran"]
YDIFF = R - H0
YTXT = f'1 yıl önce <b style="color:var(--y);font-weight:800">{pct(H0)}</b> idi'

T = {}
T[f"{SLUG}_01_dikey-4x5"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', tag='KİRA ARTIŞI', h=118, ml=-14)}
<div style="padding:0 64px;margin-top:100px">
  <div style="width:120px;height:14px;background:#000;margin-bottom:40px"></div>
  <h1 style="font-weight:900;font-size:92px;line-height:1.0">{AY} ayı kira artış oranı açıklandı</h1>
  <div class="rate" style="font-size:300px;margin-top:40px"><small>%</small>{RATE}</div>
  <p style="font-weight:500;font-size:34px;line-height:1.35;margin-top:30px;max-width:900px">{AY} ayında yenilenen konut ve iş yeri kira sözleşmeleri için yasal üst sınır. <span style="font-weight:400;opacity:.8">(son 12 ayın ortalama enflasyonu)</span></p>
</div>
{footer('fk', 160)}""")

T[f"{SLUG}_02_kare-1x1"] = P(1080, 1080, "k", f"""
{head('yatay_siyah-zemin', h=104)}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">YASAL ÜST SINIR</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:34px">{AY} ayı kira<br>artış oranı</h1>
  <div class="rate" style="font-size:270px;color:var(--y);margin-top:26px"><small>%</small>{RATE}</div>
</div>
{footer('fy', 120, addr=False)}""")

N = 5
T[f"{SLUG}_03_carousel-4x5_1-kapak"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, 0, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:130px">
  <span class="tag" style="background:var(--y);color:#000">{up(AY)} {YIL}</span>
  <h1 style="font-weight:900;font-size:104px;line-height:.98;margin-top:40px">Kira artış<br>oranı<br>açıklandı</h1>
  <div class="rate" style="font-size:280px;color:var(--y);margin-top:40px"><small>%</small>{RATE}</div>
</div>
<div style="margin-top:auto;padding:0 64px 64px;display:flex;justify-content:flex-end;font-weight:700;font-size:32px;color:var(--y);letter-spacing:.06em">KAYDIRIN →</div>""")

items = [(f"En fazla %{RATE} zam", f"{AY} ayında yenilenen konut ve iş yeri sözleşmelerinde kira bu oranın üzerinde artırılamaz."),
         ("Son 12 ayın ortalaması", f"Oran, açıklanan yıllık enflasyon ({pct(SA['tufe_yillik'])}) değil, son 12 ayın ortalama enflasyonu esas alınarak belirlenir."),
         (f"{PREV['ay']} ayına göre {YON}", f"{PREV['ay']} ayında {pct(PREV['oran'])} olan tavan oran {AY} ayında {pct(R)} oldu.")]
rows = "".join(f"""<div style="display:flex;gap:36px;align-items:flex-start;padding:40px 0;border-top:3px solid #000">
  <div style="flex:none;width:96px;height:96px;background:var(--y);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:56px">{n}</div>
  <div><h2 style="font-weight:800;font-size:48px;line-height:1.1">{t}</h2><p style="font-weight:400;font-size:32px;line-height:1.35;margin-top:12px">{d}</p></div></div>"""
  for n, (t, d) in enumerate(items, 1))
T[f"{SLUG}_03_carousel-4x5_2-icerik"] = P(1080, 1350, "w", f"""
{head('yatay_beyaz-zemin', N, 1, h=84, ml=0)}
<div style="padding:0 64px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y)">NE ANLAMA GELİYOR?</span>
  <div style="margin-top:40px">{rows}</div>
</div>
{footer('fk', 120, addr=False)}""")

T[f"{SLUG}_03_carousel-4x5_3-hesaplama"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', N, 2, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:#000;color:var(--y)">KİRA HESAPLAMA</span>
  <h1 style="font-weight:900;font-size:72px;line-height:1.0;margin-top:30px">Yeni kiranız<br>ne kadar olacak?</h1>
  <p style="font-weight:500;font-size:32px;margin:18px 0 30px">Mevcut kira × {MULT} = azami yeni kira</p>
  {table()}
  <p style="font-weight:400;font-size:24px;line-height:1.4;margin-top:24px;opacity:.85">Tabloda azami oran uygulanmıştır; taraflar daha düşük bir artışta anlaşabilir.</p>
</div>
{footer('fk', 120, addr=False)}""")

T[f"{SLUG}_03_carousel-4x5_4-trend"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, 3, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:90px">
  <span class="tag" style="background:var(--y);color:#000">SON 6 AY</span>
  <h1 style="font-weight:900;font-size:88px;line-height:1.0;margin-top:34px">Tavan oran<br><span style="color:var(--y)">6 ayda {"yükseldi" if R > LAST6[0]["oran"] else "geriledi"}.</span></h1>
  <p style="font-weight:400;font-size:32px;margin-top:22px;opacity:.85">{LAST6[0]['ay']} {pct(LAST6[0]['oran'])} → {AY} {pct(R)}</p>
</div>
<div style="margin-top:auto;padding:0 64px 64px">{bars(400)}</div>""")

T[f"{SLUG}_03_carousel-4x5_5-kapanis"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', N, 4, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:130px">
  <h1 style="font-weight:900;font-size:104px;line-height:1.02">Kiranızı doğru belirleyelim.</h1>
  <p style="font-weight:500;font-size:36px;line-height:1.35;margin-top:40px;max-width:900px">Yasal artış hesabı, bölgedeki güncel kira değerleri ve sözleşme yenileme için ofisimizi arayın.</p>
  <div style="margin-top:64px;background:#000;color:var(--y);font-weight:900;font-size:96px;padding:30px 40px;border-radius:10px;display:inline-block;letter-spacing:.01em">{PHONE}</div>
</div>
<div style="margin-top:auto;padding:0 64px 56px;font-weight:700;font-size:32px">{IG}<div style="font-weight:400;font-size:24px;margin-top:10px">{ADDR}</div></div>""")

T[f"{SLUG}_04_story-9x16_1-oran"] = P(1080, 1920, "k", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:120px;margin-left:-12px"></div>
<div style="padding:0 80px;margin-top:170px">
  <span class="tag" style="background:var(--y);color:#000">TÜİK · {up(SA['tarih'])}</span>
  <h1 style="font-weight:900;font-size:120px;line-height:.98;margin-top:44px">{AY} ayı<br>kira artış<br>oranı</h1>
  <div class="rate" style="font-size:290px;color:var(--y);margin-top:50px"><small>%</small>{RATE}</div>
  <p style="font-weight:400;font-size:38px;line-height:1.35;margin-top:44px;opacity:.9">{AY} ayında yenilenen kira sözleşmeleri için yasal üst sınır.</p>
</div>
<div style="margin-top:auto;height:230px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:40px;letter-spacing:.02em">Yeni kiranızı hesaplayın →</div>""")

T[f"{SLUG}_04_story-9x16_2-hesaplama"] = P(1080, 1920, "w", f"""
<div class="y" style="height:640px;padding:150px 80px 0">
  <img src="{logo('yatay_sari-zemin')}" style="height:120px;margin-left:-14px">
  <h1 style="font-weight:900;font-size:104px;line-height:1.0;margin-top:70px">Yeni kiranız<br>ne kadar olacak?</h1>
</div>
<div style="padding:70px 80px 0">
  <p style="font-weight:700;font-size:40px;margin-bottom:40px">Mevcut kira × {MULT}</p>
  {table()}
  <p style="font-weight:400;font-size:28px;line-height:1.4;margin-top:30px;opacity:.8">Azami %{RATE} artış uygulanmıştır.</p>
</div>
<div style="margin-top:auto;height:190px;background:#000;color:var(--y);display:flex;align-items:center;justify-content:center;gap:16px;font-weight:800;font-size:44px;stroke:var(--y)"><span style="display:inline-flex;width:46px">{PH}</span>{PHONE}</div>""")

T[f"{SLUG}_04_story-9x16_3-iletisim"] = P(1080, 1920, "w", f"""
<div class="y" style="height:880px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-top:120px">
  <img src="{logo('dikey_sari-zemin')}" style="width:640px">
</div>
<div style="padding:90px 80px 0;flex:1">
  <div class="tag" style="background:#000;color:var(--y)">KİRA DANIŞMANLIĞI</div>
  <h1 style="font-weight:900;font-size:96px;line-height:1.02;margin-top:36px">Kiranızı doğru<br>belirleyelim.</h1>
  <div style="margin-top:56px;display:flex;flex-direction:column;gap:34px;font-size:40px">
    <div style="display:flex;gap:22px;align-items:center;font-weight:800;font-size:56px"><span style="display:inline-flex;width:56px;stroke:#000">{PH}</span>{PHONE}</div>
    <div style="display:flex;gap:22px;align-items:center;font-weight:700"><span style="display:inline-flex;width:48px;stroke:#000">{IGI}</span>{IG}</div>
    <div style="display:flex;gap:22px;align-items:flex-start;font-weight:400;font-size:33px;line-height:1.35"><span style="display:inline-flex;flex:none;width:48px;stroke:#000">{PIN}</span>Sarıgöl Mah. Mezarlık Sk.<br>D1 Blok No:112A TOKİ Konutları<br>Gaziosmanpaşa / İstanbul</div>
  </div>
</div>
<div style="height:170px;background:#000;color:var(--y);display:flex;align-items:center;justify-content:center;font-weight:500;font-size:26px;letter-spacing:.04em">Her Ofis Özel Yetkili Bir Emlak İşletmesidir.</div>""")

T[f"{SLUG}_05_gecmis_post-4x5"] = P(1080, 1350, "k", f"""
<div style="padding:64px 64px 0;display:flex;justify-content:space-between;align-items:center">
  <img src="{logo('yatay_siyah-zemin')}" style="height:100px;margin-left:-12px">
  <span class="tag" style="background:var(--y);color:#000">SON 12 AY</span>
</div>
<div style="padding:0 64px;margin-top:40px;display:flex;justify-content:space-between;align-items:flex-end">
  <h1 style="font-weight:900;font-size:66px;line-height:1.0">{AY} ayı<br>kira artış oranı</h1>
  <div class="rate" style="font-size:150px;color:var(--y)"><small>%</small>{RATE}</div>
</div>
<div style="padding:0 64px;margin-top:22px;font-size:27px;font-weight:400;opacity:.85">{YTXT} · son 12 ayın ortalama enflasyonu</div>
<div style="padding:0 64px;margin-top:30px">{hist_rows(60, 32, 27, 196, 130)}</div>
{footer('fy', 110, addr=False)}""")

T[f"{SLUG}_05_gecmis_story-9x16"] = P(1080, 1920, "k", f"""
<div style="padding:140px 72px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:116px;margin-left:-12px"></div>
<div style="padding:0 72px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">KİRA ARTIŞ ORANLARI · SON 12 AY</span>
  <h1 style="font-weight:900;font-size:86px;line-height:1.0;margin-top:34px">{AY} ayı<br>kira artış oranı</h1>
  <div class="rate" style="font-size:230px;color:var(--y);margin-top:18px"><small>%</small>{RATE}</div>
  <div style="font-size:32px;font-weight:400;opacity:.85;margin-top:24px">{YTXT}</div>
</div>
<div style="padding:0 72px;margin-top:44px">{hist_rows(59, 34, 30, 220, 150)}</div>
<div style="margin-top:auto;height:190px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;gap:16px;font-weight:800;font-size:44px;stroke:#000"><span style="display:inline-flex;width:46px">{PH}</span>{PHONE}<span style="font-weight:500;font-size:32px;margin-left:18px">{IG}</span></div>""")

# ---------------- GRAFİKLİ SÜRÜMLER (yukarıdakilerin yerine geçer) ----------------
L12 = OR[-12:]
DOWN = R < PREV["oran"]
T[f"{SLUG}_01_dikey-4x5"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', tag='KİRA ARTIŞI', h=118, ml=-14)}
<div style="padding:0 64px;margin-top:64px">
  <h1 style="font-weight:900;font-size:80px;line-height:1.0">{AY} ayı kira artış<br>oranı açıklandı</h1>
  <div style="display:flex;align-items:flex-end;gap:30px;margin-top:30px">
    <div class="rate" style="font-size:250px"><small>%</small>{RATE}</div>
  </div>
  <div style="margin-top:26px">{delta('#000', '#F3BD48', 28)}</div>
</div>
<div style="padding:0 34px;margin-top:26px">{line_chart(L12, 1012, 340, line='#000', txt='#000', hi='#000', grid='rgba(0,0,0,.18)', fs=22, dotbg='#F3BD48')}</div>
{footer('fk', 150)}""")

T[f"{SLUG}_02_kare-1x1"] = P(1080, 1080, "k", f"""
{head('yatay_siyah-zemin', h=104)}
<div style="text-align:center;margin-top:44px">
  <h1 style="font-weight:900;font-size:60px;line-height:1.05">{AY} ayı kira artış oranı</h1>
</div>
<div style="position:relative;display:flex;justify-content:center;margin-top:24px">
  {gauge(R, 800)}
  <div style="position:absolute;left:0;right:0;top:215px;text-align:center">
    <div class="rate" style="font-size:185px;color:var(--y)"><small>%</small>{RATE}</div>
    <div style="font-size:22px;font-weight:500;opacity:.75;margin-top:14px">Son 12 ayın ortalama enflasyonu · yasal üst sınır</div>
  </div>
</div>
<div style="display:flex;justify-content:center;margin:6px 0 0">{delta('#F3BD48', '#000', 26)}</div>
{footer('fy', 110, addr=False)}""")

T[f"{SLUG}_03_carousel-4x5_1-kapak"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, 0, col='color:var(--y)')}
<div style="position:absolute;right:40px;bottom:110px;opacity:.95">{house('#F3BD48', 340)}</div>

<div style="padding:0 64px;margin-top:110px;position:relative">
  <span class="tag" style="background:var(--y);color:#000">{up(AY)} {YIL}</span>
  <h1 style="font-weight:900;font-size:104px;line-height:.98;margin-top:40px">Kira artış<br>oranı<br>açıklandı</h1>
  <div class="rate" style="font-size:230px;color:var(--y);margin-top:40px"><small>%</small>{RATE}</div>
  <div style="margin-top:30px">{delta('#F3BD48', '#000', 28)}</div>
</div>
<div style="margin-top:auto;padding:0 64px 64px;display:flex;justify-content:flex-start;font-weight:700;font-size:32px;color:var(--y);letter-spacing:.06em;position:relative">KAYDIRIN →</div>""")

ics = ["pct", "cal", "trend" if DOWN else "trendup"]
rows2 = "".join(f"""<div style="display:flex;gap:36px;align-items:flex-start;padding:38px 0;border-top:3px solid #000">
  <div style="flex:none;width:110px;height:110px;background:var(--y);border-radius:22px;display:flex;align-items:center;justify-content:center">{icon(ics[n], '#000', 62)}</div>
  <div><h2 style="font-weight:800;font-size:48px;line-height:1.1">{t}</h2><p style="font-weight:400;font-size:31px;line-height:1.35;margin-top:12px">{d}</p></div></div>"""
  for n, (t, d) in enumerate(items))
T[f"{SLUG}_03_carousel-4x5_2-icerik"] = P(1080, 1350, "w", f"""
{head('yatay_beyaz-zemin', N, 1, h=84, ml=0)}
<div style="padding:0 64px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y)">NE ANLAMA GELİYOR?</span>
  <div style="margin-top:40px">{rows2}</div>
</div>
{footer('fk', 120, addr=False)}""")

mx = TABLE[-1][1]
brows = "".join(f"""<div style="display:grid;grid-template-columns:180px 1fr 262px;align-items:center;gap:22px;padding:12px 0;border-bottom:3px solid #000">
  <div style="font-weight:600;font-size:32px">{tl(a)} TL</div>
  <div style="display:flex;height:44px;border-radius:8px;overflow:hidden;background:rgba(0,0,0,.08)">
    <div style="width:{a/mx*100:.1f}%;background:#000"></div>
    <div style="width:{(b-a)/mx*100:.1f}%;background:#fff"></div>
  </div>
  <div style="text-align:right;white-space:nowrap"><div style="font-weight:900;font-size:34px">{tl(b)} TL</div><div style="font-weight:600;font-size:21px;opacity:.7;margin-top:2px">+{tl(b-a)} TL artış</div></div></div>""" for a, b in TABLE)
T[f"{SLUG}_03_carousel-4x5_3-hesaplama"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', N, 2, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:64px">
  <span class="tag" style="background:#000;color:var(--y)">KİRA HESAPLAMA</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.0;margin-top:30px">Yeni kiranız<br>ne kadar olacak?</h1>
  <div style="display:inline-flex;align-items:center;gap:14px;margin:30px 0 26px;background:#000;color:#fff;border-radius:14px;padding:16px 26px;font-size:32px;font-weight:700">Mevcut kira <span style="color:var(--y)">×</span> <span style="color:var(--y);font-weight:900">{MULT}</span></div>
  <div style="display:flex;gap:30px;font-size:22px;font-weight:700;letter-spacing:.06em;margin-bottom:6px;padding-bottom:14px;border-bottom:3px solid #000">
    <span style="display:flex;align-items:center;gap:10px"><i style="width:22px;height:22px;background:#000;display:inline-block;border-radius:4px"></i>MEVCUT KİRA</span>
    <span style="display:flex;align-items:center;gap:10px"><i style="width:22px;height:22px;background:#fff;display:inline-block;border-radius:4px"></i>ARTIŞ</span>
    <span style="margin-left:auto">YENİ KİRA</span></div>
  {brows}
  <p style="font-weight:400;font-size:23px;line-height:1.4;margin-top:20px;opacity:.85">Azami %{RATE} uygulanmıştır; taraflar daha düşük bir artışta anlaşabilir.</p>
</div>
{footer('fk', 110, addr=False)}""")

T[f"{SLUG}_03_carousel-4x5_4-trend"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, 3, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:80px">
  <span class="tag" style="background:var(--y);color:#000">SON 12 AY</span>
  <h1 style="font-weight:900;font-size:84px;line-height:1.0;margin-top:34px">Kira artış tavanı<br><span style="color:var(--y)">{"yükselişte." if R > L12[0]["oran"] else "düşüşte."}</span></h1>
  <p style="font-weight:400;font-size:32px;margin-top:22px;opacity:.85">{L12[0]['ay']} {L12[0]['yil']} {pct(L12[0]['oran'])} → {AY} {YIL} {pct(R)}</p>
</div>
<div style="margin-top:auto;padding:0 34px 70px">{line_chart(L12, 1012, 560, line='#F3BD48', txt='#fff', hi='#F3BD48', grid='rgba(255,255,255,.14)', fs=24, dotbg='#000', show_all=False)}</div>""")

T[f"{SLUG}_04_story-9x16_1-oran"] = P(1080, 1920, "k", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:120px;margin-left:-12px"></div>
<div style="padding:0 80px;margin-top:90px">
  <span class="tag" style="background:var(--y);color:#000">TÜİK · {up(SA['tarih'])}</span>
  <h1 style="font-weight:900;font-size:104px;line-height:.98;margin-top:40px">{AY} ayı<br>kira artış oranı</h1>
</div>
<div style="position:relative;display:flex;justify-content:center;margin-top:40px">
  {gauge(R, 920)}
  <div style="position:absolute;left:0;right:0;top:250px;text-align:center">
    <div class="rate" style="font-size:210px;color:var(--y)"><small>%</small>{RATE}</div>
  </div>
</div>
<div style="display:flex;justify-content:center;margin-top:0">{delta('#F3BD48', '#000', 32)}</div>
<div style="padding:0 44px;margin-top:40px">{line_chart(L12, 992, 330, line='#F3BD48', txt='#fff', hi='#F3BD48', grid='rgba(255,255,255,.14)', fs=22, dotbg='#000')}</div>
<div style="margin-top:auto;height:200px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:40px;letter-spacing:.02em">Yeni kiranızı hesaplayın →</div>""")

CAPTION = f"""{AY} ayı kira artış oranı açıklandı: %{RATE} 📊
{AY} ayında sözleşmesi yenilenen konut ve iş yerlerinde kiraya en fazla %{RATE} zam yapılabilir. Kiranızın yeni tutarını ve bölgedeki güncel kira değerlerini öğrenmek için bizi arayın.
☎ {PHONE}
#kiraartışoranı #{AY.lower()}{YIL} #gaziosmanpaşa #altınemlak #altinemlakgop"""

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else KIT / "out_kira") / FOLDER
    render(T, out)
    (out / "aciklama.txt").write_text(CAPTION, encoding="utf-8")
    print("FOLDER", out)
