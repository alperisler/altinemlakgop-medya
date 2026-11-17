"""Danışman adayı ikna serisi — İşlerOS + Danışman El Kitabı + altinemlakkariyer.com (4:5 carousel)."""
import sys
from build import page, logo, footer, dots, render, PHONE, IG, PH, IGI, PIN, ADDR, KIT
from isleros import ICONS, waves, islogo, APP

N = 11
BOOK = (KIT / "kitap_on.png").as_uri()
ALPER = (KIT / "alper.png").as_uri()
URL = "altinemlakkariyer.com/basvuru"

def ic(d, sw=1.9):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'

I = {
 "card": ic('<rect x="2.5" y="5" width="19" height="14" rx="2"/><circle cx="8" cy="11" r="2"/><path d="M5 16c.6-1.6 1.7-2.3 3-2.3s2.4.7 3 2.3M14 10h4.5M14 13.5h3"/>'),
 "mail": ic('<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="m3 6.5 9 6.5 9-6.5"/>'),
 "crm": ic('<ellipse cx="12" cy="5.5" rx="8" ry="3"/><path d="M4 5.5v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/><path d="M4 11.5v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>'),
 "web": ic('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/>'),
 "app": ic('<rect x="6" y="2.5" width="12" height="19" rx="2.5"/><path d="M10.5 18.5h3"/><path d="m9 9 2 2 4-4"/>'),
 "desk": ic('<path d="M3 9h18M5 9v11M19 9v11M3 9l2-5h14l2 5"/><path d="M9 14h6"/>'),
 "video": ic('<rect x="2.5" y="5" width="15" height="14" rx="2"/><path d="m17.5 10 4-2.5v9l-4-2.5"/><path d="m8.5 9.5 4 2.5-4 2.5z"/>'),
 "book": ic('<path d="M4 4.5A1.5 1.5 0 0 1 5.5 3H20v15H5.5A1.5 1.5 0 0 0 4 19.5z"/><path d="M4 19.5A1.5 1.5 0 0 0 5.5 21H20v-3"/><path d="M8 7h8M8 10.5h5"/>'),
 "x": ic('<path d="M6 6l12 12M18 6 6 18"/>', 2.6),
 "ok": ic('<path d="m5 12 5 5 9-10"/>', 2.8),
 "users": ic('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6.5 6.5-6.5s6.5 2.9 6.5 6.5"/><circle cx="17" cy="9" r="2.6"/><path d="M17.5 13.6c2.4.4 4 2.7 4 5.4"/>'),
 "cap": ic('<path d="m12 4 10 5-10 5L2 9z"/><path d="M6 11v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/>'),
 "map": ic('<path d="M9 4 3 6.5v13.5l6-2.5 6 2.5 6-2.5V4l-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/>'),
}

