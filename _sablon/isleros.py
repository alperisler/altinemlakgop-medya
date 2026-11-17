"""İşlerOS — danışmanlara sunulanlar carousel'ı (4:5, 8 sayfa) — v2: her maddeye destek görseli."""
import sys, pathlib
from build import page, logo, footer, dots, render, PHONE, IG, PH, IGI, KIT

N = 8
ISLOGO = KIT / "logo" / "isleros_logo.png"
APP = KIT / "app.png"

def ic(d):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'

ICONS = [
    ic('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="m8 8 1.5 1.5L12 7"/><path d="M14 8h3"/><path d="m8 13 1.5 1.5L12 12"/><path d="M14 13h3"/><path d="M8 18h9"/>'),
    ic('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/><path d="M8 14h2M14 14h2M8 17h2"/>'),
    ic('<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.3 2.7-6 6-6 1.4 0 2.6.4 3.6 1.2"/><path d="M21 15a4 4 0 1 1-1.2-2.8"/><path d="M21 11v2.5h-2.5"/>'),
    ic('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M8.5 13h7M8.5 16.5h5"/>'),
    ic('<rect x="5" y="2.5" width="14" height="19" rx="2"/><rect x="8" y="5.5" width="8" height="4" rx=".5"/><path d="M8.5 13h.01M12 13h.01M15.5 13h.01M8.5 16.5h.01M12 16.5h.01M15.5 16.5h.01M8.5 19h7"/>'),
    ic('<path d="M21 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20.5l1.6-5.2A8.5 8.5 0 1 1 21 11.5z"/><path d="M8.5 10h7M8.5 13.5h4.5"/>'),
    ic('<path d="m12 4 10 5-10 5L2 9z"/><path d="M6 11v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/><path d="M22 9v5"/>'),
    ic('<path d="M3 3v18h18"/><rect x="6.5" y="12" width="3" height="6"/><rect x="11.5" y="9" width="3" height="9"/><rect x="16.5" y="6" width="3" height="12"/>'),
    ic('<rect x="3" y="4" width="15" height="15" rx="2"/><circle cx="8" cy="9" r="1.6"/><path d="m3 16 4.5-4 4 3.5 2.5-2 4 3"/><path d="M20 2.5v4M18 4.5h4"/>'),
    ic('<path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4v1.5A3.5 3.5 0 0 0 7.5 11M17 6h3v1.5a3.5 3.5 0 0 1-3.5 3.5"/><path d="M12 14v3.5M8 21h8M9.5 17.5h5V21h-5z"/>'),
    ic('<path d="M4 5h13v14a2 2 0 0 0 2 2H6a2 2 0 0 1-2-2z"/><path d="M17 9h3v10a2 2 0 0 1-2 2"/><path d="M7.5 8.5h6M7.5 12h6M7.5 15.5h4"/>'),
    ic('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5.5"/><circle cx="12" cy="12" r="2"/>'),
]

