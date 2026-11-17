"""Aylık Gaziosmanpaşa piyasa blog yazısı görselleri (16:9 + OG 1200x630).
Kullanım: python3 blog_gorsel.py <çıktı_klasörü>
Veri: blog_veri.json + konut_satis_veri.json + kfe_veri.json
"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import page, logo, render, PHONE, IG, PH
from grafik import *

KIT = pathlib.Path(__file__).parent
J = lambda f: json.loads((KIT / f).read_text(encoding="utf-8"))
B, S, K = J("blog_veri.json"), J("konut_satis_veri.json"), J("kfe_veri.json")
AY, YIL = B["ay"], B["yil"]
G = B["gop_ilan"]
GETIRI = G["kiralik_ort"] * 12 / G["satilik_ort"] * 100
AMORT = G["satilik_ort"] / (G["kiralik_ort"] * 12)
TRM = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
SLUG = f"blog-{AY.translate(TRM).lower()}-{YIL}"
FOLDER = f"Blog Görselleri {AY} {YIL}"
PHOTO = (KIT / "alper.png").as_uri()
def mtl(v): return num(v / 1e6, 1) + " milyon TL"

EX = CSS + HERO_CSS + """
.chip{display:inline-flex;flex-direction:column;background:#161616;border:2px solid #2c2c2c;border-radius:16px;padding:16px 22px;color:#fff}
.chip b{font-size:40px;font-weight:900;color:#F3BD48;line-height:1.05;white-space:nowrap}
.chip span{font-size:18px;font-weight:700;letter-spacing:.08em;opacity:.75}
.src{position:absolute;left:70px;bottom:34px;font-size:20px;opacity:.6}
"""
def P(w, h, cls, inner): return page(w, h, cls, inner, EX)

def chips(fs=1):
    gop = S["gop"]; ist = K["istanbul"]
    items = [(thou(gop["satis"]), f"GOP KONUT SATIŞI · {up(S['donem']['ay'])[:3]}"),
             (pct(ist["yillik"], 1, True), "İSTANBUL KONUT FİYATI · YILLIK"),
             (thou(G["kiralik_ort"]) + " TL", "GOP ORT. KİRA İLANI")]
    return "".join(f'<div class="chip" style="transform:scale({fs});transform-origin:left top"><b>{v}</b><span>{k}</span></div>' for v, k in items)

def author(scale=1):
    return (f'<div style="display:flex;align-items:center;gap:14px;background:#F3BD48;color:#000;border-radius:999px;padding:10px 26px 10px 12px;font-size:{22*scale:.0f}px">'
            f'<div style="width:{54*scale:.0f}px;height:{54*scale:.0f}px;border-radius:50%;background:#000 url({PHOTO}) center 12%/150% no-repeat"></div>'
            f'<div><div style="font-weight:900">Alper İşler</div><div style="font-weight:600;font-size:.8em">Gayrimenkul Danışmanı · Altın Emlak Gaziosmanpaşa</div></div></div>')

T = {}
T[f"{SLUG}_01_kapak-16x9"] = P(1600, 900, "k", f"""
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 78% 55%, rgba(243,189,72,.35), rgba(0,0,0,0) 70%),#000"></div>
{sunburst(1600, 900, 1250, 520, op=.06)}
<div style="position:absolute;right:120px;bottom:0;width:620px;height:620px;border-radius:50%;background:#F3BD48;transform:translateY(160px)"></div>
<img src="{PHOTO}" style="position:absolute;right:150px;bottom:0;height:800px">
<div style="position:absolute;left:-60px;top:40px">{''}</div>
<div style="position:relative;padding:60px 70px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:92px;margin-left:-10px"></div>
<div style="position:relative;padding:0 70px;margin-top:46px;max-width:900px">
  <span class="tag" style="background:var(--y);color:#000">PİYASA RAPORU · {up(AY)} {YIL}</span>
  <div class="hero-title" style="font-size:92px;margin-top:30px">{B['manset_ust']}<br><span>{B['manset_vurgu']}</span><br>{B['manset_alt']}</div>
  <div style="display:flex;gap:16px;margin-top:34px">{chips()}</div>
</div>
<div style="position:absolute;left:70px;bottom:46px">{author()}</div>""")

T[f"{SLUG}_02_og-1200x630"] = P(1200, 630, "k", f"""
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 60% 70% at 80% 60%, rgba(243,189,72,.35), rgba(0,0,0,0) 70%),#000"></div>
{sunburst(1200, 630, 950, 380, op=.06)}
<div style="position:absolute;right:70px;bottom:0;width:440px;height:440px;border-radius:50%;background:#F3BD48;transform:translateY(120px)"></div>
<img src="{PHOTO}" style="position:absolute;right:90px;bottom:0;height:560px">
<div style="position:relative;padding:44px 52px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:70px;margin-left:-8px"></div>
<div style="position:relative;padding:0 52px;margin-top:34px;max-width:700px">
  <span class="tag" style="background:var(--y);color:#000;font-size:20px">PİYASA RAPORU · {up(AY)} {YIL}</span>
  <div class="hero-title" style="font-size:66px;margin-top:22px">{B['manset_ust']}<br><span>{B['manset_vurgu']}</span><br>{B['manset_alt']}</div>