EXTRA = """
.hd{position:relative;z-index:3;padding:56px 64px 0;display:flex;justify-content:space-between;align-items:center}
.kick{display:inline-flex;align-items:center;gap:12px;font-weight:700;font-size:25px;letter-spacing:.14em}
.kick:before{content:"";width:46px;height:6px;background:var(--y)}
.y .kick:before{background:#000}
.h1{font-weight:900;font-size:92px;line-height:.98;letter-spacing:-.01em}
.h2{font-weight:900;font-size:76px;line-height:1.0;letter-spacing:-.01em}
.lead{font-weight:400;font-size:33px;line-height:1.38}
.body{position:relative;z-index:2;padding:40px 64px 0;flex:1;min-height:0;display:flex;flex-direction:column}
.yl{color:var(--y)}
.mark{background:var(--y);color:#000;padding:0 14px 6px;margin-left:-14px;display:inline-block}
.book{position:absolute;perspective:1800px;z-index:2}
.book .bk{position:relative;transform:rotateY(-22deg) rotateX(4deg);transform-style:preserve-3d;
  box-shadow:30px 40px 70px rgba(0,0,0,.55);border-radius:2px 6px 6px 2px}
.book .bk img{display:block;width:100%;border-radius:2px 6px 6px 2px}
.book .bk:before{content:"";position:absolute;left:0;top:0;bottom:0;width:6%;background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(255,255,255,.15) 45%,rgba(0,0,0,.08));z-index:2}
.book .bk:after{content:"";position:absolute;right:-14px;top:6px;bottom:6px;width:14px;background:repeating-linear-gradient(0deg,#f4f1ea 0 2px,#d9d4c8 2px 3px);transform:skewY(-30deg);transform-origin:left}
.phone{position:absolute;border-radius:58px;background:#000;border:11px solid #2a2a2a;box-shadow:0 40px 80px rgba(0,0,0,.6),0 0 0 2px #3a3a3a;overflow:hidden;z-index:3}
.phone img{width:100%;display:block}
.ck{display:flex;gap:18px;align-items:center}
.ck .b{width:56px;height:56px;border-radius:14px;flex:none;display:flex;align-items:center;justify-content:center}
.ck .b svg{width:32px}
.tile{border-radius:22px;padding:26px 24px;display:flex;flex-direction:column;gap:14px}
.tile .i{width:62px;height:62px;border-radius:14px;display:flex;align-items:center;justify-content:center}
.tile .i svg{width:36px}
.tile b{font-weight:800;font-size:30px;line-height:1.08}
.tile small{font-size:21px;line-height:1.3;opacity:.75}
.chips{display:flex;flex-wrap:wrap;gap:12px}
.chips span{font-weight:700;font-size:23px;padding:12px 18px;border-radius:12px}
.stamp{position:absolute;width:210px;height:210px;border-radius:50%;border:5px solid #000;display:flex;align-items:center;justify-content:center;
  text-align:center;font-weight:900;font-size:34px;line-height:1;transform:rotate(-12deg);z-index:4;letter-spacing:.04em}
.stamp:before{content:"";position:absolute;inset:10px;border-radius:50%;border:2px dashed currentColor}
"""

def head(theme, pg, tag="KARİYER"):
    lg = {"k": "yatay_siyah-zemin", "w": "yatay_beyaz-zemin", "y": "yatay_sari-zemin"}[theme]
    col = "var(--y)" if theme == "k" else "#000"
    h = {"k": 92, "w": 72, "y": 98}[theme]
    ml = {"k": -10, "w": 0, "y": -12}[theme]
    return (f'<div class="hd"><img src="{logo(lg)}" style="height:{h}px;margin-left:{ml}px">'
            f'<span style="color:{col}">{dots(N, pg)}</span></div>')

def foot(theme):
    return footer("fy" if theme == "k" else "fk", 104, addr=False)

def book(w, left=None, right=None, top=None, bottom=None, rot=-22):
    pos = "".join(f"{k}:{v}px;" for k, v in (("left", left), ("right", right), ("top", top), ("bottom", bottom)) if v is not None)
    return (f'<div class="book" style="{pos}width:{w}px"><div class="bk" style="transform:rotateY({rot}deg) rotateX(4deg)">'
            f'<img src="{BOOK}"></div></div>')

def phone(w, left=None, right=None, top=None, rot=6):
    pos = "".join(f"{k}:{v}px;" for k, v in (("left", left), ("right", right), ("top", top)) if v is not None)
    return (f'<div class="phone" style="{pos}width:{w}px;height:{int(w*2.02)}px;transform:rotate({rot}deg)">'
            f'<img src="{APP.as_uri()}" style="margin-top:-{int(w*0.135)}px"></div>')

P = {}

# 1 — KAPAK
P["01_kapak"] = page(1080, 1350, "k", f"""
{waves('#F3BD48', .14, w=1300, top=760, right=-420, rot=-12)}
{head('k', 0)}
<div class="body" style="padding-top:70px">
  <span class="tag" style="background:var(--y);color:#000;align-self:flex-start">DANIŞMAN ADAYLARINA</span>
  <div class="h1" style="margin-top:36px;font-size:104px">Bu mesleğe<br>yalnız<br><span class="yl">başlamayacaksın.</span></div>
  <p class="lead" style="margin-top:34px;max-width:520px;opacity:.85">Altın Emlak Gaziosmanpaşa'da danışmanlarımıza <b class="yl">ücretsiz</b> sunduklarımızı gör.</p>
</div>
{book(330, left=470, top=780, rot=-24)}
{phone(250, right=58, top=700, rot=8)}
<div style="position:relative;z-index:4;margin-top:auto;padding:0 64px 56px;font-weight:700;font-size:30px;color:var(--y);letter-spacing:.08em">KAYDIRIN →</div>""", EXTRA)

