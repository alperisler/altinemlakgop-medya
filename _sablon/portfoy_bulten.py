"""Haftalık Portföy Bülteni — satılık ve kiralık için ayrı carousel (4:5).
Kullanım: python3 portfoy_bulten.py <çıktı_klasörü>
Veri: portfoy_veri.json  · Fotoğraflar: foto/<id>.jpg  · EİDS logosu: logo/eids.png
"""
import json, sys, pathlib
from build import page, logo, render, PHONE, PIN

KIT = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else KIT / "out")
V = json.loads((KIT / "portfoy_veri.json").read_text())
MAX_SAYFA = 20  # Instagram carousel sınırı (kapak dahil)

def tl(v):
    return f"{int(v):,}".replace(",", ".")

def foto(p): return (KIT / "foto" / p["foto"]).as_uri()

CSS = """
.ph{position:absolute;left:0;top:0;width:1080px;height:880px;object-fit:cover}
.shade{position:absolute;left:0;top:0;width:1080px;height:880px;
 background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 62%,rgba(0,0,0,.55) 100%)}
.top{position:absolute;top:44px;left:48px;right:48px;display:flex;justify-content:space-between;align-items:center}
.pill{font-weight:800;font-size:28px;letter-spacing:.14em;padding:14px 24px;border-radius:999px}
.cnt{font-weight:700;font-size:28px;color:#fff;background:rgba(0,0,0,.55);padding:12px 22px;border-radius:999px;letter-spacing:.06em}
.price{position:absolute;z-index:5;left:48px;top:790px;background:var(--y);color:#000;padding:22px 34px 18px;border-radius:14px;
 box-shadow:0 18px 40px rgba(0,0,0,.35);display:flex;align-items:baseline;gap:14px}
.price b{font-weight:900;font-size:92px;line-height:1;letter-spacing:-.01em}
.price s{text-decoration:none;font-weight:800;font-size:40px}
.panel{position:absolute;left:0;top:880px;width:1080px;height:470px;background:#000;color:#fff;padding:100px 48px 0}
.ttl{font-weight:800;font-size:52px;line-height:1.05;letter-spacing:-.005em;max-width:860px}
.loc{display:flex;align-items:center;gap:12px;font-weight:500;font-size:30px;margin-top:16px;color:#ddd}
.loc svg{width:32px;height:32px;stroke:var(--y)}
.chips{display:flex;gap:12px;margin-top:20px;flex-wrap:wrap}
.chip{border:2px solid #444;border-radius:10px;padding:8px 16px;font-weight:700;font-size:26px}
.chip.kc{background:var(--y);color:#000;border-color:var(--y)}
.chip i{font-style:normal;color:var(--y)}
.bot{position:absolute;left:48px;right:48px;bottom:30px;display:flex;align-items:flex-end;justify-content:space-between}
.no{font-weight:500;font-size:22px;color:#999;letter-spacing:.04em;margin-top:8px}
.yld{position:absolute;right:48px;top:118px;z-index:6;background:#000;color:#fff;border:3px solid var(--y);border-radius:14px;padding:18px 24px;width:400px}
.yld .h{font-weight:900;font-size:24px;letter-spacing:.14em;color:var(--y)}
.yld .r{font-weight:800;font-size:30px;margin-top:6px;line-height:1.15}
.yld .r{font-size:38px}
.yld .st{display:flex;gap:18px;margin-top:12px;border-top:1px solid #444;padding-top:12px}
.yld .st div{font-weight:600;font-size:20px;color:#bbb;letter-spacing:.04em}
.yld .st b{display:block;font-weight:900;font-size:34px;color:#fff;letter-spacing:0}
.ag{display:flex;align-items:center;gap:16px}
.ag img.av{width:96px;height:96px;border-radius:50%;object-fit:cover;border:4px solid var(--y)}
.ag .l{font-weight:600;font-size:20px;color:#999;letter-spacing:.08em}
.ag .n{font-weight:800;font-size:32px;color:#fff;line-height:1.1}
.rb{display:flex;align-items:center;gap:22px}
.eids{width:118px;height:118px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}
.eids img{width:112px;height:112px}
"""

