"""Altın Emlak Gaziosmanpaşa — sosyal medya şablon üretici (HTML -> PNG)."""
import sys, pathlib
from playwright.sync_api import sync_playwright

KIT = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else KIT / "out")
OUT.mkdir(parents=True, exist_ok=True)

PHONE = "0212 615 43 72"
IG = "@altinemlakgop"
ADDR = "Sarıgöl Mah. Mezarlık Sk. D1 Blok No:112A TOKİ Konutları, Gaziosmanpaşa / İstanbul"

def logo(name): return (KIT / "logo" / f"{name}.png").as_uri()

FONTS = "".join(
    f"@font-face{{font-family:Canaro;src:url('{(KIT/'fonts'/f).as_uri()}');font-weight:{w}}}"
    for f, w in [("Canaro-Light.otf",300),("Canaro-Book.otf",400),("Canaro-Medium.otf",500),
                 ("Canaro-Bold.otf",700),("Canaro-ExtraBold.otf",800),("Canaro-Black.otf",900)])

BASE = FONTS + """
:root{--y:#F3BD48;--k:#000;--w:#fff;--g:#808080}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Canaro,sans-serif;-webkit-font-smoothing:antialiased}
.c{position:relative;overflow:hidden;display:flex;flex-direction:column}
.y{background:var(--y);color:var(--k)} .k{background:var(--k);color:var(--w)} .w{background:var(--w);color:var(--k)}
.tag{display:inline-block;font-weight:800;letter-spacing:.14em;font-size:26px;padding:12px 22px;border-radius:6px}
.foot{margin-top:auto;display:flex;flex-direction:column;justify-content:center;gap:10px;padding:0 64px}
.foot .row{display:flex;align-items:center;gap:36px;font-weight:700;font-size:32px;letter-spacing:.02em}
.foot .it{display:flex;align-items:center;gap:14px}
.foot svg{width:34px;height:34px}
.foot .addr{font-weight:400;font-size:21px;opacity:.85;letter-spacing:.01em}
.fk{background:var(--k);color:var(--w)} .fk svg{stroke:var(--y)}
.fy{background:var(--y);color:var(--k)} .fy svg{stroke:var(--k)}
.dots{display:flex;gap:10px} .dots i{width:14px;height:14px;border-radius:7px;background:currentColor;opacity:.25} .dots i.on{opacity:1;width:40px}
"""

PH = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
IGI = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r=".6"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>'

def footer(style="fk", h=150, addr=True):
    a = f'<div class="addr">{ADDR}</div>' if addr else ""
    return (f'<div class="foot {style}" style="height:{h}px"><div class="row">'
            f'<span class="it">{PH}{PHONE}</span><span class="it">{IGI}{IG}</span></div>{a}</div>')

def dots(n, i):
    return '<div class="dots">' + "".join(f'<i class="{"on" if j==i else ""}"></i>' for j in range(n)) + '</div>'

def page(w, h, cls, inner, extra=""):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{extra}</style></head>"
            f"<body><div class='c {cls}' style='width:{w}px;height:{h}px'>{inner}</div></body></html>")

# ---------------- ÖRNEK ŞABLONLAR ----------------
T = {}

# 1) 4:5 — Bilgi postu (sarı zemin)
T["01_dikey-4x5_bilgi"] = page(1080, 1350, "y", f"""
<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">
  <img src="{logo('yatay_sari-zemin')}" style="height:118px;margin-left:-14px">
  <span class="tag" style="background:#000;color:var(--y)">BİLGİ</span>
</div>
<div style="padding:0 64px;margin-top:130px">
  <div style="width:120px;height:14px;background:#000;margin-bottom:44px"></div>
  <h1 style="font-weight:900;font-size:112px;line-height:1.0;letter-spacing:-.01em">Ev alırken tapuda nelere dikkat etmeli?</h1>
  <p style="font-weight:500;font-size:38px;line-height:1.35;margin-top:44px;max-width:860px">Satış öncesi kontrol etmeniz gereken üç kritik başlığı derledik.</p>
</div>
{footer('fk', 160)}""")

# 2) Kare — Çağrı postu (siyah zemin)
T["02_kare-1x1_cagri"] = page(1080, 1080, "k", f"""
<div style="padding:60px 64px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:104px;margin-left:-12px"></div>
<div style="padding:0 64px;margin-top:96px">
  <h1 style="font-weight:900;font-size:100px;line-height:1.02;color:var(--y)">Evinizi satmak mı istiyorsunuz?</h1>
  <p style="font-weight:400;font-size:38px;line-height:1.35;margin-top:34px;max-width:820px">Gaziosmanpaşa'da doğru fiyat ve doğru alıcı için bizi arayın.</p>
  <div style="display:inline-flex;align-items:center;gap:18px;margin-top:56px;background:var(--y);color:#000;font-weight:800;font-size:36px;padding:22px 34px;border-radius:8px;stroke:#000"><span style="display:inline-flex;width:38px">{PH}</span>{PHONE}</div>
</div>
{footer('fy', 120, addr=False)}""")