# 2 — SORUN / FARK
bad = ["Telefon rehberindeki isimler", "WhatsApp'ta kaybolan konuşmalar", "Masadaki not kâğıtları", "Yalnızca hafızaya güvenmek"]
P["02_fark"] = page(1080, 1350, "w", f"""
{head('w', 1)}
<div class="body">
  <span class="kick">GERÇEK</span>
  <div class="h2" style="margin-top:28px">Çoğu danışman<br>sıfırdan başlar.</div>
  <div style="margin-top:46px;display:flex;flex-direction:column;gap:20px">
    {''.join(f'<div class="ck" style="font-size:34px;font-weight:500;color:#777"><span class="b" style="background:#eee;stroke:#999">{I["x"]}</span><span style="text-decoration:line-through;text-decoration-thickness:2px">{t}</span></div>' for t in bad)}
  </div>
  <p class="lead" style="margin-top:34px;color:#555;font-size:29px">Bu düzenle müşteri unutulur, iş ölçülemez, emek boşa gider.</p>
</div>
<div style="position:relative;z-index:2;margin:0 64px 56px;background:#000;color:#fff;border-radius:26px;padding:44px 48px;display:flex;align-items:center;gap:30px">
  <span style="width:86px;height:86px;border-radius:20px;background:var(--y);stroke:#000;display:flex;align-items:center;justify-content:center;flex:none"><span style="width:50px;display:flex">{I["ok"]}</span></span>
  <div><div style="font-weight:900;font-size:50px;line-height:1.05">Bizde sistem,<br><span class="yl">ilk gün masanda hazır.</span></div></div>
</div>
{foot('w')}""", EXTRA)

# 3 — İLK GÜN MASANDA
kit = [("card", "Kurumsal kartvizit", "Altın Emlak kimliğiyle"),
       ("mail", "Kurumsal e-posta", "@altinemlak.com.tr"),
       ("crm", "GoldNet hesabı", "Kurumsal CRM, ilan ve EİDS"),
       ("web", "Kişisel web siten", "GoldNet ile entegre"),
       ("app", "İşlerOS erişimi", "Danışman profilin aktif"),
       ("desk", "Ofis alanı", "Çalışma alanın tahsis edilir"),
       ("video", "Eğitim videoları", "Dijital eğitim kaynakları"),
       ("book", "Danışman El Kitabı", "16 bölümlük sistem")]
tiles = "".join(f'<div class="tile" style="background:#000;color:#fff;flex-direction:row;align-items:center;gap:18px;padding:22px 20px"><span class="i" style="background:var(--y);stroke:#000;flex:none">{I[k]}</span><div style="display:flex;flex-direction:column;gap:6px"><b style="font-size:27px">{t}</b><small style="font-size:19px">{d}</small></div></div>' for k, t, d in kit)
P["03_ilk-gun"] = page(1080, 1350, "y", f"""
{head('y', 2)}
<div class="body">
  <span class="kick" style="color:#000">İLK GÜN MASANDA</span>
  <div class="h2" style="margin-top:24px">Kurumsal altyapın<br>hazır bekliyor.</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:44px">{tiles}</div>
  <div style="margin-top:auto;margin-bottom:48px;font-weight:900;font-size:58px;line-height:1.05">Hepsi ilk günden,<br><span class="mark" style="background:#000;color:var(--y)">ücretsiz.</span></div>
</div>
<div class="stamp" style="right:64px;top:176px;color:#000;width:190px;height:190px;font-size:30px">ÜCRET-<br>SİZ</div>
{foot('y')}""", EXTRA)