</div>
<div style="position:absolute;left:52px;bottom:40px">{author(.85)}</div>""")

rows = sorted([(k["ilce"], k["satis"], k["yillik_degisim"], False) for k in S["komsular"]] +
              [("Gaziosmanpaşa", S["gop"]["satis"], S["gop"]["yillik_degisim"], True)], key=lambda r: -r[1])
def chart_frame(title, sub, body, src, dark=False):
    bg = "k" if dark else "w"; fg = "#fff" if dark else "#000"
    return P(1600, 900, bg, f"""
<div style="padding:56px 70px 0;display:flex;justify-content:space-between;align-items:flex-start">
  <div><div style="font-size:22px;font-weight:800;letter-spacing:.12em;color:{'#F3BD48' if dark else '#000'};opacity:.85">{sub}</div>
  <div style="font-size:56px;font-weight:900;line-height:1.05;margin-top:10px;max-width:1100px;color:{fg}">{title}</div></div>
  <img src="{logo('yatay_siyah-zemin' if dark else 'yatay_beyaz-zemin')}" style="height:{74 if dark else 60}px"></div>
{body}
<div class="src" style="color:{fg}">{src}</div>
<div style="position:absolute;right:70px;bottom:30px;font-size:22px;font-weight:800;color:{fg}">{IG}</div>""")

T[f"{SLUG}_03_grafik-satis"] = chart_frame(
    f"Gaziosmanpaşa ve çevresinde {S['donem']['ay']} {S['donem']['yil']} konut satışları",
    "GRAFİK 1 · İLÇE KARŞILAŞTIRMASI",
    f'<div style="padding:0 70px;margin-top:50px">{hbars(rows, 1460, rh=82, fs=30, lw=300, vw=220, txt="#000", muted="#d6d6d6", hi="#000")}</div>'
    f'<div style="position:absolute;right:70px;top:250px;font-size:20px;opacity:.6">sağdaki oran: geçen yılın aynı ayına göre</div>',
    "Kaynak: TÜİK Konut ve İş Yeri Satış İstatistikleri (İşlerOS)")

H = K["gecmis"][-12:]
T[f"{SLUG}_04_grafik-fiyat"] = chart_frame(
    "Konut fiyatlarında yıllık artış: İstanbul ve Türkiye",
    "GRAFİK 2 · KONUT FİYATLARI (TCMB)",
    f'<div style="padding:40px 70px 0">{lines([ab(x["ay"]) for x in H], [("İstanbul", [x["ist"] for x in H], Y), ("Türkiye", [x["tr"] for x in H], "#fff")], 1460, 540, fs=28)}</div>',
    f"Kaynak: TCMB Konut Fiyat Endeksi · geçen yılın aynı ayına göre % artış · son dönem {K['donem']['ay']} {K['donem']['yil']}", dark=True)

def bigcard(icn, k, v, sub, dark=False):
    bg = "#000" if dark else "#fff"; fg = "#F3BD48" if dark else "#000"
    return (f'<div style="background:{bg};border:4px solid #000;border-radius:24px;padding:34px 34px;display:flex;flex-direction:column;gap:16px">'
            f'<div style="width:86px;height:86px;border-radius:20px;background:{"#F3BD48" if not dark else "#F3BD48"};display:flex;align-items:center;justify-content:center">{icon(icn, "#000", 52)}</div>'
            f'<div style="font-size:22px;font-weight:800;letter-spacing:.1em;color:{"#fff" if dark else "#000"}">{k}</div>'
            f'<div style="font-size:50px;font-weight:900;line-height:1.05;color:{fg}">{v}</div>'
            f'<div style="font-size:22px;font-weight:600;color:{"#fff" if dark else "#000"};opacity:.8">{sub}</div></div>')
T[f"{SLUG}_05_grafik-kira-getiri"] = P(1600, 900, "y", f"""
<div style="padding:56px 70px 0;display:flex;justify-content:space-between;align-items:flex-start">
  <div><div style="font-size:22px;font-weight:800;letter-spacing:.12em">GRAFİK 3 · GAZİOSMANPAŞA İLAN PİYASASI · {up(G['donem'])}</div>
  <div style="font-size:56px;font-weight:900;line-height:1.05;margin-top:10px">Satılık ve kiralık ilanlar ne söylüyor?</div></div>
  <img src="{logo('yatay_sari-zemin')}" style="height:80px"></div>
