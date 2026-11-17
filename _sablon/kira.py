"""Kasım 2026 kira artış oranı seti — _sablon/build.py kiti ile."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import page, footer, dots, logo, render, PH, IGI, PIN, PHONE, IG, ADDR

RATE = "31,23"
TREND = [("HAZ", 32.24), ("TEM", 32.03), ("AĞU", 31.90), ("EYL", 31.79), ("EKİ", 31.49), ("KAS", 31.23)]
TABLE = [(15000, 19684.50), (20000, 26246.00), (25000, 32807.50), (30000, 39369.00), (40000, 52492.00)]

def tl(v):
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s[:-3] if s.endswith(",00") else s

def pct(v): return f"%{v:.2f}".replace(".", ",")

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
"""

def P(w, h, cls, inner): return page(w, h, cls, inner, EXTRA)

def head(lg, n=None, i=None, tag=None, tagstyle="background:#000;color:var(--y)", h=110, ml=-12, col=""):
    right = f'<span class="tag" style="{tagstyle}">{tag}</span>' if tag else (f'<span style="{col}">{dots(n, i)}</span>' if n else "")
    return (f'<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">'
            f'<img src="{logo(lg)}" style="height:{h}px;margin-left:{ml}px">{right}</div>')

def bars(maxh, on_color, off_color, txt):
    lo, hi = 30.7, 32.3
    out = ""
    for k, (m, v) in enumerate(TREND):
        on = k == len(TREND) - 1
        hh = int((v - lo) / (hi - lo) * maxh)
        c = on_color if on else off_color
        out += (f'<div class="bar"><div class="v" style="color:{on_color if on else txt}">{pct(v)}</div>'
                f'<div style="width:100%;height:{hh}px;background:{c}"></div>'
                f'<div class="m" style="color:{on_color if on else txt}">{m}</div></div>')
    return f'<div class="bars">{out}</div>'

def table(head_bg="#000", head_fg="var(--y)"):
    rows = "".join(f'<tr><td>{tl(a)} TL</td><td>+{tl(b-a)} TL</td><td class="n">{tl(b)} TL</td></tr>' for a, b in TABLE)
    return (f'<table><tr style="background:{head_bg};color:{head_fg}"><th>MEVCUT KİRA</th><th>ARTIŞ</th><th>YENİ KİRA</th></tr>{rows}</table>')

T = {}

# ---- 4:5 tekil post (sarı) ----
T["kira-kasim_01_dikey-4x5"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', tag='KİRA ARTIŞI', h=118, ml=-14)}
<div style="padding:0 64px;margin-top:100px">
  <div style="width:120px;height:14px;background:#000;margin-bottom:40px"></div>
  <h1 style="font-weight:900;font-size:92px;line-height:1.0">Kasım ayı kira artış oranı açıklandı</h1>
  <div class="rate" style="font-size:300px;margin-top:40px"><small>%</small>{RATE}</div>
  <p style="font-weight:500;font-size:34px;line-height:1.35;margin-top:30px;max-width:900px">Kasımda yenilenen konut ve iş yeri kira sözleşmeleri için yasal üst sınır. <span style="font-weight:400;opacity:.8">(TÜFE 12 aylık ortalama)</span></p>
</div>
{footer('fk', 160)}""")

# ---- Kare (siyah) ----
T["kira-kasim_02_kare-1x1"] = P(1080, 1080, "k", f"""
{head('yatay_siyah-zemin', h=104)}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">TÜFE 12 AYLIK ORTALAMA</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:34px">Kasım ayı kira<br>artış oranı</h1>
  <div class="rate" style="font-size:270px;color:var(--y);margin-top:26px"><small>%</small>{RATE}</div>
</div>
{footer('fy', 120, addr=False)}""")

# ---- Carousel (5 sayfa) ----
N = 5
T["kira-kasim_03_carousel-4x5_1-kapak"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, 0, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:130px">
  <span class="tag" style="background:var(--y);color:#000">KASIM 2026</span>
  <h1 style="font-weight:900;font-size:104px;line-height:.98;margin-top:40px">Kira artış<br>oranı<br>açıklandı</h1>
  <div class="rate" style="font-size:280px;color:var(--y);margin-top:40px"><small>%</small>{RATE}</div>
</div>
<div style="margin-top:auto;padding:0 64px 64px;display:flex;justify-content:flex-end;font-weight:700;font-size:32px;color:var(--y);letter-spacing:.06em">KAYDIRIN →</div>""")

items = [("En fazla %31,23 zam", "Kasımda yenilenen konut ve iş yeri sözleşmelerinde kira bu oranın üzerinde artırılamaz."),
         ("12 aylık TÜFE ortalaması", "Oran yıllık enflasyon (%29,77) değil, TÜFE'nin 12 aylık ortalamasına göre belirlenir."),
         ("Ekime göre geriledi", "Ekimde %31,49 olan tavan oran kasımda %31,23'e düştü.")]