FEATURES = [
    ("Akıllı Görev Yönetimi", "To-Do List", "Günlük işlerini planla, görevlerini takip et, hiçbir detayı atlama."),
    ("Randevu Yönetim Sistemi", "", "Müşteri görüşmelerini, portföy sunumlarını ve randevularını tek yerden yönet."),
    ("Tam Otomatik Müşteri Takip Sistemi", "", "Müşterilerini unutmadan, manuel takip yükü olmadan satış ve kiralama süreçlerini yönet."),
    ("Profesyonel Ekspertiz Formatları", "", "Gayrimenkul değerleme ve ekspertiz çalışmalarını standart, profesyonel formatlarla hazırla."),
    ("Saha Hesaplama Araçları", "", "Gayrimenkul işlemlerinde ihtiyaç duyduğun hesaplamalara saniyeler içinde ulaş."),
    ("Hazır WhatsApp Mesaj Şablonları", "", "Müşteri iletişiminin her aşamasında profesyonel, hızlı ve hazır mesajlardan yararlan."),
    ("Ücretsiz Dijital Danışman Koçluğu", "", "Farklı konularda kişiselleştirilmiş koçluk önerileri al, gelişimini takip et."),
    ("Gayrimenkul Piyasa Analizleri", "", "Güncel piyasa verilerini incele, müşterilerine veriye dayalı danışmanlık sun."),
    ("Yapay Zekâ ile Görsel Düzenleme", "", "Portföy görsellerini yapay zekâ desteğiyle düzenle, pazarlama çalışmalarını güçlendir."),
    ("Canlı Performans ve Ciro Takibi", "", "Ofis ve danışman sıralamalarını, güncel ciro performansını anlık görüntüle."),
    ("Anlık Resmî Gazete Takibi", "", "Gayrimenkul sektörünü ilgilendiren mevzuat ve düzenlemelerden haberdar ol."),
    ("Akıllı Kazanç ve Hedef Planlama", "", "Potansiyel kazancını otomatik hesapla, ciro hedefini belirle ve hedeflerine ulaşmak için çalışma planı oluştur."),
]
GROUPS = ["Planla", "Müşteri & portföy", "Sahada hızlan", "Gelişim & analiz", "Pazarla & ölç", "Haberdar ol & hedefle"]

# ---------------- destek görselleri (uygulama arayüzü çizimleri) ----------------
Y = "#F3BD48"
def chk(on): return (f'<span class="cb" style="background:{Y};border-color:{Y}">'
                     f'<svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5 9-10"/></svg></span>'
                     if on else '<span class="cb"></span>')
def head_v(t, right=""): return f'<div class="vh"><span>{t}</span>{right}</div>'
def badge(t, y=True): return f'<span class="bd" style="{"background:"+Y+";color:#000" if y else ""}">{t}</span>'

V = []
# 1 görevler
V.append(head_v("Bugünkü Görevler", badge("10 / 16")) + "".join(
    f'<div class="trow{" done" if d else ""}">{chk(d)}<span>{t}</span></div>' for t, d in
    [("Müşteri geri dönüşü", 1), ("İlan fotoğrafları", 1), ("Ekspertiz raporu", 0), ("Tapu randevusu teyidi", 0)])
    + '<div class="bar" style="margin-top:auto;flex:none"><i style="width:62%"></i></div>')
# 2 randevu
days = "".join(f'<div class="dy{" on" if n == 23 else ""}"><small>{g}</small><b>{n}</b></div>'
               for g, n in zip(["Pt", "Sa", "Ça", "Pe", "Cu", "Ct", "Pz"], range(19, 26)))
V.append(head_v("Randevular", badge("Ekim", False)) + f'<div class="wk">{days}</div>' + "".join(
    f'<div class="ap"><b>{h}</b><div><div class="t">{t}</div><div class="s">{s}</div></div></div>'
    for h, t, s in [("10:30", "Portföy sunumu", "Sarıgöl Mah."), ("16:00", "Yer gösterme", "Karadeniz Mah.")]))
# 3 müşteri takip
stg = [("Yeni", 2), ("Görüşme", 2), ("Yer gösterme", 1), ("Teklif", 0)]
pipe = "".join(f'<div class="st"><i class="s{s}"></i><small>{t}</small></div>' for t, s in stg)
V.append(head_v("Müşteri Takibi", badge("OTOMATİK")) +
    '<div class="lead"><span class="av">AY</span><div><div class="t">Ahmet Y.</div><div class="s">3+1 satılık daire arıyor</div></div></div>'
    f'<div class="pipe">{pipe}</div>'
    '<div class="lead" style="padding:10px 14px"><span class="av sm">MD</span><div><div class="t" style="font-size:18px">Merve D.</div><div class="s" style="font-size:15px">Kiralık 2+1 · Son temas 2 gün önce</div></div></div>'
    f'<div class="nt" style="margin-top:auto"><span class="dot"></span>Hatırlatma · Yarın 11:00 geri dönüş</div>')
