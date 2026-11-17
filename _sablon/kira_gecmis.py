"""Kira artış oranı — son 13 ay (Kasım 2025 → Kasım 2026). Post 4:5 + Story 9:16."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build import page, footer, logo, render, PHONE, PH

DATA = [("Kasım", "2025", 37.15), ("Aralık", "2025", 35.91), ("Ocak", "2026", 34.88), ("Şubat", "2026", 33.98),
        ("Mart", "2026", 33.39), ("Nisan", "2026", 32.82), ("Mayıs", "2026", 32.43), ("Haziran", "2026", 32.24),
        ("Temmuz", "2026", 32.03), ("Ağustos", "2026", 31.90), ("Eylül", "2026", 31.79), ("Ekim", "2026", 31.49),
        ("Kasım", "2026", 31.23)]

def pct(v): return f"%{v:.2f}".replace(".", ",")

EXTRA = """
.rate{font-weight:900;line-height:.86;letter-spacing:-.03em}
.rate small{font-size:.5em;letter-spacing:0;margin-right:.06em;vertical-align:.42em}
.row{display:flex;align-items:center;gap:20px}
.row .mo{flex:none;font-weight:700;letter-spacing:.02em}
.row .mo span{font-weight:400;opacity:.55;margin-left:8px}
.row .tr{flex:1;position:relative}
.row .b{background:#3a3a3a}
.row .v{flex:none;font-weight:800;text-align:right}
.row.on .b{background:var(--y)} .row.on .mo,.row.on .v{color:var(--y)}
.row.first .b{background:#fff}
.c svg{width:100%;height:auto}
.foot svg{width:34px!important;height:34px!important}
"""

def rows(rh, bh, fs, mow, vw):
    lo, hi = 29.5, 37.4
    out = ""
    for i, (m, y, v) in enumerate(DATA):
        cls = "on" if i == len(DATA) - 1 else ("first" if i == 0 else "")
        w = (v - lo) / (hi - lo) * 100
        out += (f'<div class="row {cls}" style="height:{rh}px">'
                f'<div class="mo" style="width:{mow}px;font-size:{fs}px">{m}<span>{y[2:]}</span></div>'
                f'<div class="tr"><div class="b" style="width:{w:.1f}%;height:{bh}px"></div></div>'
                f'<div class="v" style="width:{vw}px;font-size:{fs+2}px">{pct(v)}</div></div>')
    return out

DROP = f"{DATA[0][2]-DATA[-1][2]:.2f}".replace(".", ",")

T = {}
T["kira-gecmis_01_post-4x5"] = page(1080, 1350, "k", f"""
<div style="padding:64px 64px 0;display:flex;justify-content:space-between;align-items:center">
  <img src="{logo('yatay_siyah-zemin')}" style="height:100px;margin-left:-12px">
  <span class="tag" style="background:var(--y);color:#000">SON 12 AY</span>
</div>
<div style="padding:0 64px;margin-top:40px;display:flex;justify-content:space-between;align-items:flex-end">
  <h1 style="font-weight:900;font-size:66px;line-height:1.0">Kasım ayı<br>kira artış oranı</h1>
  <div class="rate" style="font-size:150px;color:var(--y)"><small>%</small>31,23</div>
</div>
<div style="padding:0 64px;margin-top:22px;font-size:27px;font-weight:400;opacity:.85">1 yılda <b style="color:var(--y);font-weight:800">{DROP} puan</b> geriledi · TÜFE 12 aylık ortalama</div>
<div style="padding:0 64px;margin-top:30px">{rows(60, 32, 27, 196, 130)}</div>
{footer('fy', 110, addr=False)}""", EXTRA)

T["kira-gecmis_02_story-9x16"] = page(1080, 1920, "k", f"""
<div style="padding:140px 72px 0"><img src="{logo('yatay_siyah-zemin')}" style="height:116px;margin-left:-12px"></div>
<div style="padding:0 72px;margin-top:70px">
  <span class="tag" style="background:var(--y);color:#000">KİRA ARTIŞ ORANLARI · SON 12 AY</span>
  <h1 style="font-weight:900;font-size:86px;line-height:1.0;margin-top:34px">Kasım ayı<br>kira artış oranı</h1>
  <div class="rate" style="font-size:230px;color:var(--y);margin-top:18px"><small>%</small>31,23</div>
  <div style="font-size:32px;font-weight:400;opacity:.85;margin-top:24px">1 yılda <b style="color:var(--y);font-weight:800">{DROP} puan</b> geriledi</div>
</div>
<div style="padding:0 72px;margin-top:44px">{rows(59, 34, 30, 220, 150)}</div>
<div style="margin-top:auto;height:190px;background:var(--y);color:#000;display:flex;align-items:center;justify-content:center;gap:16px;font-weight:800;font-size:44px;stroke:#000"><span style="display:inline-flex;width:46px">{PH}</span>{PHONE}<span style="font-weight:500;font-size:32px;margin-left:18px">@altinemlakgop</span></div>""", EXTRA)

if __name__ == "__main__":
    render(T, sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent / "out_kira")