<div style="padding:0 70px;margin-top:44px;display:grid;grid-template-columns:repeat(4,1fr);gap:26px">
  {bigcard('home', 'SATILIK İLAN ORTALAMASI', mtl(G['satilik_ort']), pct(G['satilik_degisim'],1,True) + ' geçen aya göre')}
  {bigcard('key', 'KİRALIK İLAN ORTALAMASI', thou(G['kiralik_ort']) + ' TL', pct(G['kiralik_degisim'],1,True) + ' geçen aya göre')}
  {bigcard('pct', 'BRÜT KİRA GETİRİSİ', '≈ %' + num(GETIRI), 'yıllık kira ÷ satış fiyatı', dark=True)}
  {bigcard('cal', 'AMORTİSMAN', '≈ ' + num(AMORT) + ' yıl', 'kira ile geri dönüş', dark=True)}
</div>
<div style="margin:30px 70px 0;background:#000;color:#fff;border-radius:20px;padding:24px 32px;display:flex;align-items:center;gap:24px;font-size:28px;font-weight:700">
  {icon('pin', Y, 50)}<span>Karşılaştırma: İstanbul ortalamasında kiradan yıllık kazanç <b style="color:#F3BD48">≈ %{num(K['istanbul_birim']['kira_m2']*12/K['istanbul_birim']['fiyat_m2']*100)}</b>, ev kendini kirayla <b style="color:#F3BD48">≈ {num(K['istanbul_birim']['fiyat_m2']/(K['istanbul_birim']['kira_m2']*12))} yılda</b> öder <span style="opacity:.6;font-weight:500">(TCMB, {K['istanbul_birim']['donem']})</span></span></div>
<div class="src">Kaynak: İşlerOS ilan verileri (ilan fiyatlarıdır, gerçekleşen satış fiyatı değildir).</div>
<div style="position:absolute;right:70px;bottom:30px;font-size:22px;font-weight:800">☎ {PHONE}</div>""")

# ---------------- INSTAGRAM SÜRÜMLERİ (4:5 carousel + 9:16 hikâye) ----------------
from build import dots, footer, ADDR
NIG = 12
def ighead(lg, i, dark=True):
    return (f'<div style="position:relative;padding:72px 64px 0;display:flex;justify-content:space-between;align-items:center">'
            f'<img src="{logo(lg)}" style="height:{110 if lg != "yatay_beyaz-zemin" else 84}px;margin-left:-12px">'
            f'<span style="color:{"var(--y)" if dark else "#000"}">{dots(NIG, i)}</span></div>')

T[f"{SLUG}_10_ig-carousel-4x5_1-kapak"] = P(1080, 1350, "k", f"""
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 55% at 70% 75%, rgba(243,189,72,.35), rgba(0,0,0,0) 70%),#000"></div>
{sunburst(1080, 1350, 760, 1000, op=.07)}
<div style="position:absolute;right:-60px;bottom:-200px;width:760px;height:760px;border-radius:50%;background:#F3BD48"></div>
<img src="{PHOTO}" style="position:absolute;right:-40px;bottom:0;height:820px">
<div style="position:absolute;left:270px;top:665px">{sticker(["PİYASA", "RAPORU"], f"{up(AY)} {YIL}", 190, -10)}</div>
{ighead('yatay_siyah-zemin', 0)}
<div style="position:relative;padding:0 64px;margin-top:110px">
  <div style="font-size:30px;font-weight:800;letter-spacing:.1em;color:#F3BD48">GAZİOSMANPAŞA · {up(AY)} {YIL}</div>
  <div class="hero-title" style="font-size:100px;max-width:760px;margin-top:16px">{B['manset_ust']}<br><span>{B['manset_vurgu']}</span><br>{B['manset_alt']}</div>