# 4 — DANIŞMAN EL KİTABI
chs = ["Bölge Hakimiyet Sistemi", "Portföy Kazanım Sistemi", "Değerleme ve Doğru Fiyatlandırma", "Sosyal Medya & Kişisel Marka",
       "Yapay Zekâ ile İçerik Üretimi", "Müşteri İlişkileri ve Satış", "Zaman ve Bütçe Yönetimi", "Performans Sistemi (KPI)", "Formlar ve Sözleşmeler"]
P["04_el-kitabi"] = page(1080, 1350, "k", f"""
{waves('#F3BD48', .12, w=1300, top=820, right=-500, rot=-10)}
{head('k', 3)}
<div class="body">
  <span class="kick" style="color:#fff">HEDİYEMİZ</span>
  <div class="h2" style="margin-top:24px">Danışman<br><span class="yl">El Kitabı</span></div>
  <p class="lead" style="margin-top:24px;max-width:500px;opacity:.85">16 bölüm. Sahada edinilmiş tecrübe, çalışma standartlarımız ve sistemimiz tek kitapta.</p>
  <div style="margin-top:36px;display:flex;flex-direction:column;gap:12px;max-width:540px">
    {''.join(f'<div style="display:flex;gap:16px;align-items:center;font-size:26px;font-weight:600;padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,.14)"><span style="color:var(--y);font-weight:900;width:38px">{n:02d}</span>{t}</div>' for n, t in enumerate(chs, 1))}
  </div>
</div>
{book(360, right=56, top=420, rot=-20)}
{foot('k')}""", EXTRA)

# 5 — İLK 90 GÜN
steps = [("30", "Sistemi öğren", "GoldNet ve İşlerOS, ofis prosedürleri, EİDS. Bölgeni yürüyerek tanı."),
         ("60", "İlişki kur, görünür ol", "Bölge çalışması, iş ortakları, düzenli içerik ve aktif talep havuzu."),
         ("90", "Sistemi oturt", "Günlük rutin, ilk yetkiler, ilk portföyler ve kendi verilerini ölçmek.")]
tl = "".join(f"""<div style="display:flex;gap:34px;position:relative">
  <div style="flex:none;width:150px;height:150px;border-radius:50%;background:{'#000' if i < 2 else 'var(--y)'};color:{'var(--y)' if i < 2 else '#000'};
     display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;z-index:2;{'border:4px solid #000' if i == 2 else ''}">
     <b style="font-weight:900;font-size:62px;line-height:.9">{d}</b><small style="font-weight:700;font-size:20px;letter-spacing:.12em">GÜN</small></div>
  <div style="padding-top:22px"><div style="font-weight:800;font-size:44px">{t}</div><div style="font-size:28px;line-height:1.38;margin-top:10px;color:#333;max-width:640px">{x}</div></div>
</div>""" for i, (d, t, x) in enumerate(steps))
P["05_ilk-90-gun"] = page(1080, 1350, "w", f"""
{head('w', 4)}
<div class="body">
  <span class="kick">YOL HARİTASI</span>
  <div class="h2" style="margin-top:24px">İlk 90 günün<br>planlı.</div>
  <div style="margin-top:46px;display:flex;flex-direction:column;gap:40px;position:relative">
    <span style="position:absolute;left:73px;top:40px;bottom:40px;width:4px;background:#000"></span>{tl}
  </div>
  <div style="margin-top:auto;margin-bottom:40px;background:#f4f4f4;border-left:8px solid var(--y);padding:24px 28px;font-size:26px;line-height:1.4">
    <b>Sahada yalnız değilsin:</b> broker ile değerleme görüşmeleri, tecrübeli danışmanlarla yer gösterme, tapu süreçlerini yerinde gözlem.</div>
</div>
{foot('w')}""", EXTRA)