def getiri(p):
    """Satılıkta açıklamada kira varsa: (aylık kira, brüt getiri %, amortisman yılı)."""
    if p["durum"] != "Satılık" or not p.get("kira_ay"): return None
    yil = p["kira_ay"] * 12
    return p["kira_ay"], yil / p["fiyat"] * 100, p["fiyat"] / yil

def ondalik(x, d=1):
    return f"{x:.{d}f}".rstrip("0").rstrip(".").replace(".", ",")

def sayfa(p, i, n, renk):
    fiyat = tl(p["fiyat"]) + " ₺"
    ek = '<s>/ ay</s>' if p["durum"] == "Kiralık" else ""
    chips = []
    if p.get("oda"): chips.append(f'<span class="chip">{p["oda"]}</span>')
    if p["tur"] in ("Arsa", "Tarla"):
        chips.append(f'<span class="chip">{tl(p["brut"])} <i>m²</i></span>')
    else:
        chips.append(f'<span class="chip">{p["brut"]} <i>m²</i> brüt · {p["net"]} <i>m²</i> net</span>')
    if p.get("kat"):
        k = p["kat"]; chips.append(f'<span class="chip">{k}{". kat" if k.isdigit() else ""}</span>')
    chips.append(f'<span class="chip">{p["tur"]}</span>')
    if p.get("kiracili") and p["durum"] == "Satılık": chips.insert(0, '<span class="chip kc">KİRACILI</span>')
    g = getiri(p); yld = ""
    if g:
        k, gt, am = g
        h = "TAHMİNİ KİRA POTANSİYELİ" if p.get("kira_tahmini") else "MEVCUT KİRA GELİRİ"
        yld = (f'<div class="yld"><div class="h">{h}</div><div class="r">{tl(k)} ₺ / ay'
               f'</div><div class="st"><div>BRÜT GETİRİ<b>%{ondalik(gt)}</b></div><div>AMORTİSMAN<b>~{ondalik(am)} yıl</b></div></div></div>')
    eids = f'<div class="eids"><img src="{logo("eids")}"></div>'  # kullanıcı isteği: tüm portföylerde EİDS logosu
    pill_bg = "background:var(--y);color:#000" if renk == "s" else "background:#fff;color:#000"
    return page(1080, 1350, "k", f"""
<img class="ph" src="{foto(p)}"><div class="shade"></div>
<div class="top"><span class="pill" style="{pill_bg}">{p['durum'].upper()}</span><span class="cnt">{i:02d} / {n:02d}</span></div>
<div class="price"><b>{fiyat}</b>{ek}</div>{yld}
<div class="panel">
  <div class="ttl">{p['baslik']}</div>
  <div class="loc">{PIN}{p['mahalle']} · {p['ilce']}</div>
  <div class="chips">{''.join(chips)}</div>
</div>
<div class="bot">
  <div class="ag"><img class="av" src="{(KIT / 'danisman' / p['danisman_foto']).as_uri()}"><div><div class="l">PORTFÖY DANIŞMANI</div><div class="n">{p['danisman']}</div><div class="no">Portföy No {p['no']} · {PHONE}</div></div></div>
  <div class="rb"><img src="{logo('yatay_siyah-zemin')}" style="height:62px">{eids}</div>
</div>""", CSS)