</div>
<div style="position:absolute;left:64px;bottom:150px;display:flex;flex-direction:column;gap:14px">{chips()}</div>
<div style="position:absolute;left:-40px;right:-40px;bottom:40px;height:90px;background:#F3BD48;transform:rotate(-3deg);display:flex;align-items:center;justify-content:space-between;padding:0 104px;color:#000;font-weight:900;font-size:32px;letter-spacing:.08em"><span>ALPER İŞLER</span><span>KAYDIRIN →</span></div>""")

T[f"{SLUG}_10_ig-carousel-4x5_2-satis"] = P(1080, 1350, "k", f"""
{ighead('yatay_siyah-zemin', 9)}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">KONUT SATIŞLARI · {up(S['donem']['ay'])} {S['donem']['yil']}</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">Gaziosmanpaşa'da<br><span style="color:var(--y)">{thou(S['gop']['satis'])} konut</span> satıldı</h1>
  <p style="font-size:26px;opacity:.7;margin-top:16px">Komşu ilçelerle karşılaştırma · geçen yılın aynı ayına göre değişim</p>
</div>
<div style="padding:0 64px;margin-top:44px">{hbars(rows, 952, rh=86, fs=30, lw=270, vw=200)}</div>
{footer('fy', 110, addr=False)}""")

T[f"{SLUG}_10_ig-carousel-4x5_3-fiyat"] = P(1080, 1350, "k", f"""
{ighead('yatay_siyah-zemin', 10)}
<div style="padding:0 64px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">KONUT FİYATLARI · TCMB</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">İstanbul'da fiyatlar<br>yıllık <span style="color:var(--y)">{pct(K['istanbul']['yillik'])}</span> arttı</h1>
  <p style="font-size:26px;opacity:.7;margin-top:16px">Konut fiyatları · geçen yılın aynı ayına göre % artış</p>
</div>
<div style="margin-top:auto;padding:0 34px 80px">{lines([ab(x["ay"]) for x in H], [("İstanbul", [x["ist"] for x in H], Y), ("Türkiye", [x["tr"] for x in H], "#fff")], 1012, 600, fs=26)}</div>""")

T[f"{SLUG}_10_ig-carousel-4x5_4-kira"] = P(1080, 1350, "y", f"""
{ighead('yatay_sari-zemin', 5, dark=False)}
<div style="padding:0 64px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y)">İLAN PİYASASI · {up(G['donem'])}</span>
  <h1 style="font-weight:900;font-size:76px;line-height:1.02;margin-top:30px">Gaziosmanpaşa'da<br>kira ve getiri</h1>
</div>
<div style="padding:0 64px;margin-top:44px;display:grid;grid-template-columns:1fr 1fr;gap:22px">
  {bigcard('home', 'SATILIK İLAN ORTALAMASI', mtl(G['satilik_ort']), pct(G['satilik_degisim'],1,True) + ' geçen aya göre')}
  {bigcard('key', 'KİRALIK İLAN ORTALAMASI', thou(G['kiralik_ort']) + ' TL', pct(G['kiralik_degisim'],1,True) + ' geçen aya göre')}
  {bigcard('pct', 'BRÜT GETİRİ', '≈ %' + num(GETIRI), 'yıllık', dark=True)}
  {bigcard('cal', 'AMORTİSMAN', '≈ ' + num(AMORT) + ' yıl', 'kira ile geri dönüş', dark=True)}