# 4 ekspertiz
V.append('<div class="doc"><div class="dh">EKSPERTİZ RAPORU</div>' + "".join(
    f'<div class="dr"><span>{k}</span><i style="width:{w}%"></i></div>' for k, w in
    [("Brüt / Net m²", 46), ("Kat / Bina yaşı", 38), ("İmar durumu", 54), ("Emsal karşılaştırma", 30)]) +
    '<div class="dr" style="border:0;margin-top:6px"><span><b>Değer aralığı</b></span><i class="rg"></i></div>'
    '<div class="stamp">AE</div></div>')
# 5 hesaplama
tools = ["Tapu harcı", "Kredi taksiti", "Hizmet bedeli", "m² birim fiyat", "Kira artışı", "Getiri süresi"]
V.append(head_v("Hesaplama Araçları") +
    '<div class="inp"><small>Satış bedeli</small><span>₺ <i></i></span></div>'
    '<div class="btn">Hesapla</div>'
    '<div class="grid">' + "".join(f'<span{" class=on" if i == 0 else ""}>{t}</span>' for i, t in enumerate(tools)) + '</div>')
# 6 whatsapp
V.append(head_v("Mesaj Şablonları") +
    '<div class="bin">Merhaba, ilandaki daire hâlâ satılık mı?</div>'
    '<div class="chips"><span class="on">İlk temas</span><span>Randevu teyidi</span><span>Teşekkür</span></div>'
    '<div class="bout">Merhaba, ilginiz için teşekkürler! Daire satışta. Size uygun bir saatte yer gösterme planlayalım mı?</div>')
# 7 koçluk
V.append(head_v("Koçluk Merkezi") +
    '<div class="tip"><small>BUGÜNÜN ÖNERİSİ</small>Portföy sunumundan önce bölgedeki son satışları yanında götür.</div>' + "".join(
    f'<div class="sk"><span>{t}</span><div class="bar"><i style="width:{w}%"></i></div></div>' for t, w in
    [("Müzakere", 72), ("Portföy alma", 55), ("Dijital pazarlama", 84)]))
# 8 piyasa
V.append(head_v("Piyasa Analizi", '<span class="chips sm"><span class="on">Satış</span><span>Kira</span></span>') +
    '<div class="s" style="margin:-4px 0 4px">m² fiyat eğilimi · Gaziosmanpaşa</div>'
    '<svg viewBox="0 0 360 190" preserveAspectRatio="none" style="width:100%;flex:1;min-height:0">'
    '<defs><linearGradient id="gA" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#F3BD48" stop-opacity=".45"/><stop offset="1" stop-color="#F3BD48" stop-opacity="0"/></linearGradient></defs>'
    + "".join(f'<line x1="0" x2="360" y1="{y}" y2="{y}" stroke="#fff" stroke-opacity=".08"/>' for y in (30, 80, 130, 180)) +
    '<path d="M0 160 C 40 150, 60 140, 90 145 S 140 110, 170 118 S 220 80, 250 86 S 310 40, 355 30 V190 H0Z" fill="url(#gA)"/>'
    '<path d="M0 160 C 40 150, 60 140, 90 145 S 140 110, 170 118 S 220 80, 250 86 S 310 40, 355 30" stroke="#F3BD48" stroke-width="4" fill="none"/>'
    '</svg>'
    '<div class="ax">' + "".join(f'<span>{m}</span>' for m in ["May", "Haz", "Tem", "Ağu", "Eyl", "Eki"]) + '</div>')
# 9 AI görsel (önce / sonra)
room = lambda f: (f'<svg viewBox="0 0 360 230" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:0;width:100%;height:100%;{f}">'
    '<rect width="360" height="230" fill="#e9dcc4"/><rect y="170" width="360" height="60" fill="#b98c5a"/>'
    '<rect x="40" y="40" width="110" height="90" rx="4" fill="#bfe0f2" stroke="#fff" stroke-width="8"/><line x1="95" y1="40" x2="95" y2="130" stroke="#fff" stroke-width="6"/>'
    '<rect x="185" y="120" width="140" height="50" rx="10" fill="#3d4b5c"/><rect x="195" y="100" width="120" height="34" rx="10" fill="#4f6075"/>'
    '<rect x="240" y="55" width="50" height="38" fill="#F3BD48"/>'
    '<path d="M60 170 v-40" stroke="#5b7a3a" stroke-width="5"/><circle cx="60" cy="125" r="18" fill="#6e9645"/></svg>')