# 6 — İŞLEROS
short = ["Görev yönetimi", "Randevu sistemi", "Otomatik müşteri takibi", "Ekspertiz formatları", "Saha hesaplamaları", "WhatsApp şablonları",
         "Dijital koçluk", "Piyasa analizleri", "Yapay zekâ ile görsel", "Performans ve ciro", "Resmî Gazete takibi", "Hedef planlama"]
P["06_isleros"] = page(1080, 1350, "k", f"""
{waves('#F3BD48', .12, w=1300, top=240, right=-560, rot=8)}
{head('k', 5)}
<div class="body">
  <span class="kick" style="color:#fff">DİJİTAL ASİSTANIN</span>
  <div style="margin:26px 0 0 -12px">{islogo(170)}</div>
  <p class="lead" style="margin-top:22px;max-width:560px;opacity:.85">Ofisimizin sahadaki ihtiyaçlardan doğan kendi sistemi. Web ve mobilde, cebinde.</p>
  <div style="margin-top:34px;display:grid;grid-template-columns:1fr 1fr;gap:12px 14px;max-width:600px">
    {''.join(f'<div style="display:flex;gap:12px;align-items:center;font-size:22px;font-weight:600"><span style="width:44px;height:44px;border-radius:11px;background:#1c1f23;stroke:var(--y);display:flex;align-items:center;justify-content:center;flex:none"><span style="width:26px;display:flex">{ICONS[i]}</span></span>{t}</div>' for i, t in enumerate(short))}
  </div>
</div>
{phone(330, right=40, top=330, rot=7)}
{foot('k')}""", EXTRA)

# 7 — DİJİTAL EKOSİSTEM
nodes = [("GoldNet", "Kurumsal CRM · ilan · EİDS", 120, 40), ("İşlerOS", "Görev · randevu · talep", 560, 40),
         ("REOS MLS", "Meslektaş iş birliği", 40, 400), ("Tapusor", "Tapu ve emsal verisi", 640, 400),
         ("Yapay zekâ", "İçerik · görsel · değerleme", 316, 530)]
svg_lines = "".join(f'<line x1="476" y1="330" x2="{x+160}" y2="{y+70}" stroke="#000" stroke-width="4" stroke-dasharray="2 12" stroke-linecap="round"/>' for _, _, x, y in nodes)
nd = "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:320px;background:#000;color:#fff;border-radius:20px;padding:22px 24px">'
             f'<div style="font-weight:900;font-size:36px;color:var(--y)">{t}</div><div style="font-size:21px;margin-top:6px;opacity:.85">{d}</div></div>' for t, d, x, y in nodes)
P["07_ekosistem"] = page(1080, 1350, "y", f"""
{head('y', 6)}
<div class="body">
  <span class="kick" style="color:#000">TEKNOLOJİ</span>
  <div class="h2" style="margin-top:24px">Tek program değil,<br>bir ekosistem.</div>
  <div style="position:relative;height:660px;margin-top:30px">
    <svg style="position:absolute;inset:0;width:952px;height:700px">{svg_lines}</svg>
    {nd}
    <div style="position:absolute;left:386px;top:240px;width:180px;height:180px;border-radius:50%;background:#fff;border:6px solid #000;display:flex;flex-direction:column;align-items:center;justify-content:center">
      <b style="font-weight:900;font-size:44px">SEN</b><small style="font-size:18px;font-weight:600">danışman</small></div>
  </div>
</div>
<div style="position:relative;z-index:2;margin:0 64px 40px;display:flex;gap:16px;font-weight:800;font-size:26px">
  <span style="background:#000;color:var(--y);padding:14px 20px;border-radius:12px">100+ temsilcilik</span>
  <span style="background:#000;color:#fff;padding:14px 20px;border-radius:12px">Türkiye geneli portföy paylaşımı</span></div>
{foot('y')}""", EXTRA)

# 8 — EĞİTİM
edu = [("users", "Ofis içi eğitimler", "Düzenli eğitimler, vaka analizleri ve saha değerlendirme toplantıları."),
       ("cap", "Altın Akademi", "Genel Müdürlük'ten çevrim içi ve yüz yüze programlar: mevzuat, satış, teknoloji, pazarlama."),
       ("map", "Saha mentorluğu", "Broker ile değerleme görüşmeleri, portföy çekimleri ve tapu süreçleri."),
       (None, "Dijital koçluk", "İşlerOS Koçluk Merkezi'nde kişiselleştirilmiş öneriler ve gelişim takibi.")]