</div>
<p style="padding:0 64px;font-size:21px;margin-top:22px;opacity:.7">İlan fiyatlarıdır, gerçekleşen satış fiyatı değildir. Kaynak: İşlerOS ilan verileri.</p>
{footer('fk', 110, addr=False)}""")

T[f"{SLUG}_10_ig-carousel-4x5_5-kapanis"] = P(1080, 1350, "y", f"""
<div style="position:absolute;right:-80px;bottom:-160px;width:700px;height:700px;border-radius:50%;background:#000"></div>
<img src="{PHOTO}" style="position:absolute;right:-30px;bottom:0;height:760px">
{ighead('yatay_sari-zemin', 11, dark=False)}
<div style="position:relative;padding:0 64px;margin-top:110px;max-width:640px">
  <h1 style="font-weight:900;font-size:88px;line-height:1.0">Evinizin bugünkü değerini konuşalım.</h1>
  <p style="font-weight:500;font-size:32px;line-height:1.35;margin-top:34px">Gaziosmanpaşa'da satış ve kira kararlarınızı güncel verilerle birlikte verelim.</p>
  <div style="margin-top:48px;background:#000;color:var(--y);font-weight:900;font-size:58px;padding:22px 30px;border-radius:10px;display:inline-block">{PHONE}</div>
</div>
<div style="position:absolute;left:64px;bottom:56px;font-weight:800;font-size:30px">Alper İşler · {IG}</div>""")

T[f"{SLUG}_11_ig-story-9x16_1-yeni-yazi"] = P(1080, 1920, "k", f"""
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 50% at 60% 80%, rgba(243,189,72,.35), rgba(0,0,0,0) 70%),#000"></div>
{sunburst(1080, 1920, 600, 1500, op=.07)}
<div style="position:absolute;left:50%;bottom:-260px;width:900px;height:900px;margin-left:-450px;border-radius:50%;background:#F3BD48"></div>
<img src="{PHOTO}" style="position:absolute;left:50%;bottom:0;height:980px;transform:translateX(-50%)">
<div style="position:relative;padding:150px 80px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:120px;margin-left:-12px"></div>
<div style="position:relative;padding:0 80px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000;font-size:28px">GAZİOSMANPAŞA · {up(AY)} {YIL}</span>
  <div class="hero-title" style="font-size:108px;margin-top:36px">{B['manset_ust']}<br><span>{B['manset_vurgu']}</span><br>{B['manset_alt']}</div>
</div>
<div style="position:absolute;left:-40px;right:-40px;bottom:120px;height:120px;background:#000;border-top:6px solid #F3BD48;border-bottom:6px solid #F3BD48;transform:rotate(-3deg);display:flex;align-items:center;justify-content:center;color:#F3BD48;font-weight:900;font-size:40px;letter-spacing:.06em">BU AYIN YORUMLARI →</div>""")

T[f"{SLUG}_11_ig-story-9x16_2-ozet"] = P(1080, 1920, "y", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_sari-zemin')}" style="height:120px;margin-left:-14px"></div>
<div style="padding:0 80px;margin-top:80px">
  <span class="tag" style="background:#000;color:var(--y);font-size:28px">3 RAKAMDA {up(AY)}</span>
  <h1 style="font-weight:900;font-size:96px;line-height:1.0;margin-top:36px">Gaziosmanpaşa'da<br>bu ay</h1>
  <div style="display:flex;flex-direction:column;gap:26px;margin-top:60px">
    {bigcard('home', 'KONUT SATIŞI · ' + up(S['donem']['ay']), thou(S['gop']['satis']) + ' adet', pct(S['gop']['yillik_degisim'],1,True) + ' yıllık', dark=True)}
    {bigcard('key', 'KİRALIK İLAN ORTALAMASI', thou(G['kiralik_ort']) + ' TL', pct(G['kiralik_degisim'],1,True) + ' geçen aya göre')}
    {bigcard('trendup', 'İSTANBUL KONUT FİYATI', pct(K['istanbul']['yillik'],1,True), 'yıllık · TCMB', dark=True)}
  </div>
</div>
<div style="margin-top:auto;height:190px;background:#000;color:var(--y);display:flex;align-items:center;justify-content:center;gap:16px;font-weight:800;font-size:44px;stroke:var(--y)"><span style="display:inline-flex;width:46px">{PH}</span>{PHONE}</div>""")

