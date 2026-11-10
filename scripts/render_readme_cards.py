#!/usr/bin/env python3
"""
Render the profile README's cards as animated SVGs into cards/.

Design: Paper and ink palette matching the animated SVG cards design
(Instrument Serif, Geist, Geist Mono; paper #f3f3f1, ink #111111,
and theme accents: Tech blue #2f55ff, Studio red #ef3b2d, Learn yellow #ffc81a).

Stand-alone SVGs embedded via <img> tags:
- Inline CSS keyframe animations
- SMIL <animate> / <set> animations
- Subset WOFF fonts embedded as base64 data URIs
- Prefers-reduced-motion fallback
- STATIC=1 support for headless screenshots and instant previews
"""
import base64
import datetime
import json
import os
import re
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
DATA = os.path.join(ROOT, "data", "contributions.json")
OUT = os.path.join(ROOT, "cards")
FONTS = os.path.join(ROOT, "fonts")
PORTRAIT = os.path.join(ROOT, "egor-ascii.svg")

# ---- brand tokens -----------------------------------------------------------
PAPER = "#f3f3f1"
PAPER_DEEP = "#e2e2de"
INK = "#111111"
INK_SOFT = "#3a3a3c"
MUTED = "#6e6e73"
RULE = "#dcdcd7"
TECH = "#2f55ff"      # Blue
STUDIO = "#ef3b2d"    # Red
LEARN = "#ffc81a"     # Yellow
W = 880               # Full README column width

SERIF = "'Instrument Serif', Georgia, serif"
SANS = "Geist, system-ui, -apple-system, sans-serif"
MONO = "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace"

FONT_FILES = {
    "serif": ("Instrument Serif", "normal", 400, "serif-400.woff"),
    "serif-i": ("Instrument Serif", "italic", 400, "serif-italic.woff"),
    "sans": ("Geist", "normal", 400, "geist-400.woff"),
    "sans-b": ("Geist", "normal", 600, "geist-600.woff"),
    "mono": ("Geist Mono", "normal", 400, "geistmono-400.woff"),
}

BASE_CSS = """
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pop{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.15)}100%{opacity:1;transform:none}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes nudge{0%,100%{transform:none}50%{transform:translateX(4px)}}
@keyframes nudgeup{0%,100%{transform:none}50%{transform:translate(3px,-3px)}}
.r{opacity:0;animation:rise .8s cubic-bezier(.2,.7,.2,1) both;transform-box:fill-box}
.f{opacity:0;animation:fade .9s ease-out both}
.g{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .8s cubic-bezier(.2,.7,.2,1) both}
.p{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s ease-out both}
.live{animation:pulse 1.6s ease-in-out infinite}
.n{transform-box:fill-box;animation:nudge 1.8s ease-in-out infinite}
.nu{transform-box:fill-box;animation:nudgeup 1.8s ease-in-out infinite}
@keyframes tilein{0%{opacity:0;transform:translateY(90px) scale(.6) rotate(-9deg)}55%{opacity:1;transform:translateY(-10px) scale(1.05) rotate(2deg)}75%{transform:translateY(3px) scale(.98) rotate(-.8deg)}90%{transform:translateY(-1px) scale(1.01) rotate(.2deg)}100%{opacity:1;transform:none}}
@keyframes slidein{from{opacity:0;transform:translateX(-26px)}to{opacity:1;transform:none}}
@keyframes arrowin{0%{opacity:0;transform:translateX(-30px)}60%{opacity:1;transform:translateX(6px)}100%{opacity:1;transform:none}}
@keyframes roll{from{transform:translateY(60px)}to{transform:none}}
@keyframes sheen{0%{transform:translateX(-260px) skewX(-20deg)}22%,100%{transform:translateX(420px) skewX(-20deg)}}
@keyframes ring{0%{opacity:.7;transform:scale(.2)}100%{opacity:0;transform:scale(2.4)}}
.ti{opacity:0;transform-box:fill-box;transform-origin:50% 60%;animation:tilein 1.1s cubic-bezier(.2,.8,.2,1) both}
.sl{opacity:0;transform-box:fill-box;animation:slidein .6s cubic-bezier(.2,.7,.2,1) both}
.ai{opacity:0;transform-box:fill-box;animation:arrowin .7s cubic-bezier(.2,.7,.2,1) both}
.ro{transform-box:fill-box;animation:roll .8s cubic-bezier(.15,.8,.2,1) both}
.sh{animation:sheen 5s ease-in-out infinite}
.rg{opacity:0;transform-box:fill-box;transform-origin:center;animation:ring 1s ease-out both}
@media (prefers-reduced-motion: reduce){.r,.f,.g,.p,.live,.n,.nu,.ti,.sl,.ai,.ro,.rg{animation:none!important;opacity:1!important;transform:none!important}.sh,.rg{display:none}}
"""