cards = "".join(f'<div style="display:flex;gap:26px;align-items:flex-start;padding:30px 0;border-top:3px solid #000">'
                f'<span style="width:82px;height:82px;border-radius:18px;background:#000;stroke:var(--y);display:flex;align-items:center;justify-content:center;flex:none"><span style="width:46px;display:flex">{I[k] if k else ICONS[6]}</span></span>'
                f'<div><div style="font-weight:800;font-size:42px">{t}</div><div style="font-size:28px;line-height:1.38;color:#333;margin-top:8px">{d}</div></div></div>' for k, t, d in edu)
P["08_egitim"] = page(1080, 1350, "w", f"""
{waves('#F3BD48', .28, w=1400, top=150, right=-760, rot=-8)}
{head('w', 7)}
<div class="body">
  <span class="kick">EĞİTİM</span>
  <div class="h2" style="margin-top:24px">Öğrenmek<br>burada bitmiyor.</div>
  <div style="margin-top:36px">{cards}</div>
</div>
{foot('w')}""", EXTRA)

# 9 — KAZANÇ MODELİ
lv = [("Standart", 50, "Başlangıç modeli", ["Aylık katkı payı yok", "Ofis onaylı sınırsız ilan"], 1),
      ("Performans", 65, "6 ay kıdem + üretim kriteri", ["10 ilan hakkı", "Aylık katkı payı"], 0),
      ("Premium", 80, "12 ay kıdem + üretim kriteri", ["10 ilan hakkı", "Aylık katkı payı"], 0)]
bars = "".join(f"""<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;gap:14px">
  <div style="font-weight:700;font-size:22px;letter-spacing:.1em;color:{'var(--y)' if hl else '#bbb'}">{n.upper()}</div>
  <div style="height:{int(p*6.2)}px;border-radius:18px 18px 0 0;background:{'var(--y)' if hl else '#1f2226'};color:{'#000' if hl else '#fff'};padding:22px;display:flex;flex-direction:column;gap:10px;{'' if hl else 'border:2px solid #333;border-bottom:0'}">
    <div style="font-weight:900;font-size:72px;line-height:.9">%{p}</div><div style="font-size:19px;font-weight:600;opacity:.8">danışman payı</div>
    <div style="margin-top:auto;font-size:19px;line-height:1.35;font-weight:600">{s}<br>{'<br>'.join(f + ('' ) for f in fs)}</div></div></div>""" for n, p, s, fs, hl in lv)
P["09_kazanc"] = page(1080, 1350, "k", f"""
{head('k', 8)}
<div class="body">
  <span class="kick" style="color:#fff">KAZANÇ</span>
  <div class="h2" style="margin-top:24px">Kazancın,<br><span class="yl">gelişiminle büyür.</span></div>
  <p class="lead" style="margin-top:22px;opacity:.85;font-size:30px">Performansa dayalı iş ortaklığı modeli. Kriterleri sağladıkça üst modele geçersin.</p>
  <div style="display:flex;gap:18px;margin-top:auto;align-items:flex-end">{bars}</div>
  <div style="font-size:19px;opacity:.6;margin:16px 0 30px">Geçiş şartları ve katkı payları İş Ortaklığı ve Çalışma Prensipleri Sözleşmesi'nde düzenlenir.</div>
</div>
{foot('k')}""", EXTRA)