V.append('<div class="ba">' + room("filter:grayscale(.85) brightness(.55) contrast(.9)") +
    '<div style="position:absolute;inset:0;clip-path:inset(0 0 0 50%)">' + room("filter:saturate(1.15) brightness(1.05)") + '</div>'
    '<div class="sl"><span>⟷</span></div><b class="lb" style="left:12px">ÖNCE</b><b class="lb" style="right:12px;background:#F3BD48;color:#000">SONRA</b></div>'
    '<div class="btn">✦ Yapay zekâ ile iyileştir</div>')
# 10 performans
rk = [("M.K.", 92, 1), ("A.İ.", 78, 0), ("S.D.", 61, 0), ("E.Y.", 44, 0)]
V.append(head_v("Ofis Sıralaması", badge("CANLI")) + "".join(
    f'<div class="rk"><b>{i}</b><span class="av sm"{" style=background:#F3BD48;color:#000" if top else ""}>{n}</span>'
    f'<div class="bar"><i style="width:{w}%;{"" if top else "background:#666"}"></i></div></div>'
    for i, (n, w, top) in enumerate(rk, 1)) +
    '<div class="nt" style="margin-top:auto"><span class="dot"></span>Ciro performansı anlık güncellenir</div>')
# 11 resmî gazete
V.append('<div class="nt" style="background:#F3BD48;color:#000"><span class="dot" style="background:#000;box-shadow:none"></span><b>Yeni düzenleme yayımlandı</b></div>'
    '<div class="gz"><div class="gh">RESMÎ GAZETE</div><div class="gd">Sektörünüzle ilgili güncel kararlar</div>'
    '<i style="width:92%"></i><i style="width:78%"></i><i class="hl" style="width:86%"></i><i class="hl" style="width:64%"></i><i style="width:70%"></i>'
    '<div class="tg">Sizin için özetlendi</div></div>')
# 12 hedef
V.append(head_v("Hedef Planlama") +
    '<div style="display:flex;gap:20px;align-items:center">'
    '<svg viewBox="0 0 120 120" style="width:150px;flex:none"><circle cx="60" cy="60" r="48" stroke="#fff" stroke-opacity=".1" stroke-width="14" fill="none"/>'
    '<circle cx="60" cy="60" r="48" stroke="#F3BD48" stroke-width="14" fill="none" stroke-linecap="round" stroke-dasharray="301.6" stroke-dashoffset="108" transform="rotate(-90 60 60)"/>'
    '<text x="60" y="60" text-anchor="middle" fill="#fff" font-family="Canaro" font-weight="900" font-size="26">%64</text>'
    '<text x="60" y="80" text-anchor="middle" fill="#aaa" font-family="Canaro" font-size="12">yıllık hedef</text></svg>'
    '<div style="flex:1"><div class="s">Bu haftanın planı</div>' + "".join(
    f'<div class="pl"><b>{n}</b><span>{t}</span></div>' for n, t in [("12", "arama"), ("4", "yer gösterme"), ("1", "portföy alma")]) +
    '</div></div><div class="nt" style="margin-top:auto"><span class="dot"></span>Potansiyel kazanç otomatik hesaplanır</div>')