def font_face(keys):
    out = []
    for k in keys:
        fam, style, weight, fn = FONT_FILES[k]
        font_path = os.path.join(FONTS, fn)
        if os.path.exists(font_path):
            b64 = base64.b64encode(open(font_path, "rb").read()).decode()
            out.append(
                f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
                f"src:url(data:font/woff;base64,{b64}) format('woff')}}"
            )
    return "".join(out)


GAP = 12
BOTTOM = 12
COL = W / 3


def svg(w, h, body, fonts, label, extra_css="", left=0, right=0, bottom=BOTTOM):
    if left:
        body = f'<g transform="translate({left:.3f} 0)">{body}</g>'
    w, h = w + left + right, h + bottom
    css = font_face(fonts) + BASE_CSS + extra_css
    if os.environ.get("STATIC"):
        css += (
            ".r,.f,.g,.p,.live,.n,.nu,.ti,.sl,.ai,.ro{animation:none!important;opacity:1!important;transform:none!important}"
            ".sh,.rg{display:none}"
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}" height="{h}" viewBox="0 0 {w:.3f} {h}" '
        f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
        f"<style>{css}</style>{body}</svg>"
    )


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"wrote cards/{name} ({len(content) // 1024} KB)")


def d(s):
    return f'style="animation-delay:{s:.2f}s"'


def wrap(text, n):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > n:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line] if line else lines


def text_lines(x, y, lines, lh, attrs):
    return "".join(
        f'<text x="{x}" y="{y + i * lh}" {attrs}>{escape(l)}</text>' for i, l in enumerate(lines)
    )


# ---- 1 · hero -----------------------------------------------------------------
def hero():
    h = 420
    portrait = []
    if os.path.exists(PORTRAIT):
        src = open(PORTRAIT).read()
        rows = re.findall(r'<text xml:space="preserve"[^>]*\by="([\d.]+)"[^>]*>(.*?)</text>', src, re.S)
        for i, (y, txt) in enumerate(rows):
            portrait.append(
                f'<text class="f" style="animation-delay:{0.25 + i * 0.018:.3f}s;animation-duration:.35s" '
                f'xml:space="preserve" x="20" y="{y}" fill="{INK}" font-size="7.2" '
                f'textLength="800" lengthAdjust="spacing">{txt}</text>'
            )

    s = 0.41
    body = f"""
<defs>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0">
    <stop offset="0" stop-color="{INK}"/><stop offset=".42" stop-color="{INK}"/>
    <stop offset=".5" stop-color="{TECH}"/><stop offset=".58" stop-color="{INK}"/>
    <stop offset="1" stop-color="{INK}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-600 0;600 0;600 0"
      keyTimes="0;.45;1" dur="7s" begin="1.6s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<rect width="{W}" height="{h}" rx="14" fill="{PAPER}"/>
<g class="f" {d(0)}>
  <rect class="live" x="48" y="49" width="8" height="8" rx="2" fill="{TECH}"/>
  <text x="66" y="57" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{MUTED}">PYTHON DEVELOPER (BACKEND / AI AUTOMATION)</text>
</g>
<text class="r" {d(0.15)} x="44" y="190" font-family="{SERIF}" font-size="116" letter-spacing="-2.5" fill="{INK}">Egor</text>
<text class="r" {d(0.3)} x="44" y="290" font-family="{SERIF}" font-style="italic" font-size="116" letter-spacing="-2.5" fill="url(#shine)">Fominykh</text>
<g class="r" {d(0.55)}>
  {text_lines(48, 338, ["Backend architecture, AI & RAG evaluation,", "web scraping and DevSecOps automation."], 27, f'font-family="{SANS}" font-size="18" fill="{INK_SOFT}"')}
</g>
<g class="f" {d(0.8)}>
  <text x="48" y="396" font-family="{MONO}" font-size="12" fill="{INK}">t.me/egorfm</text>
  <text class="nu" x="136" y="396" font-family="{MONO}" font-size="12" fill="{TECH}">&#8599;</text>
  <text x="160" y="396" font-family="{MONO}" font-size="12" fill="{MUTED}">·</text>
  <text x="176" y="396" font-family="{MONO}" font-size="12" fill="{INK}">linkedin.com/in/egor-fominykh-b66825449</text>
  <text class="nu" x="464" y="396" font-family="{MONO}" font-size="12" fill="{TECH}">&#8599;</text>
</g>
<g transform="translate(520 46) scale({s}) translate(-20 -37)" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  {''.join(portrait)}
</g>
"""
    card_svg = svg(
        W,
        h,
        body,
        ["serif", "serif-i", "sans", "mono"],
        "Egor Fominykh. Python Developer (Backend / AI Automation).",
    )
    write("hero.svg", card_svg)
    write("hero-v3.svg", card_svg)
    write("hero-card.svg", card_svg)