def yorum_card(y, dark, big=False):
    bg = "#000" if dark else "#fff"; fg = "#fff" if dark else "#000"; vc = Y if dark else "#000"
    return (f'<div style="background:{bg};color:{fg};border:4px solid {"#3a3a3a" if dark else "#000"};border-radius:24px;padding:{30 if big else 26}px;display:flex;flex-direction:column;gap:12px">'
            f'<div style="display:flex;align-items:center;gap:14px"><div style="width:64px;height:64px;border-radius:16px;background:{Y};display:flex;align-items:center;justify-content:center">{icon(y["ikon"], "#000", 40)}</div>'
            f'<div style="font-size:18px;font-weight:800;letter-spacing:.1em;opacity:.8">{y["etiket"]}</div></div>'
            f'<div style="font-size:{36 if big else 34}px;font-weight:900;line-height:1.1">{y["baslik"]}</div>'
            f'<div style="font-size:{48 if big else 52}px;font-weight:900;line-height:1;color:{vc}">{y["deger"]}</div>'
            f'<div style="font-size:21px;font-weight:600;line-height:1.35;opacity:.8">{y["aciklama"]}</div></div>')
YR = B.get("yorumlar", [])[:4]
T[f"{SLUG}_10_ig-carousel-4x5_1b-yorumlar"] = P(1080, 1350, "y", f"""
{ighead('yatay_sari-zemin', 1, dark=False)}
<div style="padding:0 64px;margin-top:50px">
  <span class="tag" style="background:#000;color:var(--y)">BU AYIN YORUMLARI</span>
  <h1 style="font-weight:900;font-size:68px;line-height:1.02;margin-top:24px">Bu ay öne çıkan 4 konu</h1>
</div>
<div style="padding:0 64px;margin-top:34px;display:grid;grid-template-columns:1fr 1fr;gap:20px">
  {''.join(yorum_card(y, i in (1, 2)) for i, y in enumerate(YR))}
</div>
{footer('fk', 110, addr=False)}""")
T[f"{SLUG}_06_grafik-yorumlar"] = P(1600, 900, "y", f"""
<div style="padding:56px 70px 0;display:flex;justify-content:space-between;align-items:flex-start">
  <div><div style="font-size:22px;font-weight:800;letter-spacing:.12em">GAZİOSMANPAŞA · {up(AY)} {YIL}</div>
  <div style="font-size:56px;font-weight:900;line-height:1.05;margin-top:10px">Bu ay öne çıkan 4 konu</div></div>
  <img src="{logo('yatay_sari-zemin')}" style="height:80px"></div>
<div style="padding:0 70px;margin-top:40px;display:grid;grid-template-columns:repeat(4,1fr);gap:22px">
  {''.join(yorum_card(y, i % 2 == 1, big=True) for i, y in enumerate(YR))}
</div>
<div class="src">Kaynak: TÜİK, TCMB, İşlerOS ilan verileri (ilan fiyatları gerçekleşen satış fiyatı değildir).</div>
<div style="position:absolute;right:70px;bottom:30px;font-size:22px;font-weight:800">☎ {PHONE}</div>""")
T[f"{SLUG}_11_ig-story-9x16_2-ozet"] = P(1080, 1920, "y", f"""
<div style="padding:150px 80px 0"><img src="{logo('yatay_sari-zemin')}" style="height:120px;margin-left:-14px"></div>
<div style="padding:0 80px;margin-top:60px">
  <span class="tag" style="background:#000;color:var(--y);font-size:28px">BU AYIN YORUMLARI</span>
  <h1 style="font-weight:900;font-size:90px;line-height:1.0;margin-top:30px">Gaziosmanpaşa'da<br>bu ay</h1>
  <div style="display:flex;flex-direction:column;gap:22px;margin-top:44px">
    {''.join(yorum_card(y, i % 2 == 0) for i, y in enumerate(YR))}
  </div>
</div>
<div style="margin-top:auto;height:190px;background:#000;color:var(--y);display:flex;align-items:center;justify-content:center;gap:16px;font-weight:800;font-size:44px;stroke:var(--y)"><span style="display:inline-flex;width:46px">{PH}</span>{PHONE}</div>""")