# ---------------- dekor / stil ----------------
def waves(color, op, w=900, top=None, right=-120, bottom=None, rot=0):
    pos = f"top:{top}px;" if top is not None else f"bottom:{bottom}px;"
    paths = "".join(
        f'<path d="M0 {60+i*100} C 120 {15+i*100}, 220 {110+i*100}, 340 {68+i*100} S 560 {15+i*100}, 700 {62+i*100}" '
        f'stroke="{color}" stroke-width="54" fill="none" stroke-linecap="round"/>' for i in range(3))
    return (f'<svg viewBox="0 0 700 330" style="position:absolute;{pos}right:{right}px;width:{w}px;'
            f'opacity:{op};transform:rotate({rot}deg);pointer-events:none">{paths}</svg>')

EXTRA = """
.hd{position:relative;z-index:2;padding:56px 64px 0;display:flex;justify-content:space-between;align-items:center}
.chip{display:inline-flex;align-items:center;gap:12px;font-weight:700;font-size:25px;letter-spacing:.12em}
.chip:before{content:"";width:46px;height:6px;background:var(--y)}
.ic{width:84px;height:84px;border-radius:18px;display:flex;align-items:center;justify-content:center;flex:none}
.ic svg{width:48px;height:48px}
.num{font-weight:900;font-size:104px;line-height:.8;letter-spacing:-.03em;-webkit-text-stroke:2.5px var(--y);color:transparent}
.blk{position:relative;z-index:2;flex:1;min-height:0;display:flex;align-items:center;gap:44px;padding:28px 0}
.tx{flex:1;display:flex;flex-direction:column;gap:20px}
.tx h2{font-weight:800;font-size:50px;line-height:1.05}
.tx p{font-weight:400;font-size:29px;line-height:1.38}
.pill{display:inline-block;font-weight:700;font-size:19px;letter-spacing:.12em;padding:7px 14px;border-radius:999px;vertical-align:middle;margin-left:10px;position:relative;top:-6px}
.v{width:430px;height:430px;flex:none;background:#121417;border:1.5px solid rgba(255,255,255,.09);border-radius:30px;padding:26px;color:#fff;
   display:flex;flex-direction:column;gap:12px;box-shadow:0 30px 60px rgba(0,0,0,.28);font-size:21px;position:relative;overflow:hidden}
.v:before{content:"";position:absolute;inset:0 0 auto 0;height:5px;background:var(--y)}
.vh{display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:25px;margin-bottom:4px}
.bd{font-weight:700;font-size:16px;letter-spacing:.08em;padding:6px 12px;border-radius:999px;background:#2a2d31;color:#ddd}
.trow{display:flex;align-items:center;gap:14px;background:#1c1f23;border-radius:14px;padding:13px 16px;font-weight:500}
.trow.done span:last-child{opacity:.5;text-decoration:line-through}
.cb{width:28px;height:28px;border-radius:8px;border:2.5px solid #555;flex:none;display:flex;align-items:center;justify-content:center}
.cb svg{width:18px}
.bar{height:12px;border-radius:6px;background:#2a2d31;overflow:hidden;flex:1} .bar i{display:block;height:100%;border-radius:6px;background:var(--y)}
.sk .bar{flex:none}
.wk{display:flex;gap:7px} .dy{flex:1;background:#1c1f23;border-radius:14px;padding:10px 0;text-align:center;display:flex;flex-direction:column;gap:4px}
.dy small{font-size:14px;color:#999} .dy b{font-size:22px} .dy.on{background:var(--y);color:#000} .dy.on small{color:#000}
.ap{display:flex;gap:16px;align-items:center;background:#1c1f23;border-radius:14px;padding:14px 16px;border-left:5px solid var(--y)}
.ap>b{font-size:24px;color:var(--y)} .t{font-weight:700;font-size:21px} .s{font-size:17px;color:#9a9a9a}
.lead{display:flex;gap:14px;align-items:center;background:#1c1f23;border-radius:16px;padding:14px}
.av{width:56px;height:56px;border-radius:50%;background:#2e3237;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:19px;flex:none}
.av.sm{width:44px;height:44px;font-size:15px}
.pipe{display:flex;justify-content:space-between;position:relative;margin:14px 0 4px}
.pipe:before{content:"";position:absolute;left:40px;right:40px;top:13px;height:3px;background:#333}
.st{position:relative;display:flex;flex-direction:column;align-items:center;gap:8px;width:84px;text-align:center}
.st i{width:28px;height:28px;border-radius:50%;border:3px solid #555;background:#121417}
.st i.s2{background:var(--y);border-color:var(--y)} .st i.s1{border-color:var(--y);background:radial-gradient(var(--y) 40%,#121417 45%)}
.st small{font-size:14px;color:#aaa;line-height:1.1}
.nt{display:flex;gap:12px;align-items:center;background:#1c1f23;border-radius:14px;padding:13px 16px;font-size:18px;font-weight:500}
.dot{width:12px;height:12px;border-radius:50%;background:var(--y);flex:none;box-shadow:0 0 0 5px rgba(243,189,72,.2)}
.doc{background:#fafafa;color:#111;border-radius:14px;flex:1;padding:22px;display:flex;flex-direction:column;gap:12px;position:relative}
.dh{font-weight:900;font-size:21px;letter-spacing:.1em;padding-bottom:12px;border-bottom:4px solid var(--y)}
.dr{display:flex;align-items:center;gap:14px;font-size:17px;padding:6px 0;border-bottom:1px solid #e3e3e3}
.dr span{width:170px;flex:none;color:#444} .dr i{height:10px;border-radius:5px;background:#d6d6d6}
.dr i.rg{flex:1;height:16px;background:linear-gradient(90deg,#d6d6d6 0 20%,var(--y) 20% 75%,#d6d6d6 75%)}
.stamp{position:absolute;right:24px;bottom:16px;width:74px;height:74px;border-radius:50%;border:4px solid var(--y);color:#c7962c;
   display:flex;align-items:center;justify-content:center;font-weight:900;font-size:22px;transform:rotate(-14deg)}
.inp{background:#1c1f23;border-radius:14px;padding:12px 16px;display:flex;flex-direction:column;gap:6px}
.inp small{font-size:15px;color:#999} .inp span{font-weight:800;font-size:24px;display:flex;align-items:center;gap:10px}
.inp span i{height:12px;width:160px;border-radius:6px;background:#3a3d42}
.btn{background:var(--y);color:#000;font-weight:800;font-size:20px;text-align:center;padding:13px;border-radius:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:4px}
.grid span{background:#1c1f23;border-radius:12px;padding:11px 12px;font-size:17px;font-weight:600;text-align:center}
.grid span.on{outline:2px solid var(--y)}
.bin{background:#24272c;border-radius:18px 18px 18px 4px;padding:14px 16px;font-size:18px;max-width:82%}
.bout{background:var(--y);color:#000;border-radius:18px 18px 4px 18px;padding:14px 16px;font-size:18px;font-weight:500;max-width:88%;align-self:flex-end;line-height:1.3;margin-top:auto}
.chips{display:flex;gap:8px;flex-wrap:wrap} .chips span{font-size:15px;font-weight:700;padding:7px 12px;border-radius:999px;background:#24272c;color:#ccc}
.chips span.on{background:#fff;color:#000} .chips.sm span{font-size:14px;padding:5px 10px}
.tip{background:linear-gradient(135deg,#2a2412,#1c1f23);border:1.5px solid rgba(243,189,72,.4);border-radius:16px;padding:16px;font-size:19px;line-height:1.35;font-weight:500}
.tip small{display:block;color:var(--y);font-weight:800;font-size:14px;letter-spacing:.12em;margin-bottom:8px}
.sk{display:flex;flex-direction:column;gap:8px;font-size:17px;font-weight:600}
.ax{display:flex;justify-content:space-between;font-size:14px;color:#888}
.ba{position:relative;flex:1;border-radius:16px;overflow:hidden}
.sl{position:absolute;top:0;bottom:0;left:50%;width:4px;margin-left:-2px;background:#fff}
.sl span{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:46px;height:46px;border-radius:50%;background:#fff;color:#000;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:900}
.lb{position:absolute;top:12px;font-size:14px;letter-spacing:.12em;padding:6px 10px;border-radius:8px;background:rgba(0,0,0,.65)}
.rk{display:flex;align-items:center;gap:14px} .rk>b{width:20px;font-size:20px;color:#999}
.gz{background:#fafafa;color:#111;border-radius:14px;flex:1;padding:20px;display:flex;flex-direction:column;gap:11px}
.gh{font-family:Georgia,serif;font-weight:700;font-size:28px;text-align:center;border-bottom:3px double #111;padding-bottom:8px;letter-spacing:.04em}
.gd{font-size:14px;text-align:center;color:#666;margin-top:-4px}
.gz i{display:block;height:10px;border-radius:5px;background:#dcdcdc} .gz i.hl{background:var(--y)}
.tg{margin-top:auto;align-self:flex-start;font-size:15px;font-weight:800;background:#111;color:var(--y);padding:7px 12px;border-radius:8px}
.pl{display:flex;align-items:baseline;gap:10px;padding:7px 0;border-bottom:1px solid #2a2d31} .pl b{font-size:30px;color:var(--y);font-weight:900;width:44px} .pl span{font-size:18px}
.mk{position:absolute;border-radius:62px;background:#000;border:12px solid #2a2a2a;box-shadow:0 50px 90px rgba(0,0,0,.7),0 0 0 2px #3a3a3a;overflow:hidden}
"""