KCSS = """
.bgp{position:absolute;inset:0}
.mast{position:absolute;left:56px;right:56px;top:48px;display:flex;justify-content:space-between;align-items:center}
.issue{font-weight:800;font-size:26px;letter-spacing:.16em;padding:12px 20px;border:3px solid currentColor;border-radius:8px}
.rule{position:absolute;left:56px;right:56px;top:178px;height:6px;background:currentColor}
.kick{position:absolute;right:56px;top:200px;font-weight:800;font-size:34px;letter-spacing:.22em}
.big{position:absolute;left:46px;top:276px;font-weight:900;font-size:228px;line-height:.82;letter-spacing:-.035em}
.big2{position:absolute;left:52px;top:466px;font-weight:900;font-size:96px;line-height:.9;letter-spacing:-.01em}
.cards{position:absolute;left:0;top:600px;width:1080px;height:600px}
.cd{position:absolute;width:330px;height:470px;background:#fff;padding:16px 16px 0;border-radius:10px;box-shadow:0 30px 60px rgba(0,0,0,.45)}
.cd img{width:298px;height:320px;object-fit:cover;border-radius:4px;display:block}
.cd .pr{margin-top:14px;font-weight:900;font-size:40px;color:#000;line-height:1}
.cd .pr s{text-decoration:none;font-size:24px;font-weight:800}
.cd .lb{font-weight:600;font-size:22px;color:#555;margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.stk{position:absolute;right:40px;top:520px;width:230px;height:230px;border-radius:50%;
 display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(12deg);box-shadow:0 18px 40px rgba(0,0,0,.4);z-index:9;border:6px dashed rgba(0,0,0,.25)}
.stk b{font-weight:900;font-size:110px;line-height:.85}
.stk span{font-weight:800;font-size:26px;letter-spacing:.1em;text-align:center;line-height:1.1}
.bar{position:absolute;left:0;right:0;bottom:0;height:150px;display:flex;align-items:center;justify-content:space-between;padding:0 56px}
.bar .t{font-weight:800;font-size:34px}
.bar .t small{display:block;font-weight:500;font-size:24px;opacity:.75;margin-top:4px}
.swipe{font-weight:900;font-size:34px;padding:20px 32px;border-radius:999px}
"""

