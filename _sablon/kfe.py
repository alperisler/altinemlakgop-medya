"""Aylık konut fiyat endeksi (TCMB KFE) seti — Altın Emlak Gaziosmanpaşa.
Kullanım: python3 kfe.py <çıktı_klasörü>   (veri: kfe_veri.json)
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import page, footer, dots, logo, render, PH, PHONE, IG, ADDR
from grafik import *

KIT = pathlib.Path(__file__).parent
D = json.loads((KIT / "kfe_veri.json").read_text(encoding="utf-8"))
AY, YIL = D["donem"]["ay"], D["donem"]["yil"]
TR, IST, B = D["turkiye"], D["istanbul"], D["istanbul_birim"]
H12 = D["gecmis"][-12:]
TRM = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
SLUG = f"konut-fiyat-{AY.translate(TRM).lower()}-{YIL}"
FOLDER = f"Konut Fiyat Endeksi {AY} {YIL}"
AMORT = B["fiyat_m2"] / (B["kira_m2"] * 12)
LBL = [ab(x["ay"]) for x in H12]

EX = CSS
def P(w, h, cls, inner): return page(w, h, cls, inner, EX)
def head(lg, n=None, i=None, tag=None, h=110, ml=-12, col=""):
    right = (f'<span class="tag" style="background:#000;color:var(--y)">{tag}</span>' if tag
             else (f'<span style="{col}">{dots(n, i)}</span>' if n else ""))
    return (f'<div style="padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">'
            f'<img src="{logo(lg)}" style="height:{h}px;margin-left:{ml}px">{right}</div>')

def two_lines(W, H, fs=24, txt="#fff", dotbg="#000", grid="rgba(255,255,255,.14)"):
    return lines(LBL, [("İstanbul", [x["ist"] for x in H12], Y), ("Türkiye", [x["tr"] for x in H12], "#ffffff" if txt == "#fff" else "#000")],
                 W, H, txt=txt, fs=fs, dotbg=dotbg, grid=grid)

def reel_bars(W, H, fs=24, txt="#000"):
    vals = [x["reel"] for x in H12]; n = len(vals)
    mn = min(vals) * 1.25; top = fs * 3; bw = (W - 40) / n * .58
    out = f'<line x1="0" x2="{W}" y1="{top}" y2="{top}" stroke="{txt}" stroke-width="4"/>'
    out += f'<text x="0" y="{top - 14}" font-size="{fs*.75}" font-weight="800" fill="{txt}">0</text>'
    for i, v in enumerate(vals):
        x = 20 + i * (W - 40) / n + ((W - 40) / n - bw) / 2; h = (H - top - fs * 2.6) * v / mn; last = i == n - 1
        out += f'<rect x="{x:.1f}" y="{top}" width="{bw:.1f}" height="{h:.1f}" rx="8" fill="{"#000" if last else "rgba(0,0,0,.28)"}"/>'
        out += f'<text x="{x+bw/2:.1f}" y="{top+h+fs*1.2:.1f}" text-anchor="middle" font-size="{fs*(1 if last else .8)}" font-weight="900" fill="{txt}">{pct(v)}</text>'
        out += f'<text x="{x+bw/2:.1f}" y="{top - 14}" text-anchor="middle" font-size="{fs*.8}" font-weight="800" fill="{txt}" opacity="{1 if last else .6}">{LBL[i]}</text>'
    return f'<svg viewBox="0 0 {W} {H}" style="font-family:Canaro;width:{W}px;height:{H}px">{out}</svg>'

T = {}
T[f"{SLUG}_01_dikey-4x5"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', tag='KONUT FİYATLARI', h=118, ml=-14)}
<div style="padding:0 64px;margin-top:56px">
  <h1 style="font-weight:900;font-size:66px;line-height:1.02">{AY} {YIL}'da konut<br>fiyatları yıllık</h1>
  <div class="rate" style="font-size:230px;margin-top:24px"><small>%</small>{num(TR['yillik'])}</div>
  <div style="font-size:30px;font-weight:700;margin-top:6px">arttı · TCMB Konut Fiyat Endeksi</div>
  <div style="margin-top:22px">{badge(TR['reel_yillik'], 'reel (enflasyondan arındırılmış)', '#000', Y, 26)}</div>
</div>
<div style="padding:0 64px;margin-top:44px;display:grid;grid-template-columns:1fr 1fr;gap:22px">
  {card('İSTANBUL · YILLIK', pct(IST['yillik']), 'aylık ' + pct(IST['aylik'], 1, True), dark=True, accent=True)}
  {card('TÜRKİYE · AYLIK', pct(TR['aylik'], 1, True), 'bir önceki aya göre', dark=True)}
</div>
{footer('fk', 150)}""")