GY = B.get("genel_yorumlar", [])[:4]
if GY:
    T[f"{SLUG}_10_ig-carousel-4x5_1c-genel"] = P(1080, 1350, "k", f"""
{ighead('yatay_siyah-zemin', 2)}
<div style="padding:0 64px;margin-top:50px">
  <span class="tag" style="background:var(--y);color:#000">GENEL PİYASA YORUMU</span>
  <h1 style="font-weight:900;font-size:68px;line-height:1.02;margin-top:24px">İstanbul ve Türkiye'de<br><span style="color:var(--y)">neler değişiyor?</span></h1>
</div>
<div style="padding:0 64px;margin-top:34px;display:grid;grid-template-columns:1fr 1fr;gap:20px">
  {''.join(yorum_card(y, i in (0, 3)) for i, y in enumerate(GY))}
</div>
{footer('fy', 110, addr=False)}""")
    T[f"{SLUG}_07_grafik-genel-piyasa"] = P(1600, 900, "k", f"""
<div style="padding:56px 70px 0;display:flex;justify-content:space-between;align-items:flex-start">
  <div><div style="font-size:22px;font-weight:800;letter-spacing:.12em;color:#F3BD48">GENEL PİYASA · FİYATLAR VE SATIŞLAR</div>
  <div style="font-size:56px;font-weight:900;line-height:1.05;margin-top:10px">Piyasada 4 büyük eğilim</div></div>
  <img src="{logo('yatay_siyah-zemin')}" style="height:80px"></div>
<div style="padding:0 70px;margin-top:40px;display:grid;grid-template-columns:repeat(4,1fr);gap:22px">
  {''.join(yorum_card(y, i % 2 == 1, big=True) for i, y in enumerate(GY))}
</div>
<div class="src" style="color:#fff">Kaynak: TCMB Konut Fiyat Endeksi, TÜİK Konut ve İş Yeri Satış İstatistikleri (İşlerOS).</div>
<div style="position:absolute;right:70px;bottom:30px;font-size:22px;font-weight:800;color:#fff">☎ {PHONE}</div>""")

# ---------------- 12 SAYFALIK CAROUSEL: her tespit ayrı sayfa ----------------
def tespit_slide(idx, y, grup, no, toplam, dark):
    bg = "k" if dark else "y"; fg = "#fff" if dark else "#000"; acc = Y if dark else "#000"
    numcls = "hero-num" if dark else ""
    numstyle = "" if dark else "font-weight:900;line-height:.9;letter-spacing:-.02em;color:#000"
    return P(1080, 1350, bg, f"""
{'' if not dark else sunburst(1080, 1350, 900, 1150, op=.05)}
{ighead('yatay_siyah-zemin' if dark else 'yatay_sari-zemin', idx, dark=dark)}
<div style="position:absolute;right:-90px;top:250px;width:520px;height:520px;border-radius:50%;background:{'#161616' if dark else '#000'};display:flex;align-items:center;justify-content:center;opacity:{1 if dark else .07}"></div>
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
{footer('fy' if dark else 'fk', 100, addr=False)}""")

for k in ["1b-yorumlar", "1c-genel", "4-kira"]:
    T.pop(f"{SLUG}_10_ig-carousel-4x5_{k}", None)
rename = {"1-kapak": "01-kapak", "2-satis": "10-ilceler", "3-fiyat": "11-fiyat-trend", "5-kapanis": "12-kapanis"}
for old, new in rename.items():
    T[f"{SLUG}_10_ig-carousel-4x5_{new}"] = T.pop(f"{SLUG}_10_ig-carousel-4x5_{old}")
for i, y in enumerate(B.get("yorumlar", [])[:4]):
    T[f"{SLUG}_10_ig-carousel-4x5_{i+2:02d}-tespit-{i+1}"] = tespit_slide(i + 1, y, "GAZİOSMANPAŞA", i + 1, 4, dark=(i % 2 == 0))
for i, y in enumerate(B.get("genel_yorumlar", [])[:4]):
    T[f"{SLUG}_10_ig-carousel-4x5_{i+6:02d}-genel-{i+1}"] = tespit_slide(i + 5, y, "GENEL PİYASA", i + 1, 4, dark=(i % 2 == 1))

if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else KIT / "out") / FOLDER
    render(T, out)
    print("FOLDER", out)
