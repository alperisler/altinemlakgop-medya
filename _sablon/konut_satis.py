"""Aylık konut satış istatistikleri seti — Altın Emlak Gaziosmanpaşa.
Kullanım: python3 konut_satis.py <çıktı_klasörü>   (veri: konut_satis_veri.json)
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import page, footer, dots, logo, render, PH, PHONE, IG, ADDR
from grafik import *

KIT = pathlib.Path(__file__).parent
D = json.loads((KIT / "konut_satis_veri.json").read_text(encoding="utf-8"))
AY, YIL = D["donem"]["ay"], D["donem"]["yil"]
TR, IST, GOP = D["turkiye"], D["istanbul"], D["gop"]
TRM = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
SLUG = f"konut-satis-{AY.translate(TRM).lower()}-{YIL}"
FOLDER = f"Konut Satış {AY} {YIL}"
PREVM = AYLAR[(AYLAR.index(AY) - 1) % 12]

def lastyear(x): return x.get("gecen_yil") or x["satis"] / (1 + x["yillik_degisim"] / 100)
def mchg(x): return (x["satis"] / x["onceki_ay"] - 1) * 100

EX = CSS + """
.big{font-weight:900;line-height:.9;letter-spacing:-.02em}
"""
def P(w, h, cls, inner): return page(w, h, cls, inner, EX)
def head(lg, n=None, i=None, tag=None, h=110, ml=-12, col="", tagbg="#000", tagfg="var(--y)"):
    right = (f'<span class="tag" style="background:{tagbg};color:{tagfg}">{tag}</span>' if tag
             else (f'<span style="{col}">{dots(n, i)}</span>' if n else ""))
    return (f'<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">'
            f'<img src="{logo(lg)}" style="height:{h}px;margin-left:{ml}px">{right}</div>')

G3 = [("Türkiye", [(f"{ab(AY)} {str(YIL-1)[2:]}", lastyear(TR)), (ab(PREVM), TR["onceki_ay"]), (ab(AY), TR["satis"])]),
      ("İstanbul", [(f"{ab(AY)} {str(YIL-1)[2:]}", lastyear(IST)), (ab(PREVM), IST["onceki_ay"]), (ab(AY), IST["satis"])]),
      ("Gaziosmanpaşa", [(f"{ab(AY)} {str(YIL-1)[2:]}", lastyear(GOP)), (ab(PREVM), GOP["onceki_ay"]), (ab(AY), GOP["satis"])])]
ROWS = sorted([(k["ilce"], k["satis"], k["yillik_degisim"], False) for k in D["komsular"]] +
              [("Gaziosmanpaşa", GOP["satis"], GOP["yillik_degisim"], True)], key=lambda r: -r[1])
DIR = "azaldı" if TR["yillik_degisim"] < 0 else "arttı"

T = {}
T[f"{SLUG}_01_dikey-4x5"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', tag='KONUT SATIŞLARI', h=118, ml=-14)}
<div style="padding:0 64px;margin-top:56px">
  <h1 style="font-weight:900;font-size:66px;line-height:1.02">{AY} {YIL}'da Türkiye'de<br>satılan konut</h1>
  <div class="big" style="font-size:210px;margin-top:20px">{thou(TR['satis'])}</div>
  <div style="margin-top:22px">{badge(TR['yillik_degisim'], 'geçen yılın aynı ayına göre', '#000', Y, 28)}</div>
</div>
<div style="padding:0 64px;margin-top:60px;display:grid;grid-template-columns:1fr 1fr;gap:22px">
  {card('İSTANBUL', thou(IST['satis']), chg(IST['yillik_degisim']) + ' geçen yıla göre', dark=True)}
  {card('GAZİOSMANPAŞA', thou(GOP['satis']), chg(GOP['yillik_degisim']) + ' geçen yıla göre', dark=True, accent=True)}
</div>
<div style="padding:0 64px;margin-top:30px;display:flex;gap:16px;font-size:24px;font-weight:700">
  <span style="border:3px solid #000;border-radius:999px;padding:10px 22px">Sıfır {thou(TR['ilk_el'])}</span>
  <span style="border:3px solid #000;border-radius:999px;padding:10px 22px">İkinci el {thou(TR['ikinci_el'])}</span>
  <span style="border:3px solid #000;border-radius:999px;padding:10px 22px">Krediyle %{num(TR['ipotekli']/TR['satis']*100)}</span>
</div>
{footer('fk', 150)}""")

_K = len(D.get("yorumlar", []))
N = _K + 5
T[f"{SLUG}_02_carousel-4x5_1-kapak"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, 0, col='color:var(--y)')}
<div style="position:absolute;right:40px;bottom:110px;opacity:.95">{house(Y, 330)}</div>
<div style="padding:0 64px;margin-top:110px;position:relative">
  <span class="tag" style="background:var(--y);color:#000">TÜİK · {up(AY)} {YIL}</span>
  <h1 style="font-weight:900;font-size:100px;line-height:.98;margin-top:40px">Konut<br>satışları<br>açıklandı</h1>
  <div class="big" style="font-size:190px;color:var(--y);margin-top:40px">{thou(TR['satis'])}</div>
  <div style="font-size:30px;font-weight:600;margin-top:14px;opacity:.85">konut satıldı</div>
  <div style="margin-top:28px">{badge(TR['yillik_degisim'], 'geçen yıla göre', Y, '#000', 28)}</div>