_K = len(D.get("yorumlar", []))
N = _K + 5
T[f"{SLUG}_02_carousel-4x5_1-kapak"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, 0, col='color:var(--y)')}
<div style="position:absolute;right:40px;bottom:110px">{house(Y, 330)}</div>
<div style="padding:0 64px;margin-top:110px;position:relative">
  <span class="tag" style="background:var(--y);color:#000">TCMB · {up(AY)} {YIL}</span>
  <h1 style="font-weight:900;font-size:100px;line-height:.98;margin-top:40px">Konut fiyat<br>endeksi<br>açıklandı</h1>
  <div class="rate" style="font-size:220px;color:var(--y);margin-top:40px"><small>%</small>{num(TR['yillik'])}</div>
  <div style="font-size:30px;font-weight:600;margin-top:14px;opacity:.85">yıllık artış · Türkiye</div>
</div>
<div style="margin-top:auto;padding:0 64px 64px;font-weight:700;font-size:32px;color:var(--y);letter-spacing:.06em;position:relative">KAYDIRIN →</div>""")

T[f"{SLUG}_02_carousel-4x5_2-gostergeler"] = P(1080, 1350, "w", f"""
{head('yatay_beyaz-zemin', N, 1, h=84, ml=0)}
<div style="padding:0 64px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y)">ÖNE ÇIKANLAR</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">{AY} ayında<br>konut fiyatları</h1>
</div>
<div style="padding:0 64px;margin-top:44px;display:grid;grid-template-columns:1fr 1fr;gap:22px">
  {card('İSTANBUL · YILLIK', pct(IST['yillik']), 'aylık ' + pct(IST['aylik'], 1, True), dark=True, accent=True)}
  {card('TÜRKİYE · YILLIK', pct(TR['yillik']), 'aylık ' + pct(TR['aylik'], 1, True), dark=False)}
  {card('YENİ KONUT', (pct(D['yeni_konut_yillik']) if D.get('yeni_konut_yillik') is not None else '—'), 'yıllık artış', dark=False)}
  {card('İKİNCİ EL KONUT', (pct(D['ikinci_el_yillik']) if D.get('ikinci_el_yillik') is not None else '—'), 'yıllık artış', dark=False)}