def islogo(h): return f'<img src="{ISLOGO.as_uri()}" style="height:{h}px;display:block">'

def head(dark, pg):
    lg = logo("yatay_siyah-zemin" if dark else "yatay_beyaz-zemin")
    col = "var(--y)" if dark else "#000"
    return (f'<div class="hd"><div style="display:flex;align-items:center;gap:24px">'
            f'<img src="{lg}" style="height:{90 if dark else 70}px;{"margin-left:-10px" if dark else ""}">'
            f'<span style="width:2px;height:54px;background:{col};opacity:.5"></span>{islogo(66)}</div>'
            f'<span style="color:{col}">{dots(N, pg)}</span></div>')

def feature_slide(pg, i0, dark):
    icb = ("background:var(--y)", "#000") if dark else ("background:#000", "var(--y)")
    blocks = ""
    for k, i in enumerate((i0, i0 + 1)):
        t, tag, d = FEATURES[i]
        pill = (f'<span class="pill" style="background:{"#fff" if dark else "#000"};color:{"#000" if dark else "#fff"}">{tag.upper()}</span>') if tag else ""
        border = f'border-top:3px solid {"rgba(255,255,255,.16)" if dark else "#000"};' if k else ""
        txt = (f'<div class="tx"><div style="display:flex;align-items:center;gap:22px">'
               f'<div class="ic" style="{icb[0]};stroke:{icb[1]}">{ICONS[i]}</div><div class="num">{i+1:02d}</div></div>'
               f'<h2>{t}{pill}</h2><p style="opacity:{.82 if dark else .88}">{d}</p></div>')
        vis = f'<div class="v">{V[i]}</div>'
        blocks += f'<div class="blk" style="{border}{"flex-direction:row-reverse" if k else ""}">{txt}{vis}</div>'
    deco = waves("#F3BD48", .13 if dark else .30, w=1500, top=430, right=-330, rot=-9)
    return page(1080, 1350, "k" if dark else "w", f"""{deco}
{head(dark, pg)}
<div style="position:relative;z-index:2;padding:30px 64px 8px;flex:1;min-height:0;display:flex;flex-direction:column">
  <div class="chip" style="color:{'#fff' if dark else '#000'}">{GROUPS[i0//2].upper()}<span style="font-weight:400;opacity:.6;letter-spacing:.06em;margin-left:6px">· {i0+1:02d}–{i0+2:02d} / 12</span></div>
  {blocks}
</div>
{footer('fy' if dark else 'fk', 104, addr=False)}""", EXTRA)

