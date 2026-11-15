#!/usr/bin/env python3
"""Mars-themed pixel banner for Awesome Craft Mars."""
import random
from pathlib import Path

random.seed(7)
P = 8
W = 100
H = 34  # 800x272
out = []


def r(x, y, w, h, c, cls=None, extra=""):
    a = f' class="{cls}"' if cls else ""
    out.append(
        f'<rect x="{x*P}" y="{y*P}" width="{w*P}" height="{h*P}" fill="{c}"{a}{extra}/>'
    )


# 3x5 pixel font
F = {
    "A": ["010", "101", "111", "101", "101"],
    "C": ["011", "100", "100", "100", "011"],
    "E": ["111", "100", "110", "100", "111"],
    "F": ["111", "100", "110", "100", "100"],
    "M": ["101", "111", "101", "101", "101"],
    "P": ["110", "101", "110", "100", "100"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"],
    "T": ["111", "010", "010", "010", "010"],
    " ": ["000", "000", "000", "000", "000"],
}

style = """
<style>
.tw{animation:tw 2.4s steps(2) infinite}
.tw2{animation:tw 3.1s steps(2) infinite .8s}
.tw3{animation:tw 1.9s steps(2) infinite 1.4s}
@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}
.glow{animation:glow 1.8s steps(3) infinite}
@keyframes glow{0%,100%{opacity:.3}50%{opacity:1}}
.rover{animation:rover 6s steps(6) infinite}
@keyframes rover{0%,100%{transform:translate(0,0)}50%{transform:translate(16px,0)}}
.dust{animation:dust 2.2s steps(3) infinite}
@keyframes dust{0%,100%{opacity:.15}50%{opacity:.55}}
.blink{animation:tw 1s steps(1) infinite}
</style>
"""

# Thin Martian twilight sky
sky = ["#1a0a08", "#2a100c", "#3a160e", "#4a1c10", "#5c2414", "#6e2c16", "#7a3418"]
for i, c in enumerate(sky):
    r(0, i * 3, W, 3 if i < 6 else 5, c)

# Pale sun / disk
r(82, 4, 5, 5, "#f4a88a")
r(83, 5, 3, 3, "#fde0a8")
r(84, 6, 1, 1, "#fff3c4")

# Stars, keep the title band clear
for i in range(28):
    while True:
        x = random.randrange(W)
        y = random.randrange(10)
        if not (18 <= x <= 82 and y <= 8):
            break
    r(x, y, 1, 1, random.choice(["#fde68a", "#fecaca", "#e2e8f0"]), random.choice(["tw", "tw2", "tw3"]))

# Title: CRAFT MARS
t = "CRAFT MARS"
tx = (W - len(t) * 4) // 2
ty = 2
for k, ch in enumerate(t):
    for yy, row in enumerate(F[ch]):
        for xx, b in enumerate(row):
            if b == "1":
                r(tx + k * 4 + xx + 0.25, ty + yy + 0.25, 1, 1, "#3b0d08", None, ' opacity=".55"')
                r(tx + k * 4 + xx, ty + yy, 1, 1, "#fde68a")

# Distant cratered ridge
for x in range(W):
    hgt = 1 + ((x * 3 + x // 5) % 7 == 0) + ((x // 11) % 3 == 0)
    r(x, 22 - hgt, 1, hgt, "#6b2a16")
r(0, 22, W, 1, "#8a3a1c")

# Ground bands
r(0, 23, W, 2, "#9a4a24")
r(0, 25, W, 2, "#b85a2a")
for x in range(0, W, 3):
    r(x, 24, 1, 1, "#c46a32")
    r(x + 1, 26, 1, 1, "#8a3a1c")

# Habitat dome cluster (generic, no markings)
# left dome
r(16, 18, 9, 1, "#e2e8f0")
r(15, 19, 11, 2, "#cbd5e1")
r(16, 21, 9, 2, "#94a3b8")
r(19, 17, 3, 1, "#f8fafc")
r(18, 20, 1, 1, "#38bdf8", "glow")
r(21, 20, 1, 1, "#38bdf8", "glow")
r(17, 23, 7, 1, "#64748b")
# airlock tube
r(24, 21, 4, 2, "#94a3b8")
# right dome
r(28, 19, 7, 1, "#e2e8f0")
r(27, 20, 9, 3, "#cbd5e1")
r(30, 18, 3, 1, "#f8fafc")
r(31, 21, 1, 1, "#38bdf8", "glow")
r(28, 23, 7, 1, "#64748b")
# small plant bay glow
r(29, 22, 2, 1, "#4ade80", "glow")

# Antenna / weather mast
r(40, 16, 1, 7, "#64748b")
r(39, 16, 3, 1, "#94a3b8")
r(40, 15, 1, 1, "#f87171", "glow")

# Generic six-wheel rover (no agency marks), rolling
out.append('<g class="rover">')
# body
r(58, 19, 8, 3, "#e2e8f0")
r(59, 18, 6, 1, "#f8fafc")
r(61, 17, 2, 1, "#cbd5e1")
# mast cam
r(64, 16, 1, 2, "#64748b")
r(64, 15, 2, 1, "#94a3b8")
r(65, 15, 1, 1, "#38bdf8", "glow")
# wheels
for wx in (57, 60, 63):
    r(wx, 22, 2, 2, "#1e293b")
    r(wx, 22, 2, 1, "#334155")
out.append("</g>")
# dust behind wheels
r(54, 23, 3, 1, "#d97706", "dust")
r(52, 24, 2, 1, "#f59e0b", "dust")

# Metal grid floor in rust-dark
for x in range(W):
    r(x, 27, 1, 1, "#7c2d12" if x % 4 == 0 else "#1c0b08")
    for y in range(28, H):
        if (x + y) % 4 == 0:
            r(x, y, 1, 1, "#3b140c")
        else:
            r(x, y, 1, 1, "#140806")

out.append(
    f'<text x="{8}" y="{H*P-8}" font-family="monospace" font-size="12" fill="#fde68a">'
    f"&gt; facts solid, goals dashed, estimates dotted"
    f'<tspan class="blink">_</tspan></text>'
)

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*P} {H*P}" '
    f'width="{W*P}" height="{H*P}" shape-rendering="crispEdges">'
    + style
    + "".join(out)
    + "</svg>"
)

dest = Path(__file__).resolve().parent / "assets" / "craft-mars.svg"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(svg)
print(f"wrote {dest} ({dest.stat().st_size} bytes)")