</div>
<div style="margin:30px 64px 0;background:var(--y);border-radius:18px;padding:24px 30px;display:flex;align-items:center;gap:22px;font-size:28px;font-weight:700">
  {icon('trend' if TR['reel_yillik'] < 0 else 'trendup', '#000', 56)}<span>Enflasyondan arındırılmış (reel) değişim: <b style="font-weight:900">{pct(TR['reel_yillik'], 1, True)}</b></span></div>
{footer('fk', 110, addr=False)}""")

T[f"{SLUG}_02_carousel-4x5_3-trend"] = P(1080, 1350, "k", f"""
{head('yatay_siyah-zemin', N, _K + 1, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">YILLIK ARTIŞ TRENDİ</span>
  <h1 style="font-weight:900;font-size:80px;line-height:1.02;margin-top:30px">İstanbul<br><span style="color:var(--y)">Türkiye'nin önünde</span></h1>
  <p style="font-size:28px;opacity:.75;margin-top:16px">Konut fiyat endeksi · yıllık % değişim</p>
</div>
<div style="margin-top:auto;padding:0 34px 80px">{two_lines(1012, 600, fs=26)}</div>""" if IST["yillik"] >= TR["yillik"] else f"""
{head('yatay_siyah-zemin', N, _K + 1, col='color:var(--y)')}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">YILLIK ARTIŞ TRENDİ</span>
  <h1 style="font-weight:900;font-size:80px;line-height:1.02;margin-top:30px">İstanbul ve<br><span style="color:var(--y)">Türkiye</span></h1>
  <p style="font-size:28px;opacity:.75;margin-top:16px">Konut fiyat endeksi · yıllık % değişim</p>
</div>
<div style="margin-top:auto;padding:0 34px 80px">{two_lines(1012, 600, fs=26)}</div>""")

T[f"{SLUG}_02_carousel-4x5_4-reel"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', N, _K + 2, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:#000;color:var(--y)">REEL DEĞİŞİM</span>
  <h1 style="font-weight:900;font-size:80px;line-height:1.02;margin-top:30px">Fiyatlar enflasyonun<br>{'altında kaldı' if TR['reel_yillik'] < 0 else 'üzerinde arttı'}</h1>
  <p style="font-size:28px;margin-top:16px;max-width:900px">Enflasyondan arındırıldığında konut fiyatlarının yıllık değişimi</p>
</div>
<div style="padding:0 64px;margin-top:60px">{reel_bars(952, 520, fs=28)}</div>
{footer('fk', 110, addr=False)}""")

T[f"{SLUG}_02_carousel-4x5_5-istanbul-m2"] = P(1080, 1350, "w", f"""
{head('yatay_beyaz-zemin', N, _K + 3, h=84, ml=0)}
<div style="padding:0 64px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y)">İSTANBUL · {up(B['donem'])}</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">Metrekare fiyatı,<br>kirası ve amortisman</h1>
</div>
<div style="padding:0 64px;margin-top:50px;display:flex;flex-direction:column;gap:24px">
  <div style="display:flex;align-items:center;gap:28px;border-top:3px solid #000;padding-top:26px">
    <div style="flex:none;width:100px;height:100px;background:var(--y);border-radius:22px;display:flex;align-items:center;justify-content:center">{icon('home','#000',60)}</div>
    <div><div style="font-size:24px;font-weight:800;letter-spacing:.08em">ORTALAMA M² SATIŞ FİYATI</div><div style="font-size:60px;font-weight:900">{thou(B['fiyat_m2'])} TL <span style="font-size:28px">{chg(B['fiyat_yillik'])} yıllık</span></div></div></div>
  <div style="display:flex;align-items:center;gap:28px;border-top:3px solid #000;padding-top:26px">
    <div style="flex:none;width:100px;height:100px;background:var(--y);border-radius:22px;display:flex;align-items:center;justify-content:center">{icon('key','#000',60)}</div>
    <div><div style="font-size:24px;font-weight:800;letter-spacing:.08em">ORTALAMA M² KİRASI</div><div style="font-size:60px;font-weight:900">{thou(B['kira_m2'])} TL <span style="font-size:28px">{chg(B['kira_yillik'])} yıllık</span></div></div></div>
  <div style="display:flex;align-items:center;gap:28px;border-top:3px solid #000;padding-top:26px">
    <div style="flex:none;width:100px;height:100px;background:#000;border-radius:22px;display:flex;align-items:center;justify-content:center">{icon('cal',Y,60)}</div>
    <div><div style="font-size:24px;font-weight:800;letter-spacing:.08em">KİRA İLE GERİ DÖNÜŞ (AMORTİSMAN)</div><div style="font-size:60px;font-weight:900">≈ {num(AMORT)} yıl</div></div></div>
</div>
<p style="padding:0 64px;font-size:21px;opacity:.6;margin-top:24px">Kaynak: TCMB değerleme verileri (çeyreklik). Amortisman = m² fiyatı ÷ (m² kirası × 12).</p>
{footer('fk', 110, addr=False)}""")

T[f"{SLUG}_02_carousel-4x5_6-kapanis"] = P(1080, 1350, "y", f"""
{head('yatay_sari-zemin', N, _K + 4, h=118, ml=-14)}
<div style="padding:0 64px;margin-top:130px">
  <h1 style="font-weight:900;font-size:100px;line-height:1.02">Evinizin bugünkü değeri ne?</h1>
  <p style="font-weight:500;font-size:36px;line-height:1.35;margin-top:40px;max-width:900px">Gaziosmanpaşa ve çevresinde güncel verilerle ücretsiz değerleme için ofisimizi arayın.</p>
  <div style="margin-top:64px;background:#000;color:var(--y);font-weight:900;font-size:96px;padding:30px 40px;border-radius:10px;display:inline-block">{PHONE}</div>
</div>
<div style="margin-top:auto;padding:0 64px 56px;font-weight:700;font-size:32px">{IG}<div style="font-weight:400;font-size:24px;margin-top:10px">{ADDR}</div></div>""")

T[f"{SLUG}_03_story-9x16_1-ozet"] = P(1080, 1920, "k", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:120px;margin-left:-12px"></div>
<div style="padding:0 80px;margin-top:80px">
  <span class="tag" style="background:var(--y);color:#000">TCMB · KONUT FİYAT ENDEKSİ</span>
  <h1 style="font-weight:900;font-size:92px;line-height:1.0;margin-top:40px">{AY} {YIL}'da konut<br>fiyatları yıllık</h1>
  <div class="rate" style="font-size:250px;color:var(--y);margin-top:30px"><small>%</small>{num(TR['yillik'])}</div>
  <div style="margin-top:26px">{badge(TR['reel_yillik'], 'reel', Y, '#000', 32)}</div>
</div>
<div style="padding:0 44px;margin-top:70px">{two_lines(992, 520, fs=26)}</div>
<div style="margin-top:auto;height:200px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:40px">İstanbul'da m² fiyatı sonraki hikâyede →</div>""")

T[f"{SLUG}_03_story-9x16_2-istanbul"] = P(1080, 1920, "w", f"""
<div class="y" style="height:640px;padding:150px 80px 0">
  <img src="{logo('yatay_sari-zemin')}" style="height:120px;margin-left:-14px">
  <h1 style="font-weight:900;font-size:100px;line-height:1.0;margin-top:70px">İstanbul'da<br>m² fiyatı</h1>
</div>
<div style="padding:70px 80px 0">
  <div class="rate" style="font-size:190px">{thou(B['fiyat_m2'])} <span style="font-size:70px">TL</span></div>
  <div style="font-size:34px;font-weight:700;margin-top:18px">{chg(B['fiyat_yillik'])} yıllık · {B['donem']}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:60px">
    {card('M² KİRASI', thou(B['kira_m2']) + ' TL', chg(B['kira_yillik']) + ' yıllık', dark=False)}
    {card('AMORTİSMAN', '≈ ' + num(AMORT) + ' yıl', 'kira ile geri dönüş', dark=True, accent=True)}
  </div>
  <div style="margin-top:34px;background:var(--y);border-radius:20px;padding:30px 34px;display:flex;align-items:center;gap:26px">
    <div style="flex:none;width:96px;height:96px;background:#000;border-radius:20px;display:flex;align-items:center;justify-content:center">{icon('pct', Y, 56)}</div>
    <div><div style="font-size:24px;font-weight:800;letter-spacing:.08em">BRÜT KİRA GETİRİSİ</div><div style="font-size:56px;font-weight:900">≈ %{num(100/AMORT)} <span style="font-size:28px;font-weight:600">yıllık</span></div></div>
  </div>
  <p style="font-size:24px;line-height:1.4;margin-top:34px;opacity:.75">Gaziosmanpaşa'daki evinizin satış ve kira değerini güncel verilerle birlikte hesaplayalım.</p>
</div>
<div style="margin-top:auto;height:200px;background:#000;color:var(--y);display:flex;align-items:center;justify-content:center;gap:16px;font-weight:800;font-size:40px;stroke:var(--y)"><span style="display:inline-flex;width:44px">{PH}</span>Ücretsiz değerleme: {PHONE}</div>""")

# ---------------- DİKKAT ÇEKİCİ KAPAK ----------------
from grafik import hero_cover, HERO_CSS
T[f"{SLUG}_02_carousel-4x5_1-kapak"] = page(1080, 1350, "k", hero_cover(1080, 1350, logo('yatay_siyah-zemin'),
    f'<span style="color:var(--y)">{dots(N, 0)}</span>',
    f'Konut<br>fiyatları<br><span>yıllık</span>',
    f'<small>%</small>{num(TR["yillik"])}', f"İstanbul'da {pct(IST['yillik'])} · Reel {pct(TR['reel_yillik'],1,True)}",
    ["FİYAT", "ENDEKSİ"], f"TCMB · {up(AY)}", badge(IST['aylik'], 'İstanbul aylık', Y, '#000', 28), down=False), EX + HERO_CSS)

EXTRA_KEYS = ['3-trend', '4-reel', '5-istanbul-m2']
LAST_KEY = '6-kapanis'
EXTRA_PAGES = len(EXTRA_KEYS)
GRUP = 'KONUT FİYATLARI'

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

CAPTION = f"""{AY} {YIL} Konut Fiyat Endeksi açıklandı 📈
Konut fiyatları Türkiye'de yıllık {pct(TR['yillik'])}, İstanbul'da {pct(IST['yillik'])} arttı. Enflasyondan arındırıldığında yıllık değişim {pct(TR['reel_yillik'],1,True)}.
Evinizin bugünkü değerini öğrenmek için ücretsiz değerleme randevusu alın.
☎ {PHONE}
Kaynak: TCMB Konut Fiyat Endeksi
#konutfiyatları #konutfiyatendeksi #gaziosmanpaşa #istanbulemlak #altınemlak #altinemlakgop"""

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else KIT / "out") / FOLDER
    render(T, out)
    (out / "aciklama.txt").write_text(CAPTION, encoding="utf-8")
    print("FOLDER", out)
