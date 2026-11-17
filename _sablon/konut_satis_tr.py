"""Türkiye odaklı aylık konut satış seti (İstanbul/GOP verisi olmadan) — Altın Emlak Gaziosmanpaşa.
Kullanım: python3 konut_satis_tr.py <çıktı_klasörü>   (veri: konut_satis_tr_veri.json)
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import page, footer, dots, logo, render, PH, PHONE, IG, ADDR
from grafik import *
from grafik import hero_cover, HERO_CSS, insight_slide

KIT = pathlib.Path(__file__).parent
D = json.loads((KIT / "konut_satis_tr_veri.json").read_text(encoding="utf-8"))
AY, YIL = D["donem"]["ay"], D["donem"]["yil"]
TR, YB = D["turkiye"], D["ybb"]
TRM = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
SLUG = f"konut-satis-{AY.translate(TRM).lower()}-{YIL}"
FOLDER = f"Konut Satış {AY} {YIL} Türkiye"
PREVM = AYLAR[(AYLAR.index(AY) - 1) % 12]
YR = D["yorumlar"]
NN = 1 + len(YR) + 3 + 1
GRUP = "KONUT SATIŞLARI"

EX = CSS + ".big{font-weight:900;line-height:.9;letter-spacing:-.02em}"
CSSX = EX + HERO_CSS
def P(w, h, cls, inner): return page(w, h, cls, inner, CSSX)
def head(lg, i=None, tag=None, h=110, ml=-12, col=""):
    right = (f'<span class="tag" style="background:#000;color:var(--y)">{tag}</span>' if tag
             else f'<span style="{col}">{dots(NN, i)}</span>')
    return (f'<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">'
            f'<img src="{logo(lg)}" style="height:{h}px;margin-left:{ml}px">{right}</div>')

LY = f"{ab(AY)} {str(YIL-1)[2:]}"
G3 = [("Toplam", [(LY, TR["gecen_yil"]), (ab(PREVM), TR["onceki_ay"]), (ab(AY), TR["satis"])]),
      ("İlk el", [(LY, TR["ilk_el_gecen_yil"]), (ab(PREVM), TR["ilk_el_onceki_ay"]), (ab(AY), TR["ilk_el"])]),
      ("İkinci el", [(LY, TR["ikinci_el_gecen_yil"]), (ab(PREVM), TR["ikinci_el_onceki_ay"]), (ab(AY), TR["ikinci_el"])])]
mchg = (TR["satis"] / TR["onceki_ay"] - 1) * 100
kred = TR["ipotekli"] / TR["satis"] * 100
ilk_pay = TR["ilk_el"] / TR["satis"] * 100
pill = 'border:3px solid #000;border-radius:999px;padding:10px 22px'

T = {}
T[f"{SLUG}_01_dikey-4x5"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', tag='KONUT SATIŞLARI', h=118, ml=-14)}
<div style="padding:0 64px;margin-top:56px">
  <h1 style="font-weight:900;font-size:66px;line-height:1.02">{AY} {YIL}'de Türkiye'de<br>satılan konut</h1>
  <div class="big" style="font-size:210px;margin-top:20px">{thou(TR['satis'])}</div>
  <div style="margin-top:22px">{badge(TR['yillik_degisim'], 'geçen yılın aynı ayına göre', '#000', Y, 28)}</div>
</div>
<div style="padding:0 64px;margin-top:60px;display:grid;grid-template-columns:1fr 1fr;gap:22px">
  {card('İLK EL', thou(TR['ilk_el']), chg(TR['ilk_el_yillik']) + ' yıllık', dark=True)}
  {card('İKİNCİ EL', thou(TR['ikinci_el']), chg(TR['ikinci_el_yillik']) + ' yıllık', dark=True, accent=True)}
</div>
<div style="padding:0 64px;margin-top:30px;display:flex;gap:16px;font-size:24px;font-weight:700">
  <span style="{pill}">Aylık {pct(mchg,1,True)}</span>
  <span style="{pill}">Kredili %{num(kred)}</span>
  <span style="{pill}">Ocak–{AY} {pct(YB['toplam_degisim'],1,True)}</span>
</div>
{footer('fk', 150)}""")