# 3) Story — İletişim kartı (beyaz + sarı)
T["03_story-9x16_iletisim"] = page(1080, 1920, "w", f"""
<div class="y" style="height:880px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding-top:120px">
  <img src="{logo('dikey_sari-zemin')}" style="width:640px">
</div>
<div style="padding:90px 80px 0;flex:1">
  <div class="tag" style="background:#000;color:var(--y)">BİZE ULAŞIN</div>
  <h1 style="font-weight:900;font-size:96px;line-height:1.02;margin-top:36px">Ofisimize<br>bekleriz.</h1>
  <div style="margin-top:56px;display:flex;flex-direction:column;gap:34px;font-size:40px">
    <div style="display:flex;gap:22px;align-items:center;font-weight:800;font-size:56px"><span style="display:inline-flex;width:56px;stroke:#000">{PH}</span>{PHONE}</div>
    <div style="display:flex;gap:22px;align-items:center;font-weight:700"><span style="display:inline-flex;width:48px;stroke:#000">{IGI}</span>{IG}</div>
    <div style="display:flex;gap:22px;align-items:flex-start;font-weight:400;font-size:33px;line-height:1.35"><span style="display:inline-flex;flex:none;width:48px;stroke:#000">{PIN}</span>Sarıgöl Mah. Mezarlık Sk.<br>D1 Blok No:112A TOKİ Konutları<br>Gaziosmanpaşa / İstanbul</div>
  </div>
</div>
<div style="height:170px;background:#000;color:var(--y);display:flex;align-items:center;justify-content:center;font-weight:500;font-size:26px;letter-spacing:.04em">Her Ofis Özel Yetkili Bir Emlak İşletmesidir.</div>""", ".c svg{width:100%;height:auto}")

# 4) Carousel — 3 sayfa 4:5
T["04_carousel-4x5_1-kapak"] = page(1080, 1350, "k", f"""
<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">
  <img src="{logo('yatay_siyah-zemin')}" style="height:110px;margin-left:-12px"><span style="color:var(--y)">{dots(3,0)}</span>
</div>
<div style="padding:0 64px;margin-top:150px">
  <span class="tag" style="background:var(--y);color:#000">KONTROL LİSTESİ</span>
  <h1 style="font-weight:900;font-size:124px;line-height:.98;margin-top:40px">Tapu<br>öncesi<br><span style="color:var(--y)">3 kontrol.</span></h1>
</div>
<div style="margin-top:auto;padding:0 64px 64px;display:flex;justify-content:flex-end;font-weight:700;font-size:32px;color:var(--y);letter-spacing:.06em">KAYDIRIN →</div>""")

items = [("Tapu kaydını sorgulayın", "Malik bilgisini ve ipotek, haciz, şerh gibi kayıtları kontrol edin."),
         ("İmar ve iskânı öğrenin", "Binanın imar durumunu ve iskân belgesi olup olmadığını sorun."),
         ("Borçları netleştirin", "Emlak vergisi, aidat ve fatura borçlarını devirden önce öğrenin.")]
rows = "".join(f"""<div style="display:flex;gap:36px;align-items:flex-start;padding:40px 0;border-top:3px solid #000">
  <div style="flex:none;width:96px;height:96px;background:var(--y);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:56px">{n}</div>
  <div><h2 style="font-weight:800;font-size:48px;line-height:1.1">{t}</h2><p style="font-weight:400;font-size:32px;line-height:1.35;margin-top:12px">{d}</p></div></div>"""
  for n, (t, d) in enumerate(items, 1))
T["04_carousel-4x5_2-icerik"] = page(1080, 1350, "w", f"""
<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">
  <img src="{logo('yatay_beyaz-zemin')}" style="height:84px">{dots(3,1)}
</div>
<div style="padding:0 64px;margin-top:80px">{rows}</div>
{footer('fk', 120, addr=False)}""")

T["04_carousel-4x5_3-kapanis"] = page(1080, 1350, "y", f"""
<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">
  <img src="{logo('yatay_sari-zemin')}" style="height:118px;margin-left:-14px">{dots(3,2)}
</div>
<div style="padding:0 64px;margin-top:150px">
  <h1 style="font-weight:900;font-size:104px;line-height:1.02">Sürecin her adımında yanınızdayız.</h1>
  <p style="font-weight:500;font-size:38px;margin-top:40px">Sorularınız için ofisimizi arayın.</p>
  <div style="margin-top:70px;background:#000;color:var(--y);font-weight:900;font-size:96px;padding:30px 40px;border-radius:10px;display:inline-block;letter-spacing:.01em">{PHONE}</div>
</div>
<div style="margin-top:auto;padding:0 64px 56px;font-weight:700;font-size:32px">{IG}<div style="font-weight:400;font-size:24px;margin-top:10px">{ADDR}</div></div>""")

def render(pages, out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for name, html in pages.items():
            f = KIT / "_tmp.html"; f.write_text(html, encoding="utf-8")
            pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            pg.query_selector(".c").screenshot(path=str(out / f"{name}.png"))
            print("ok", name)
        b.close()

if __name__ == "__main__":
    render({k: T[k] for k in (sys.argv[2:] or T)}, OUT)