# ---------------- KAPAK ----------------
phone = (f'<div class="mk" style="width:470px;height:960px;right:-40px;top:290px;transform:rotate(-6deg)">'
         f'<img src="{APP.as_uri()}" style="width:100%;display:block;margin-top:-62px"></div>')
cover = page(1080, 1350, "k", f"""
{waves('#F3BD48', .14, w=1000, top=-40, right=-380, rot=10)}
<div class="hd"><img src="{logo('yatay_siyah-zemin')}" style="height:104px;margin-left:-12px"><span style="color:var(--y)">{dots(N,0)}</span></div>
{phone}
<div style="position:relative;z-index:2;padding:0 64px;margin-top:96px;max-width:620px">
  <span class="tag" style="background:var(--y);color:#000">DANIŞMANLARIMIZA ÖZEL</span>
  <div style="margin:34px 0 0 -14px">{islogo(230)}</div>
  <h1 style="font-weight:800;font-size:54px;line-height:1.08;margin-top:26px">Gayrimenkul<br>Danışmanının<br>Dijital Asistanı</h1>
  <div style="display:flex;align-items:center;gap:22px;margin-top:48px">
    <div style="font-weight:900;font-size:110px;line-height:.85;color:var(--y)">12</div>
    <div style="font-weight:500;font-size:30px;line-height:1.25">araç,<br>tek platformda.</div>
  </div>
</div>
<div style="margin-top:auto;position:relative;z-index:2;padding:0 64px 56px;font-weight:700;font-size:30px;color:var(--y);letter-spacing:.08em">KAYDIRIN →</div>""", EXTRA)