pages = {}
pages["01-kapak"] = page(1080, 1350, "k", hero_cover(1080, 1350, logo('yatay_siyah-zemin'),
    f'<span style="color:var(--y)">{dots(NN, 0)}</span>',
    f'{AY} ayında<br><span>kaç konut</span><br>satıldı?',
    thou(TR['satis']), f"İlk el {thou(TR['ilk_el'])} · İkinci el {thou(TR['ikinci_el'])}",
    ["KONUT", "SATIŞI"], f"TÜİK · {up(AY)}", badge(TR['yillik_degisim'], 'yıllık', Y, '#000', 28),
    down=TR['yillik_degisim'] < 0), CSSX)
for i, y in enumerate(YR):
    pages[f"{i+2:02d}-tespit-{i+1}"] = insight_slide(page, CSSX, logo, dots, footer, i + 1, NN, y, GRUP, i + 1, len(YR), dark=(i % 2 == 0))
b = len(YR) + 2

pages[f"{b:02d}-karsilastirma"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', b - 1, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">TÜRKİYE · {up(AY)} {YIL}</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">Geçen yıl, geçen ay<br>ve <span style="color:var(--y)">bu ay</span></h1>
</div>
<div style="padding:0 34px;margin-top:50px">{bars3(G3, 1012, 600, fs=26)}</div>
<div style="padding:0 64px;margin-top:10px;display:flex;justify-content:space-around;font-size:28px">
  <span>{chg(TR['yillik_degisim'])}</span><span>{chg(TR['ilk_el_yillik'])}</span><span>{chg(TR['ikinci_el_yillik'])}</span></div>
<div style="padding:0 64px;text-align:center;font-size:22px;opacity:.6;margin-top:8px">yıllık değişim</div>
{footer('fy', 110, addr=False)}""")

pages[f"{b+1:02d}-dagilim"] = P(1080, 1350, "w", f"""
{head('yatay_beyaz-zemin', b, h=84, ml=0)}
<div style="padding:0 64px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y)">TÜRKİYE</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">{thou(TR['satis'])} konutun<br>dağılımı</h1>
</div>
<div style="display:flex;align-items:center;gap:50px;padding:0 64px;margin-top:50px">
  {donut([('İkinci el', TR['ikinci_el'], '#000'), ('İlk el', TR['ilk_el'], Y)], 430, txt='#000', center='%' + num(100-ilk_pay,0), sub='ikinci el')}
  <div style="display:flex;flex-direction:column;gap:26px;font-size:30px">
    <div><div style="display:flex;align-items:center;gap:12px;font-weight:800"><i style="width:26px;height:26px;background:#000;border-radius:6px;display:inline-block"></i>İkinci el</div><div style="font-size:52px;font-weight:900">{thou(TR['ikinci_el'])}</div></div>
    <div><div style="display:flex;align-items:center;gap:12px;font-weight:800"><i style="width:26px;height:26px;background:var(--y);border-radius:6px;display:inline-block"></i>İlk el</div><div style="font-size:52px;font-weight:900">{thou(TR['ilk_el'])}</div></div>
  </div>
</div>
<div style="margin:56px 64px 0;background:var(--y);border-radius:20px;padding:30px 34px;display:flex;align-items:center;gap:28px">
  <div style="flex:none;width:96px;height:96px;background:#000;border-radius:20px;display:flex;align-items:center;justify-content:center">{icon('bank', Y, 58)}</div>
  <div><div style="font-size:24px;font-weight:800;letter-spacing:.08em">KREDİLİ (İPOTEKLİ) SATIŞ</div>
  <div style="font-size:50px;font-weight:900">{thou(TR['ipotekli'])} <span style="font-size:30px;font-weight:600">· satışların %{num(kred)}'i</span></div></div>
</div>
{footer('fk', 110, addr=False)}""")

ROWS = [("Toplam", YB["toplam"], YB["toplam_degisim"], True),
        ("İkinci el", YB["ikinci_el"], YB["ikinci_el_degisim"], False),
        ("İlk el", YB["ilk_el"], YB["ilk_el_degisim"], False),
        ("Kredili", YB["ipotekli"], YB["ipotekli_degisim"], False)]
pages[f"{b+2:02d}-yilbasindan"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', b + 1, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">OCAK–{up(AY)} {YIL}</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">Yılbaşından<br>bu yana satışlar</h1>
  <p style="font-size:26px;opacity:.7;margin-top:16px">Konut satış adedi · yanında geçen yılın aynı dönemine göre değişim</p>
</div>
<div style="padding:0 64px;margin-top:60px">{hbars(ROWS, 952, rh=120, fs=32, lw=200, vw=330)}</div>
{footer('fy', 110, addr=False)}""")