def kapak(lst, durum):
    import math
    kir = durum == "Kiralık"
    bg, fg, acc = ("#F3BD48", "#000", "#000") if kir else ("#000", "#fff", "#F3BD48")
    rays = "".join(
        f'<path d="M540,900 L{540+2200*math.cos(2*math.pi*i/32):.0f},{900+2200*math.sin(2*math.pi*i/32):.0f} '
        f'L{540+2200*math.cos(2*math.pi*(i+1)/32):.0f},{900+2200*math.sin(2*math.pi*(i+1)/32):.0f} Z" '
        f'fill="{"#000" if kir else "#F3BD48"}" opacity="{.07 if kir else .09}"/>' for i in range(0, 32, 2))
    sec = lst[:3]
    pos = [(48, 70, -7), (375, 30, 1), (702, 90, 7)]
    cards = ""
    for (x, y, r), p in zip(pos, sec):
        pr = tl(p["fiyat"]) + " ₺" + ("<s> / ay</s>" if kir else "")
        cards += (f'<div class="cd" style="left:{x}px;top:{y}px;transform:rotate({r}deg)">'
                  f'<img src="{foto(p)}"><div class="pr">{pr}</div>'
                  f'<div class="lb">{(p.get("oda") or p["tur"])} · {p["mahalle"]}</div></div>')
    konut = [p["fiyat"] for p in lst if p["tur"] in ("Daire", "Residence")] or [p["fiyat"] for p in lst]
    alt = min(konut)
    alt_txt = (f"{tl(alt)} ₺ / ay" if kir else
               f"{alt/1e6:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " milyon ₺")
    stk_bg = "#000;color:#F3BD48" if kir else "#F3BD48;color:#000"
    bar = "background:#000;color:#fff" if kir else "background:#F3BD48;color:#000"
    sw = "background:#F3BD48;color:#000" if kir else "background:#000;color:#F3BD48"
    lg = "yatay_sari-zemin" if kir else "yatay_siyah-zemin"
    baslik = "KİRALIK" if kir else "SATILIK"
    return page(1080, 1350, "", f"""
<div class="bgp" style="background:{bg}"></div>
<svg viewBox="0 0 1080 1350" style="position:absolute;inset:0;width:1080px;height:1350px">{rays}</svg>
<div class="mast" style="color:{fg}"><img src="{logo(lg)}" style="height:96px;margin-left:-10px"><span class="issue">{V['hafta'].upper()}</span></div>
<div class="rule" style="color:{fg}"></div>
<div class="kick" style="color:{fg}">HAFTALIK</div>
<div class="big" style="color:{acc}">{baslik}</div>
<div class="big2" style="color:{fg}">PORTFÖY BÜLTENİ</div>
<div class="cards">{cards}</div>
<div class="stk" style="background:{stk_bg}"><b>{len(lst)}</b><span>{'KİRALIK' if kir else 'SATILIK'}<br>FIRSAT</span></div>
<div class="bar" style="{bar}"><div class="t">Konutlar {alt_txt}'dan başlıyor<small>Gaziosmanpaşa ve çevresi · fiyatlar her sayfada</small></div>
<span class="swipe" style="{sw}">Kaydır →</span></div>""", KCSS)

def u16(t):
    return len(t.encode("utf-16-le")) // 2

def aciklama(lst, durum):
    """(açıklama, ilk_yorum) döndürür. Linkler TAM adres (kullanıcı isteği).
    Instagram açıklama ve yorum sınırı 2200 (UTF-16); güvenli pay için 2100.
    Açıklamaya sığmayan portföyler ilk yoruma sırayla devam eder."""
    LIM = 2100
    bas = (f"🏠 HAFTALIK PORTFÖY BÜLTENİ · {durum.upper()}\n{V['hafta']}\n\n"
           f"{len(lst)} {durum.lower()} portföy, görsel sırasıyla:\n\n")
    son = (f"\n\n📞 {PHONE} · Altın Emlak Gaziosmanpaşa\n"
           "#gaziosmanpaşa #" + ("satılıkdaire" if durum == "Satılık" else "kiralıkdaire") + " #altinemlakgop")
    devam_not = "\n\n👇 Diğer portföylerin linkleri ilk yorumda."
    satir = []
    for i, p in enumerate(lst, 1):
        f = tl(p["fiyat"]) + " ₺" + (" / ay" if durum == "Kiralık" else "")
        ek = ""
        g = getiri(p)
        if g:
            ek = (f"\n{'Tahmini kira' if p.get('kira_tahmini') else 'Kira'} {tl(g[0])} ₺/ay · "
                  f"%{ondalik(g[1])} getiri · ~{ondalik(g[2])} yıl amortisman")
        kc = " · Kiracılı" if (p.get("kiracili") and durum == "Satılık") else ""
        url = p.get("url") or ("https://www." + p["link"])
        satir.append(f"{i:02d}) {p['baslik']} · {f}{kc}{ek}\n{url}")
    tam = bas + "\n\n".join(satir) + son
    if u16(tam) <= LIM:
        return tam, ""
    # sığdığı kadarını açıklamaya, kalanını ilk yoruma
    k = len(satir)
    while k > 0 and u16(bas + "\n\n".join(satir[:k]) + devam_not + son) > LIM:
        k -= 1
    cap = bas + "\n\n".join(satir[:k]) + devam_not + son
    yorum = "🔗 Devamı:\n\n" + "\n\n".join(satir[k:])
    assert u16(yorum) <= LIM, ("ilk yorum da uzun", u16(yorum))
    return cap, yorum

def uret():
    for durum, kod, ad in (("Satılık", "s", "satilik"), ("Kiralık", "k", "kiralik")):
        lst = [p for p in V["portfoyler"] if p["durum"] == durum][: MAX_SAYFA - 1]
        d = OUT / f"Portföy Bülteni {V['bulten_tarihi']}" / ad
        d.mkdir(parents=True, exist_ok=True)
        pages = {f"{ad}_00-kapak": kapak(lst, durum)}
        for i, p in enumerate(lst, 1):
            pages[f"{ad}_{i:02d}-{p['no']}"] = sayfa(p, i, len(lst), kod)
        render(pages, d)
        txt, yorum = aciklama(lst, durum)
        (d / "aciklama.txt").write_text(txt)
        if yorum: (d / "ilk_yorum.txt").write_text(yorum)
        print(durum, len(lst), "sayfa +1 kapak · açıklama", u16(txt), "· ilk yorum", u16(yorum))

if __name__ == "__main__":
    uret()