# ---------------- KAPANIŞ ----------------
closing = page(1080, 1350, "y", f"""
{waves('#000', .07, w=1100, bottom=150, right=-300, rot=-6)}
<div class="hd"><img src="{logo('yatay_sari-zemin')}" style="height:112px;margin-left:-14px">{dots(N, N-1)}</div>
<div style="position:relative;z-index:2;padding:0 64px;margin-top:80px">
  <div style="margin-left:-12px">{islogo(200)}</div>
  <div style="margin-top:40px;display:flex;flex-direction:column;gap:6px;font-weight:900;font-size:76px;line-height:1.05">
    <div>İşini planla.</div><div>Performansını ölç.</div><div style="background:#000;color:var(--y);align-self:flex-start;padding:4px 20px 10px;margin-left:-20px;margin-top:6px">Hedeflerini yönet.</div>
  </div>
  <div style="display:flex;gap:16px;margin-top:44px">
    <span class="tag" style="background:#000;color:#fff;font-size:24px">WEB</span><span class="tag" style="background:#000;color:#fff;font-size:24px">MOBİL</span>
  </div>
  <p style="font-weight:500;font-size:34px;margin-top:22px">Web ve mobilde, gayrimenkul danışmanının yanında.</p>
</div>
<div style="margin-top:auto;position:relative;z-index:2;background:#000;color:#fff;padding:40px 64px 44px">
  <div style="font-weight:700;font-size:24px;letter-spacing:.12em;color:var(--y)">EKİBİMİZE KATILMAK İÇİN</div>
  <div style="display:flex;align-items:center;gap:40px;margin-top:16px;font-weight:800;font-size:44px">
    <span style="display:flex;align-items:center;gap:16px;stroke:var(--y)"><span style="display:inline-flex;width:44px">{PH}</span>{PHONE}</span>
    <span style="display:flex;align-items:center;gap:14px;stroke:var(--y);font-weight:700;font-size:34px"><span style="display:inline-flex;width:38px">{IGI}</span>{IG}</span>
  </div>
</div>""", EXTRA + ".c span svg{height:auto}")

pages = {"01_kapak": cover}
for s in range(6):
    pages[f"{s+2:02d}_ozellik_{2*s+1:02d}-{2*s+2:02d}"] = feature_slide(s + 1, 2 * s, dark=bool(s % 2))
pages["08_kapanis"] = closing

if __name__ == "__main__":
    render({k: pages[k] for k in (sys.argv[2:] or pages)}, sys.argv[1])