# 10 — BROKER'DAN
P["10_broker"] = page(1080, 1350, "y", f"""
{waves('#000', .07, w=1300, top=500, right=-300, rot=-8)}
{head('y', 9)}
<div class="body" style="max-width:700px">
  <span class="kick" style="color:#000">BROKER'DAN</span>
  <div style="font-family:Georgia,serif;font-weight:700;font-size:200px;line-height:.6;margin-top:50px">“</div>
  <div style="font-weight:800;font-size:54px;line-height:1.12">Bu meslekte başarı tesadüf değildir.</div>
  <div style="font-weight:500;font-size:34px;line-height:1.38;margin-top:24px">Bilgi, disiplin, doğru sistem ve sürekli gelişimin sonucudur. Bilgimizi, tecrübemizi ve sistemimizi seninle paylaşmaya hazırız.</div>
  <div style="margin-top:40px;background:#000;color:#fff;display:inline-block;align-self:flex-start;padding:20px 26px;border-radius:14px">
    <div style="font-weight:900;font-size:34px">Alper İşler</div><div style="font-size:21px;color:var(--y);font-weight:600;margin-top:4px">Broker &amp; Owner · 2011'den beri sahada</div></div>
</div>
<img src="{ALPER}" style="position:absolute;right:-70px;bottom:104px;height:900px;z-index:1">
{foot('y')}""", EXTRA)

# 11 — BAŞVURU
flow = ["Başvuru", "Kariyer testi", "Görüşme", "Ofis eşleşmesi", "Altın Akademi", "Saha pratiği"]
fl = "".join(f'<div style="display:flex;align-items:center;gap:14px;font-size:25px;font-weight:600"><span style="width:44px;height:44px;border-radius:50%;background:{"var(--y)" if i == 0 else "#1c1f23"};color:{"#000" if i == 0 else "var(--y)"};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:21px;flex:none">{i+1}</span>{t}</div>' for i, t in enumerate(flow))
P["11_basvuru"] = page(1080, 1350, "k", f"""
{waves('#F3BD48', .13, w=1300, top=330, right=-560, rot=10)}
{head('k', 10)}
<div class="body">
  <span class="kick" style="color:#fff">BAŞVURU</span>
  <div class="h1" style="margin-top:26px">Yerin<br><span class="yl">hazır.</span></div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:30px">
    {''.join(f'<span style="border:2px solid var(--y);color:var(--y);font-weight:700;font-size:23px;padding:10px 18px;border-radius:999px">{t}</span>' for t in ["Başvuru ücretsiz", "Deneyim şartı aranmadan başvur", "Kariyer testi ~8 dk"])}
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px 30px;margin-top:40px">{fl}</div>
  <div style="display:flex;gap:30px;margin-top:56px"><div style="flex:1;border-top:4px solid var(--y);padding-top:16px"><div style="font-weight:900;font-size:64px;color:var(--y);line-height:1">100+</div><div style="font-size:21px;font-weight:600;margin-top:8px;opacity:.85">temsilcilik</div></div><div style="flex:1;border-top:4px solid var(--y);padding-top:16px"><div style="font-weight:900;font-size:64px;color:var(--y);line-height:1">%100</div><div style="font-size:21px;font-weight:600;margin-top:8px;opacity:.85">yerli marka</div></div><div style="flex:1;border-top:4px solid var(--y);padding-top:16px"><div style="font-weight:900;font-size:64px;color:var(--y);line-height:1">20+</div><div style="font-size:21px;font-weight:600;margin-top:8px;opacity:.85">yıllık tecrübe</div></div></div>
  <div style="margin-top:auto;margin-bottom:34px;background:var(--y);color:#000;border-radius:24px;padding:30px 36px">
    <div style="font-weight:700;font-size:22px;letter-spacing:.14em">HEMEN BAŞVUR</div>
    <div style="font-weight:900;font-size:56px;margin-top:8px;letter-spacing:-.01em">{URL}</div>
    <div style="font-size:22px;font-weight:600;margin-top:10px;display:flex;gap:10px;align-items:center;stroke:#000"><span style="width:24px;display:inline-flex">{PIN}</span>Görüşme için Gaziosmanpaşa ofisimize bekleriz.</div>
  </div>
</div>
{foot('k')}""", EXTRA + ".c span svg{height:auto}")

if __name__ == "__main__":
    render({k: P[k] for k in (sys.argv[2:] or P)}, sys.argv[1])