rows = "".join(f"""<div style="display:flex;gap:36px;align-items:flex-start;padding:40px 0;border-top:3px solid #000">
  <div style="flex:none;width:96px;height:96px;background:var(--y);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:56px">{n}</div>
  <div><h2 style="font-weight:800;font-size:48px;line-height:1.1">{t}</h2><p style="font-weight:400;font-size:32px;line-height:1.35;margin-top:12px">{d}</p></div></div>"""
  for n, (t, d) in enumerate(items, 1))
T["kira-kasim_03_carousel-4x5_2-icerik"] = P(1080, 1350, "w", f"""
{head('yatay_beyaz-zemin', N, 1, h=84, ml=0)}
<div style="padding:0 64px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y)">NE ANLAMA GELİYOR?</span>
  <div style="margin-top:40px">{rows}</div>
</div>
{footer('fk', 120, addr=False)}""")

T["kira-kasim_03_carousel-4x5_3-hesaplama"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', N, 2, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:#000;color:var(--y)">KİRA HESAPLAMA</span>
  <h1 style="font-weight:900;font-size:72px;line-height:1.0;margin-top:30px">Yeni kiranız<br>ne kadar olacak?</h1>
  <p style="font-weight:500;font-size:32px;margin:18px 0 30px">Mevcut kira × 1,3123 = azami yeni kira</p>
  {table()}
  <p style="font-weight:400;font-size:24px;line-height:1.4;margin-top:24px;opacity:.85">Tabloda azami oran uygulanmıştır; taraflar daha düşük bir artışta anlaşabilir.</p>
</div>
{footer('fk', 120, addr=False)}""")

T["kira-kasim_03_carousel-4x5_4-trend"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, 3, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:90px">
  <span class="tag" style="background:var(--y);color:#000">2026 TRENDİ</span>
  <h1 style="font-weight:900;font-size:88px;line-height:1.0;margin-top:34px">Tavan oran<br><span style="color:var(--y)">6 aydır geriliyor.</span></h1>
  <p style="font-weight:400;font-size:32px;margin-top:22px;opacity:.85">Haziran %32,24 → Kasım %31,23</p>
</div>
<div style="margin-top:auto;padding:0 64px 64px">{bars(400, 'var(--y)', '#3a3a3a', '#fff')}</div>""")

T["kira-kasim_03_carousel-4x5_5-kapanis"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', N, 4, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:130px">
  <h1 style="font-weight:900;font-size:104px;line-height:1.02">Kiranızı doğru belirleyelim.</h1>
  <p style="font-weight:500;font-size:36px;line-height:1.35;margin-top:40px;max-width:900px">Yasal artış hesabı, bölgedeki güncel kira değerleri ve sözleşme yenileme için ofisimizi arayın.</p>
  <div style="margin-top:64px;background:#000;color:var(--y);font-weight:900;font-size:96px;padding:30px 40px;border-radius:10px;display:inline-block;letter-spacing:.01em">{PHONE}</div>
</div>
<div style="margin-top:auto;padding:0 64px 56px;font-weight:700;font-size:32px">{IG}<div style="font-weight:400;font-size:24px;margin-top:10px">{ADDR}</div></div>""")

# ---- Story (3 adet) ----
T["kira-kasim_04_story-9x16_1-oran"] = P(1080, 1920, "k", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:120px;margin-left:-12px"></div>
<div style="padding:0 80px;margin-top:170px">
  <span class="tag" style="background:var(--y);color:#000">TÜİK · 3 KASIM 2026</span>
  <h1 style="font-weight:900;font-size:120px;line-height:.98;margin-top:44px">Kasım ayı<br>kira artış<br>oranı</h1>
  <div class="rate" style="font-size:290px;color:var(--y);margin-top:50px"><small>%</small>{RATE}</div>
  <p style="font-weight:400;font-size:38px;line-height:1.35;margin-top:44px;opacity:.9">Kasımda yenilenen kira sözleşmeleri için yasal üst sınır.</p>
</div>
<div style="margin-top:auto;height:230px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:40px;letter-spacing:.02em">Yeni kiranızı hesaplayın →</div>""")

T["kira-kasim_04_story-9x16_2-hesaplama"] = P(1080, 1920, "w", f"""
<div class="y" style="height:640px;padding:150px 80px 0">
  <img src="{logo('yatay_sari-zemin')}" style="height:120px;margin-left:-14px">
  <h1 style="font-weight:900;font-size:104px;line-height:1.0;margin-top:70px">Yeni kiranız<br>ne kadar olacak?</h1>
</div>
<div style="padding:70px 80px 0">
  <p style="font-weight:700;font-size:40px;margin-bottom:40px">Mevcut kira × 1,3123</p>
  {table()}
  <p style="font-weight:400;font-size:28px;line-height:1.4;margin-top:30px;opacity:.8">Azami %31,23 artış uygulanmıştır.</p>
</div>
<div style="margin-top:auto;height:190px;background:#000;color:var(--y);display:flex;align-items:center;justify-content:center;gap:16px;font-weight:800;font-size:44px;stroke:var(--y)"><span style="display:inline-flex;width:46px">{PH}</span>{PHONE}</div>""")

T["kira-kasim_04_story-9x16_3-iletisim"] = P(1080, 1920, "w", f"""
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

if __name__ == "__main__":
    render(T, sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "out_kira")