</div>
<div style="margin-top:auto;padding:0 64px 64px;font-weight:700;font-size:32px;color:var(--y);letter-spacing:.06em;position:relative">KAYDIRIN →</div>""")

T[f"{SLUG}_02_carousel-4x5_2-karsilastirma"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, _K + 1, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">TÜRKİYE · İSTANBUL · GAZİOSMANPAŞA</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">Geçen yıl, geçen ay<br>ve <span style="color:var(--y)">bu ay</span></h1>
</div>
<div style="padding:0 34px;margin-top:50px">{bars3(G3, 1012, 600, fs=26)}</div>
<div style="padding:0 64px;margin-top:10px;display:flex;justify-content:space-around;font-size:28px">
  <span>{chg(TR['yillik_degisim'])}</span><span>{chg(IST['yillik_degisim'])}</span><span>{chg(GOP['yillik_degisim'])}</span></div>
<div style="padding:0 64px;text-align:center;font-size:22px;opacity:.6;margin-top:8px">geçen yılın aynı ayına göre değişim</div>
{footer('fy', 110, addr=False)}""")

ist_first = IST["ilk_el"] / IST["satis"] * 100
T[f"{SLUG}_02_carousel-4x5_3-istanbul"] = P(1080, 1350, "w", f"""
{head('yatay_beyaz-zemin', N, _K + 2, h=84, ml=0)}
<div style="padding:0 64px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y)">İSTANBUL</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">{thou(IST['satis'])} konutun<br>dağılımı</h1>
</div>
<div style="display:flex;align-items:center;gap:50px;padding:0 64px;margin-top:50px">
  {donut([('İkinci el', IST['ikinci_el'], '#000'), ('Sıfır', IST['ilk_el'], Y)], 430, txt='#000', center='%' + num(100-ist_first,0), sub='ikinci el')}
  <div style="display:flex;flex-direction:column;gap:26px;font-size:30px">
    <div><div style="display:flex;align-items:center;gap:12px;font-weight:800"><i style="width:26px;height:26px;background:#000;border-radius:6px;display:inline-block"></i>İkinci el</div><div style="font-size:52px;font-weight:900">{thou(IST['ikinci_el'])}</div></div>
    <div><div style="display:flex;align-items:center;gap:12px;font-weight:800"><i style="width:26px;height:26px;background:var(--y);border-radius:6px;display:inline-block"></i>Sıfır konut</div><div style="font-size:52px;font-weight:900">{thou(IST['ilk_el'])}</div></div>
  </div>
</div>
<div style="margin:56px 64px 0;background:var(--y);border-radius:20px;padding:30px 34px;display:flex;align-items:center;gap:28px">
  <div style="flex:none;width:96px;height:96px;background:#000;border-radius:20px;display:flex;align-items:center;justify-content:center">{icon('bank', Y, 58)}</div>
  <div><div style="font-size:24px;font-weight:800;letter-spacing:.08em">KREDİYLE ALINAN KONUT</div>
  <div style="font-size:50px;font-weight:900">{thou(IST['ipotekli'])} <span style="font-size:30px;font-weight:600">· satışların %{num(IST['ipotekli']/IST['satis']*100)}'i</span></div></div>
</div>
{footer('fk', 110, addr=False)}""")

T[f"{SLUG}_02_carousel-4x5_4-ilceler"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, _K + 3, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">GAZİOSMANPAŞA VE ÇEVRESİ</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">Bölgemizde<br>{AY} satışları</h1>
  <p style="font-size:26px;opacity:.7;margin-top:16px">Konut satış adedi · yanında geçen yılın aynı ayına göre değişim</p>
</div>
<div style="padding:0 64px;margin-top:44px">{hbars(ROWS, 952, rh=86, fs=30, lw=270, vw=200)}</div>
{footer('fy', 110, addr=False)}""")

T[f"{SLUG}_02_carousel-4x5_5-kapanis"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', N, _K + 4, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:130px">
  <h1 style="font-weight:900;font-size:100px;line-height:1.02">Evinizi doğru fiyata satalım.</h1>
  <p style="font-weight:500;font-size:36px;line-height:1.35;margin-top:40px;max-width:900px">Gaziosmanpaşa'daki güncel satış verileriyle evinizin değerini birlikte belirleyelim.</p>
  <div style="margin-top:64px;background:#000;color:var(--y);font-weight:900;font-size:96px;padding:30px 40px;border-radius:10px;display:inline-block">{PHONE}</div>
</div>
<div style="margin-top:auto;padding:0 64px 56px;font-weight:700;font-size:32px">{IG}<div style="font-weight:400;font-size:24px;margin-top:10px">{ADDR}</div></div>""")