# ---- 2 · world tiles ----------------------------------------------------------
TILE_W, TILE_H = 880 / 3 - 8, 210


def count_up(num, word, x, y, attrs, begin, dur=1.1, frames=18):
    m = re.match(r"([\d.]+)(.*)", num)
    tail = f' <tspan font-style="italic">{escape(word)}</tspan>'
    if not m or os.environ.get("STATIC"):
        return f'<text x="{x}" y="{y}" {attrs}>{escape(num)}{tail}</text>'
    val, suf = float(m.group(1)), m.group(2)
    dec = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
    out = []
    for i in range(frames + 1):
        e = 1 - (1 - i / frames) ** 3
        txt = num if i == frames else f"{val * e:.{dec}f}{suf}"
        on = begin + dur * i / frames
        off = "" if i == frames else f'<set attributeName="opacity" to="0" begin="{begin + dur * (i + 1) / frames:.3f}s"/>'
        out.append(
            f'<text x="{x}" y="{y}" {attrs} opacity="0">{escape(txt)}{tail}'
            f'<set attributeName="opacity" to="1" begin="{on:.3f}s"/>{off}</text>'
        )
    return "".join(out)


def tile_avito(pos=0):
    name = "avito-ml-cup"
    label = "AVITOTECH"
    on = "#ffffff"
    delay = 3.1
    blurb = "Personalized recommendation feed ranking with CatBoost and 33 behavioral features."
    lines = wrap(blurb, 34)
    blurb_svg = "".join(
        f'<text class="r" {d(delay + 0.75 + i * 0.1)} x="24" y="{150 + i * 20}" font-family="{SANS}" '
        f'font-size="14" fill="{on}" opacity=".92">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    body = f"""
<defs>
  <clipPath id="card-{name}"><rect width="{TILE_W}" height="{TILE_H}" rx="14"/></clipPath>
  <clipPath id="slot-{name}"><rect x="0" y="62" width="{TILE_W}" height="62"/></clipPath>
  <linearGradient id="bg-{name}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0b0d26"/>
    <stop offset=".55" stop-color="#151744"/>
    <stop offset="1" stop-color="#3b1778"/>
  </linearGradient>
  <linearGradient id="gl-{name}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<g class="ti" {d(delay)}>
  <g clip-path="url(#card-{name})">
    <rect width="{TILE_W}" height="{TILE_H}" fill="url(#bg-{name})"/>
    <ellipse cx="260" cy="50" rx="90" ry="60" fill="none" stroke="#8b5cf6" stroke-width="26" opacity="0.32" transform="rotate(-30 260 50)"/>
    <circle class="rg" {d(delay + 0.5)} cx="{TILE_W - 40}" cy="{TILE_H - 40}" r="60" fill="none" stroke="#a78bfa" stroke-opacity=".3" stroke-width="2"/>
    <rect class="sh" style="animation-delay:{delay + 1.4:.2f}s" x="0" y="-20" width="90" height="{TILE_H + 40}" fill="url(#gl-{name})" transform="translate(-260 0)"/>
  </g>
  <!-- Avito 4 colored dots -->
  <g class="sl" {d(delay + 0.35)}>
    <circle cx="27" cy="35" r="3.2" fill="#00aa44"/>
    <circle cx="35" cy="35" r="3.2" fill="#0099ff"/>
    <circle cx="43" cy="35" r="3.2" fill="#ff4053"/>
    <circle cx="51" cy="35" r="3.2" fill="#8033ff"/>
    <text x="63" y="38" font-family="{MONO}" font-size="12" letter-spacing="1.2" fill="{on}">{escape(label)}</text>
  </g>
  <g class="ai" {d(delay + 0.5)}><text class="n" style="animation-delay:{delay + 1.3:.2f}s" x="250" y="38" font-family="{MONO}" font-size="14" fill="{on}">&#8594;</text></g>
  <g clip-path="url(#slot-{name})"><g class="ro" {d(delay + 0.45)}>
    <text x="22" y="112" font-family="{SERIF}" font-size="44" fill="{on}">ML Cup <tspan font-style="italic">2026</tspan></text>
  </g></g>
  {blurb_svg}
</g>
"""
    svg_data = svg(
        TILE_W,
        TILE_H,
        body,
        ["serif", "serif-i", "sans", "mono"],
        f"{label}: ML Cup 2026. {blurb}",
        left=4 * pos,
        right=8 - 4 * pos,
    )
    write(f"{name}.svg", svg_data)
    write("build.svg", svg_data)


def tile_nfl(pos=1):
    name = "nfl-big-data-bowl"
    label = "NFL BIG DATA BOWL"
    on = "#ffffff"
    delay = 3.35
    blurb = "10Hz RFID & NGS tracking separation with BRK+ kinematic deceleration metric."
    lines = wrap(blurb, 34)
    blurb_svg = "".join(
        f'<text class="r" {d(delay + 0.75 + i * 0.1)} x="24" y="{150 + i * 20}" font-family="{SANS}" '
        f'font-size="14" fill="{on}" opacity=".92">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    body = f"""
<defs>
  <clipPath id="card-{name}"><rect width="{TILE_W}" height="{TILE_H}" rx="14"/></clipPath>
  <clipPath id="slot-{name}"><rect x="0" y="62" width="{TILE_W}" height="62"/></clipPath>
  <linearGradient id="gl-{name}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<g class="ti" {d(delay)}>
  <g clip-path="url(#card-{name})">
    <rect width="{TILE_W}" height="{TILE_H}" fill="#c8102e"/>
    <!-- Top corner NFL Navy accent tab -->
    <polygon points="175,0 {TILE_W},0 {TILE_W},18 195,18" fill="#013369"/>
    <!-- Gridiron yard lines -->
    <line x1="0" y1="126" x2="{TILE_W}" y2="126" stroke="#ffffff" stroke-opacity="0.22" stroke-dasharray="6,8" stroke-width="1.5"/>
    <line x1="210" y1="0" x2="210" y2="70" stroke="#ffffff" stroke-opacity="0.14" stroke-width="1"/>
    <circle class="rg" {d(delay + 0.5)} cx="{TILE_W - 40}" cy="{TILE_H - 40}" r="60" fill="none" stroke="#ffffff" stroke-opacity=".35" stroke-width="2"/>
    <rect class="sh" style="animation-delay:{delay + 1.4:.2f}s" x="0" y="-20" width="90" height="{TILE_H + 40}" fill="url(#gl-{name})" transform="translate(-260 0)"/>
  </g>
  <text class="sl" {d(delay + 0.35)} x="24" y="38" font-family="{MONO}" font-size="12" letter-spacing="1.2" fill="{on}">{escape(label)}</text>
  <g class="ai" {d(delay + 0.5)}><text class="n" style="animation-delay:{delay + 1.3:.2f}s" x="250" y="38" font-family="{MONO}" font-size="14" fill="{on}">&#8594;</text></g>
  <g clip-path="url(#slot-{name})"><g class="ro" {d(delay + 0.45)}>
    {count_up("2027", "Research", 22, 112, f'font-family="{SERIF}" font-size="44" fill="{on}"', delay + 0.45)}
  </g></g>
  {blurb_svg}
</g>
"""
    svg_data = svg(
        TILE_W,
        TILE_H,
        body,
        ["serif", "serif-i", "sans", "mono"],
        f"{label}: 2027 Research. {blurb}",
        left=4 * pos,
        right=8 - 4 * pos,
    )
    write(f"{name}.svg", svg_data)
    write("brand.svg", svg_data)


def tile(name, label, color, on, num, word, blurb, delay, pos):
    lines = wrap(blurb, 34)
    blurb_svg = "".join(
        f'<text class="r" {d(delay + 0.75 + i * 0.1)} x="24" y="{150 + i * 20}" font-family="{SANS}" '
        f'font-size="14" fill="{on}" opacity=".92">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    body = f"""
<defs>
  <clipPath id="card-{name}"><rect width="{TILE_W}" height="{TILE_H}" rx="14"/></clipPath>
  <clipPath id="slot-{name}"><rect x="0" y="62" width="{TILE_W}" height="62"/></clipPath>
  <linearGradient id="gl-{name}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
</defs>
<g class="ti" {d(delay)}>
  <g clip-path="url(#card-{name})">
    <rect width="{TILE_W}" height="{TILE_H}" fill="{color}"/>
    <circle class="rg" {d(delay + 0.5)} cx="{TILE_W - 40}" cy="{TILE_H - 40}" r="60" fill="none" stroke="{on}" stroke-opacity=".5" stroke-width="2"/>
    <rect class="sh" style="animation-delay:{delay + 1.4:.2f}s" x="0" y="-20" width="90" height="{TILE_H + 40}" fill="url(#gl-{name})" transform="translate(-260 0)"/>
  </g>
  <text class="sl" {d(delay + 0.35)} x="24" y="38" font-family="{MONO}" font-size="12" letter-spacing="1.2" fill="{on}">{escape(label)}</text>
  <g class="ai" {d(delay + 0.5)}><text class="n" style="animation-delay:{delay + 1.3:.2f}s" x="250" y="38" font-family="{MONO}" font-size="14" fill="{on}">&#8594;</text></g>
  <g clip-path="url(#slot-{name})"><g class="ro" {d(delay + 0.45)}>
    {count_up(num, word, 22, 112, f'font-family="{SERIF}" font-size="44" fill="{on}"', delay + 0.45)}
  </g></g>
  {blurb_svg}
</g>
"""
    write(
        f"{name}.svg",
        svg(
            TILE_W,
            TILE_H,
            body,
            ["serif", "serif-i", "sans", "mono"],
            f"{label}: {num} {word}. {blurb}",
            left=4 * pos,
            right=8 - 4 * pos,
        ),
    )


# ---- 3 · activity (monthly bars) ------------------------------------------------
def activity(data):
    h = 340
    monthly = data["monthly"][-12:]
    best = max(monthly[:-1] or monthly, key=lambda m: m["total"])
    top = max(best["total"], 1)
    x0, x1, base, maxh, gap = 40, 600, 292, 140, 10
    bw = (x1 - x0 - gap * (len(monthly) - 1)) / len(monthly)
    bars = []
    for i, m in enumerate(monthly):
        partial = i == len(monthly) - 1
        is_best = m is best and m["total"] > 0
        bh = max(4, round(m["total"] / top * maxh)) if m["total"] > 0 else 4
        x = x0 + i * (bw + gap)
        fill = TECH if is_best else ("#c9c9c4" if partial else (INK if m["total"] > 0 else "#e0e0dc"))
        label = datetime.date.fromisoformat(m["month"] + "-01").strftime("%b")
        bars.append(
            f'<rect class="g" style="animation-delay:{2.2 + i * 0.07:.2f}s" x="{x:.1f}" y="{base - bh}" '
            f'width="{bw:.1f}" height="{bh}" rx="4" fill="{fill}"><title>{label}: {m["total"]:,}</title></rect>'
            f'<text class="f" style="animation-delay:{2.2 + i * 0.07:.2f}s" x="{x + bw / 2:.1f}" y="{base + 22}" '
            f'text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">{label}</text>'
        )
        if is_best and m["total"] > 0:
            bars.append(
                f'<text class="p" style="animation-delay:3.2s" x="{x + bw / 2:.1f}" y="{base - bh - 10}" '
                f'text-anchor="middle" font-family="{MONO}" font-size="11" fill="{TECH}">{m["total"]:,}</text>'
            )

    cs = data["current_streak"]["length"]
    ls = data["longest_streak"]["length"]
    streak_note = "current streak, and the longest" if cs >= ls else f"current streak, longest {ls}"
    total_days = len(data["days"])
    stats = [
        (f'{cs} <tspan font-style="italic">{"day" if cs == 1 else "days"}</tspan>', streak_note),
        (f'{data["active_days"]}<tspan fill="#8e8e93"> / {total_days}</tspan>', "days with a commit"),
        (f'{data["best_day"]["count"]}', "on the busiest day"),
    ]
    side = []
    for i, (big, small) in enumerate(stats):
        y = 104 + i * 92
        side.append(
            f'<g class="r" {d(2.6 + i * 0.15)}>'
            f'<text x="650" y="{y}" font-family="{SERIF}" font-size="40" fill="{INK}">{big}</text>'
            f'<text x="650" y="{y + 24}" font-family="{SANS}" font-size="13" fill="{MUTED}">{small}</text></g>'
        )
        if i < 2:
            side.append(f'<rect class="f" {d(2.6)} x="650" y="{y + 44}" width="190" height="1" fill="{RULE}"/>')

    body = f"""
<rect width="{W}" height="{h}" rx="14" fill="{PAPER}"/>
<text class="f" {d(1.9)} x="40" y="58" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{MUTED}">THE LAST 12 MONTHS ON GITHUB</text>
<text class="r" {d(2.0)} x="38" y="114" font-family="{SERIF}" font-size="52" fill="{INK}">{data["total_contributions"]:,} <tspan font-style="italic">contributions</tspan></text>
{''.join(bars)}
{''.join(side)}
"""
    write(
        "activity.svg",
        svg(
            W,
            h,
            body,
            ["serif", "serif-i", "sans", "mono"],
            f'{data["total_contributions"]:,} contributions in the last year, {cs}-day streak',
        ),
    )


# ---- 4 · blue contribution graph -----------------------------------------------
BLUE = [PAPER_DEEP, "#c8d3ff", "#94a8ff", "#6280ff", TECH, "#1a3be0"]


def level_for(c):
    return 0 if c == 0 else 1 if c <= 2 else 2 if c <= 5 else 3 if c <= 10 else 4 if c <= 15 else 5


def heatmap(data):
    days = data["days"]
    first = datetime.date.fromisoformat(days[0]["date"])
    lead = (first.weekday() + 1) % 7
    cell, step, gx, gy = 12, 15, 44, 96
    cells, months, seen = [], [], set()
    for i, day in enumerate(days):
        k = i + lead
        col, row = divmod(k, 7)
        date = datetime.date.fromisoformat(day["date"])
        if date.day <= 7 and (date.year, date.month) not in seen and row == 0:
            seen.add((date.year, date.month))
            months.append((col, date.strftime("%b")))
        c = day["count"]
        delay = 1.0 + col * 0.03 + row * 0.02
        cells.append(
            f'<rect class="p" style="animation-delay:{delay:.2f}s" x="{gx + col * step}" y="{gy + row * step}" '
            f'width="{cell}" height="{cell}" rx="3" fill="{BLUE[level_for(c)]}">'
            f'<title>{day["date"]}: {c} contribution{"s" if c != 1 else ""}</title></rect>'
        )
    ncols = (len(days) + lead + 6) // 7
    right = gx + ncols * step - 3
    labels = "".join(
        f'<text x="{gx + col * step}" y="{gy + 7 * step + 16}" font-family="{MONO}" font-size="11" fill="{MUTED}">{m}</text>'
        for col, m in months if col < ncols - 12
    )
    legend_x = right - len(BLUE) * 14
    legend = "".join(
        f'<rect x="{legend_x + i * 14}" y="{gy + 7 * step + 6}" width="11" height="11" rx="2.5" fill="{c}"/>'
        for i, c in enumerate(BLUE)
    )
    h = gy + 7 * step + 44
    body = f"""
<rect width="{W}" height="{h}" rx="14" fill="{PAPER}"/>
<text class="r" {d(0.8)} x="42" y="62" font-family="{SERIF}" font-size="34" fill="{INK}">Every day, <tspan font-style="italic" fill="{TECH}">in blue</tspan></text>
<text class="f" {d(0.8)} x="{right}" y="60" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{MUTED}">REFRESHED DAILY</text>
{''.join(cells)}
<g class="f" {d(2.4)}>{labels}
<text x="{legend_x - 8}" y="{gy + 7 * step + 16}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{MUTED}">less</text>
{legend}
<text x="{legend_x + len(BLUE) * 14 + 2}" y="{gy + 7 * step + 16}" font-family="{MONO}" font-size="11" fill="{MUTED}">more</text></g>
"""
    write(
        "heatmap.svg",
        svg(
            W,
            h,
            body,
            ["serif", "serif-i", "mono"],
            f'Contribution graph: {data["total_contributions"]:,} contributions in the last year',
        ),
    )


# ---- 5 · featured project cards (2x2 grid for 4 projects) ----------------------
REPO_W, REPO_H = 880 / 2 - 6, 176  # 434px wide each, perfectly filling 880px with 12px gap
REPOS = [
    (
        "The Deceleration Engine",
        "nfl-big-data-bowl-2027",
        "Sports Analytics & Kinematics Research: Bridging 10Hz Combine RFID & in-game NGS tracking across 100k+ plays with BRK+ metric.",
        "Python · SciPy",
        TECH,
        3,
    ),
    (
        "chunklab",
        "chunklab",
        "RAG & Document Intelligence: Evaluation framework comparing PDF chunking strategies with 2D spatial IoU grounding.",
        "Python · FastAPI · Qdrant",
        STUDIO,
        0,
    ),
    (
        "prompt-injection",
        "prompt-injection",
        "AI Safety & Adversarial Testing: Automated testing harness evaluating LLM resilience against indirect prompt injections and jailbreaks.",
        "Python · LangChain",
        LEARN,
        0,
    ),
    (
        "leak-guard",
        "leak-guard",
        "DevSecOps Secret Scanner: High-performance scanner detecting exposed API keys, private tokens, and credentials in Git history.",
        "Python · Git Analysis",
        TECH,
        0,
    ),
]


def repo_card(i, display_name, repo_name, desc, lang, color, stars):
    delay = 4.6 + i * 0.12
    meta = f"{lang}  ·  ★ {stars}" if stars else f"{lang}  ·  live"
    pos = i % 2  # 0 = left, 1 = right
    left = 0 if pos == 0 else 6
    right = 6 if pos == 0 else 0
    lines = wrap(desc, 50)
    body = f"""
<rect width="{REPO_W}" height="{REPO_H}" rx="14" fill="{PAPER}"/>
<g class="r" {d(delay)}>
  <rect x="24" y="30" width="8" height="8" rx="2" fill="{color}"/>
  <text x="40" y="39" font-family="{SANS}" font-weight="600" font-size="18" fill="{INK}">{escape(display_name)}</text>
  {text_lines(24, 72, lines, 21, f'font-family="{SANS}" font-size="14" fill="{INK_SOFT}"')}
  <text x="24" y="{REPO_H - 24}" font-family="{MONO}" font-size="12" fill="{MUTED}">{escape(meta)}</text>
</g>
"""
    write(
        f"repo-{repo_name}.svg",
        svg(
            REPO_W,
            REPO_H,
            body,
            ["sans", "sans-b", "mono"],
            f"{display_name}: {desc}",
            left=left,
            right=right,
        ),
    )


def section_title(filename, text, italic, theme):
    fg = "#e6edf3" if theme == "dark" else INK
    body = (
        f'<text class="r" {d(4.4)} x="2" y="46" font-family="{SERIF}" font-size="34" fill="{fg}">{escape(text)} '
        f'<tspan font-style="italic">{escape(italic)}</tspan></text>'
    )
    write(filename, svg(W, 64, body, ["serif", "serif-i"], f"{text} {italic}", bottom=0))


# ---- 6 · tech stack card (comprehensive display of existing stack) -------------
def tech_stack_card():
    h = 220
    categories = [
        ("LANGUAGES & FRAMEWORKS", ["Python", "FastAPI", "Pandas", "NumPy", "SciPy", "PyTest"]),
        ("AI & RAG", ["LangChain", "ChromaDB", "Qdrant", "LLM APIs", "RAG Evaluation", "Prompt Defense", "MCP"]),
        ("SCRAPING & AUTOMATION", ["Playwright", "Scrapy", "BeautifulSoup", "Crawlab", "n8n", "Langflow"]),
        ("DATABASES & INFRA", ["PostgreSQL", "Docker", "Git", "Redis", "Linux"]),
    ]

    items_svg = []
    y_start = 40
    row_gap = 42

    for row_idx, (cat_label, pills) in enumerate(categories):
        ry = y_start + row_idx * row_gap
        cat_svg = (
            f'<text class="sl" {d(4.0 + row_idx * 0.1)} x="28" y="{ry}" '
            f'font-family="{MONO}" font-size="11" letter-spacing="1" fill="{MUTED}">{escape(cat_label)}</text>'
        )

        pills_svg = []
        pill_x = 230
        for p_idx, pill in enumerate(pills):
            pw = len(pill) * 7.5 + 16
            pills_svg.append(
                f'<g class="r" {d(4.1 + row_idx * 0.08 + p_idx * 0.02)}>'
                f'<rect x="{pill_x:.1f}" y="{ry - 14}" width="{pw:.1f}" height="20" rx="4" fill="{PAPER_DEEP}"/>'
                f'<text x="{pill_x + pw/2:.1f}" y="{ry}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{INK_SOFT}">{escape(pill)}</text>'
                f'</g>'
            )
            pill_x += pw + 8

        items_svg.append(cat_svg + "".join(pills_svg))

    body = f"""
<rect width="{W}" height="{h}" rx="14" fill="{PAPER}"/>
{''.join(items_svg)}
"""
    write(
        "tech-stack.svg",
        svg(W, h, body, ["sans", "mono"], "Tech Stack: Languages, Frameworks, AI, Scraping and Infrastructure"),
    )


if __name__ == "__main__":
    data = json.load(open(DATA))
    hero()
    heatmap(data)
    activity(data)

    # 3 Worlds / Pillars
    tile_avito(0)
    tile_nfl(1)
    tile(
        "learn",
        "DEVSECOPS",
        LEARN,
        INK,
        "1",
        "scanner",
        "leak-guard scanner detecting exposed API keys & secret tokens across Git history.",
        3.6,
        2,
    )

    # Tech Stack
    section_title("title-stack-dark.svg", "Tech", "stack", "dark")
    section_title("title-stack-light.svg", "Tech", "stack", "light")
    tech_stack_card()

    # Projects
    section_title("title-projects-dark.svg", "Featured", "projects", "dark")
    section_title("title-projects-light.svg", "Featured", "projects", "light")

    for i, (disp, name, desc, lang, color, stars) in enumerate(REPOS):
        repo_card(i, disp, name, desc, lang, color, stars)

    print("All README cards rendered successfully.")