pages[f"{NN:02d}-kapanis"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', NN - 1, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:130px">
  <h1 style="font-weight:900;font-size:100px;line-height:1.02">Evinizi doğru fiyata satalım.</h1>
  <p style="font-weight:500;font-size:36px;line-height:1.35;margin-top:40px;max-width:900px">Güncel piyasa verileriyle evinizin değerini birlikte belirleyelim.</p>
  <div style="margin-top:64px;background:#000;color:var(--y);font-weight:900;font-size:96px;padding:30px 40px;border-radius:10px;display:inline-block">{PHONE}</div>
</div>
<div style="margin-top:auto;padding:0 64px 56px;font-weight:700;font-size:32px">{IG}<div style="font-weight:400;font-size:24px;margin-top:10px">{ADDR}</div></div>""")
for k, v in pages.items():
    T[f"{SLUG}_02_carousel-4x5_{k}"] = v

T[f"{SLUG}_03_story-9x16_1-ozet"] = P(1080, 1920, "k", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:120px;margin-left:-12px"></div>
<div style="padding:0 80px;margin-top:80px">
  <span class="tag" style="background:var(--y);color:#000">TÜİK · KONUT SATIŞLARI</span>
  <h1 style="font-weight:900;font-size:92px;line-height:1.0;margin-top:40px">{AY} {YIL}'de<br>satılan konut</h1>
  <div class="big" style="font-size:220px;color:var(--y);margin-top:30px">{thou(TR['satis'])}</div>
  <div style="margin-top:26px">{badge(TR['yillik_degisim'], 'yıllık', Y, '#000', 32)}</div>
</div>
<div style="padding:0 34px;margin-top:70px">{bars3(G3, 1012, 560, fs=27)}</div>
<div style="margin-top:auto;height:200px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:40px">Detaylar yeni gönderimizde →</div>""")

CAPTION = f"""{AY} {YIL} konut satış istatistikleri açıklandı 🏠
Türkiye genelinde {thou(TR['satis'])} konut satıldı; geçen yılın aynı ayına göre {pct(TR['yillik_degisim'],1,True)}, bir önceki aya göre {pct(mchg,1,True)}.
İlk el satışlar {pct(TR['ilk_el_yillik'],1,True)}, ikinci el satışlar {pct(TR['ikinci_el_yillik'],1,True)}. Kredili satışlar {AY} ayında {pct(TR['ipotekli_yillik'],1,True)} olsa da Ocak–{AY} döneminde {pct(YB['ipotekli_degisim'])} artıda.
Yılbaşından bu yana {thou(YB['toplam'])} konut el değiştirdi ({pct(YB['toplam_degisim'],1,True)}).
Evinizin bugünkü piyasa değerini öğrenmek için bizi arayın.
☎ {PHONE}
Kaynak: TÜİK Konut ve İş Yeri Satış İstatistikleri, {AY} {YIL}
#konutsatışları #gaziosmanpaşa #istanbulemlak #altınemlak #altinemlakgop"""

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else KIT / "out") / FOLDER
    render(T, out)
    (out / "aciklama.txt").write_text(CAPTION, encoding="utf-8")
    print("FOLDER", out)