T[f"{SLUG}_03_story-9x16_1-ozet"] = P(1080, 1920, "k", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:120px;margin-left:-12px"></div>
<div style="padding:0 80px;margin-top:80px">
  <span class="tag" style="background:var(--y);color:#000">TÜİK · KONUT SATIŞLARI</span>
  <h1 style="font-weight:900;font-size:92px;line-height:1.0;margin-top:40px">{AY} {YIL}'da<br>satılan konut</h1>
  <div class="big" style="font-size:220px;color:var(--y);margin-top:30px">{thou(TR['satis'])}</div>
  <div style="margin-top:26px">{badge(TR['yillik_degisim'], 'geçen yıla göre', Y, '#000', 32)}</div>
</div>
<div style="padding:0 34px;margin-top:70px">{bars3(G3, 1012, 560, fs=27)}</div>
<div style="margin-top:auto;height:200px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:40px">Bölgemizin verileri sonraki hikâyede →</div>""")

T[f"{SLUG}_03_story-9x16_2-bolge"] = P(1080, 1920, "k", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:120px;margin-left:-12px"></div>
<div style="padding:0 80px;margin-top:80px">
  <span class="tag" style="background:var(--y);color:#000">GAZİOSMANPAŞA VE ÇEVRESİ</span>
  <h1 style="font-weight:900;font-size:92px;line-height:1.0;margin-top:40px">Gaziosmanpaşa'da<br><span style="color:var(--y)">{thou(GOP['satis'])} konut</span> satıldı</h1>
  <div style="margin-top:26px">{badge(GOP['yillik_degisim'], 'geçen yıla göre', Y, '#000', 32)}</div>
</div>
<div style="padding:0 80px;margin-top:80px">{hbars(ROWS, 920, rh=118, fs=34, lw=280, vw=200)}</div>
<div style="margin-top:auto;height:200px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;gap:16px;font-weight:800;font-size:44px;stroke:#000"><span style="display:inline-flex;width:46px">{PH}</span>{PHONE}</div>""")

# ---------------- DİKKAT ÇEKİCİ KAPAK ----------------
from grafik import hero_cover, HERO_CSS
T[f"{SLUG}_02_carousel-4x5_1-kapak"] = page(1080, 1350, "k", hero_cover(1080, 1350, logo('yatay_siyah-zemin'),
    f'<span style="color:var(--y)">{dots(N, 0)}</span>',
    f'{AY} ayında<br><span>kaç konut</span><br>satıldı?',
    thou(TR['satis']), f"İstanbul {thou(IST['satis'])} · Gaziosmanpaşa {thou(GOP['satis'])}",
    ["KONUT", "SATIŞI"], f"TÜİK · {up(AY)}", badge(TR['yillik_degisim'], 'geçen yıla göre', Y, '#000', 28), down=TR['yillik_degisim'] < 0), EX + HERO_CSS)

EXTRA_KEYS = ['2-karsilastirma', '3-istanbul', '4-ilceler']
LAST_KEY = '5-kapanis'
EXTRA_PAGES = len(EXTRA_KEYS)
GRUP = 'KONUT SATIŞLARI'

# ---------------- YORUM CAROUSEL'İ (10+ sayfa) ----------------
from grafik import insight_slide
YR = D.get("yorumlar", [])
if YR:
    NN = 1 + len(YR) + EXTRA_PAGES + 1
    def _restyle(key, idx):
        return T.pop(key)
    pages = {}
    pages["01-kapak"] = T.pop(f"{SLUG}_02_carousel-4x5_1-kapak")
    for i, y in enumerate(YR):
        pages[f"{i+2:02d}-tespit-{i+1}"] = insight_slide(page, EX + HERO_CSS, logo, dots, footer, i + 1, NN, y, GRUP, i + 1, len(YR), dark=(i % 2 == 0))
    for j, k in enumerate(EXTRA_KEYS):
        pages[f"{len(YR)+2+j:02d}-{k.split('-',1)[1]}"] = T.pop(f"{SLUG}_02_carousel-4x5_{k}")
    pages[f"{NN:02d}-kapanis"] = T.pop(f"{SLUG}_02_carousel-4x5_{LAST_KEY}")
    for k in list(T):
        if "_02_carousel-4x5_" in k: T.pop(k)
    for k, v in pages.items():
        T[f"{SLUG}_02_carousel-4x5_{k}"] = v

CAPTION = f"""{AY} {YIL} konut satış istatistikleri açıklandı 🏠
Türkiye genelinde {thou(TR['satis'])} konut satıldı (geçen yılın aynı ayına göre {pct(TR['yillik_degisim'],1,True)}). İstanbul'da {thou(IST['satis'])}, Gaziosmanpaşa'da {thou(GOP['satis'])} konut satıldı.
Evinizin bugünkü piyasa değerini öğrenmek için bizi arayın.
☎ {PHONE}
Kaynak: TÜİK Konut ve İş Yeri Satış İstatistikleri
#konutsatışları #gaziosmanpaşa #istanbulemlak #altınemlak #altinemlakgop"""

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else KIT / "out") / FOLDER
    render(T, out)
    (out / "aciklama.txt").write_text(CAPTION, encoding="utf-8")
    print("FOLDER", out)
