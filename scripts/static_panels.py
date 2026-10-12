"""Render the hand-written panels: intro, contact tiles, skills, tools, LLM workflow and interests.

These hold no live data, so they are generated once and committed:

  python scripts/static_panels.py --out assets

Each panel has a desktop (1200 wide) and a mobile (600 wide) composition, shares the
style sheet and embedded Profile Mono font of activity_panels.py, and keeps the same
rules: no JavaScript or external files, and everything stops under prefers-reduced-motion.
"""

import argparse
import itertools
import json
import math
import os

from activity_panels import BLACK, COBALT, COBALT_DEEP, COBALT_LIGHT, GRAPHITE, INK, IVORY, MUTED, hops, mono_width, r, svg, t

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "icons.json"), encoding="utf-8") as fh:
    ICONS = json.load(fh)

PURPLE, LAVENDER = "#67487F", "#E0D8E9"
FOREST, SAGE = "#2A6252", "#D5E4DC"
COBALT_TEXT = "#E4E9FB"  # body text on cobalt

NAME = "Srinivasan."
TAGLINE = "Backend engineering · Machine learning · Agentic AI"
STACK = "PYTHON · JAVA · SPRING BOOT · LOCAL LLMS"
SCHOOL = "KIIT · COMPUTER SCIENCE · 2024–2028"

CONTACTS = [  # (icon, label, handle)
    ("github", "GITHUB", "S-Srinivasan-06"),
    ("linkedin", "LINKEDIN", "Connect with me"),
    ("email", "EMAIL", "srinivasansubr2006@gmail.com"),
    ("leetcode", "LEETCODE", "aKpXSchpeo"),
]
SKILLS = ["Python", "Java", "Spring Boot", "SQL"]
TOOLS = ["FastAPI", "Docker", "PostgreSQL", "React", "OpenCV", "LangGraph", "MCP", "Ollama", "Codex", "Claude Code"]
LLM_TEXT = ("I use Codex and Claude Code for repository exploration, implementation, debugging, and review. "
            "Taskflow Local and Sandman connect models to structured outputs, validation, and tool access. "
            "Their execution loops cover local inference, agent orchestration, retries, and cleanup.")
LLM_LINES = [  # desktop line breaks, one sentence each
    "I use Codex and Claude Code for repository exploration, implementation, debugging, and review.",
    "Taskflow Local and Sandman connect models to structured outputs, validation, and tool access.",
    "Their execution loops cover local inference, agent orchestration, retries, and cleanup.",
]
PIPELINE = ["CONTEXT", "MODEL", "TOOLS", "VALIDATION", "REVIEW"]
INTERESTS = [
    ("Backend systems", "API contracts, relational data,", "ownership, and concurrency.", "server"),
    ("Machine learning", "Computer vision, tabular ML,", "and model evaluation.", "scatter"),
    ("Agentic AI", "Local inference, custom harnesses,", "tool use, and orchestration.", "orbit"),
]

CSS = """
.drift{animation:drift var(--s) linear infinite}@keyframes drift{to{transform:translateX(var(--p))}}
.sheen{animation:sheen 7s ease-in-out infinite}@keyframes sheen{0%,45%{transform:translateX(0)}100%{transform:translateX(var(--d))}}
.bob{animation:bob 1.6s ease-in-out infinite}@keyframes bob{50%{transform:translateY(5px)}}
.float{animation:float 3.2s ease-in-out infinite}@keyframes float{50%{transform:translateY(-5px)}}
.nudge{animation:nudge 2.2s ease-in-out infinite}@keyframes nudge{0%,60%,100%{transform:translate(0,0)}30%{transform:translate(4px,-4px)}}
.wipe{transform-box:fill-box;transform-origin:0 50%;animation:wipe 4s cubic-bezier(.7,0,.3,1) infinite}
@keyframes wipe{0%{transform:scaleX(0)}45%,60%{transform:scaleX(1);opacity:1}100%{transform:scaleX(1);opacity:0}}
.lit{opacity:0;animation:lit var(--s) linear infinite}
.pop{transform-box:fill-box;transform-origin:50% 50%;animation:pop 6s ease-in-out infinite}
@keyframes pop{0%,10%,100%{transform:scale(1) rotate(0)}4%{transform:scale(1.28) rotate(-10deg)}7%{transform:scale(.94) rotate(4deg)}}
.spin{transform-box:fill-box;transform-origin:50% 50%;animation:spin 9s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
.flow{animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-20}}
.led{animation:led 1.8s steps(1) infinite}@keyframes led{0%{opacity:1}50%{opacity:.25}}
.jit{animation:jit 2.6s ease-in-out infinite}@keyframes jit{50%{transform:translate(var(--jx),var(--jy))}}
.tess-still{display:none}
@media(prefers-reduced-motion:reduce){.tess-live{display:none}.tess-still{display:inline}}
"""


def lit_css(hold_pct):
    """The shared CSS plus keyframes for a highlight that stays on for hold_pct of its cycle."""
    return CSS + f"@keyframes lit{{0%,{hold_pct:.1f}%{{opacity:1}}{hold_pct + 4:.1f}%,100%{{opacity:0}}}}"


def icon(name, x, y, scale, colour, cls="", style=""):
    inner = f'<g class="{cls}"{f" style={chr(34)}{style}{chr(34)}" if style else ""}>{ICONS[name]}</g>' if cls else ICONS[name]
    return f'<g transform="translate({x:g} {y:g}) scale({scale:g})" style="color:{colour}">{inner}</g>'


def tag(x, y, text, fill, ink, size=14, h=30, pad=12, anchor="start", lead=0, tail=0):
    """A label on a solid chip; lead and tail reserve room for a mark before or after the text."""
    w = mono_width(text, size) + 2 * pad + lead + tail
    if anchor == "end":
        x -= w
    return [r(x, y, w, h, fill, 4), t(x + pad + lead, y + h / 2 + size * .36, text, size, ink, "mono")], w


def wrap(text, size, width, kind="sans"):
    limit, lines, line = int(width / (size * {"sans": .54, "serif": .5}[kind])), [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > limit:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line]


# ---------------------------------------------------------------- intro

def stripes(w, h, period, angle, seconds):
    """Ivory stripes on black that drift sideways by one period per cycle, so the loop is seamless."""
    span = math.hypot(w, h) + 4 * period
    count = int(span / period) + 2
    start = -span / 2 - period
    path = "".join(f"M{start + i * period:g} {-span / 2:g}h{period / 2:g}v{span:g}h{-period / 2:g}Z" for i in range(count))
    return [r(0, 0, w, h, BLACK),
            f'<g transform="translate({w / 2:g} {h / 2:g}) rotate({angle})"><g class="drift" style="--p:{period}px;--s:{seconds}s">'
            f'<path d="{path}" fill="{IVORY}"/></g></g>']


def tesseract(cx, cy, radius, frames=72, seconds=11, stroke=2.4):
    """A 4D hypercube turning in two orthogonal planes (XW and YZ), projected to the page.

    A quarter turn in both planes maps the cube's vertices and edges onto themselves, so
    animating a quarter turn and repeating it gives an endless, seamless rotation.
    SMIL drives the geometry; under reduced motion a still frame is shown instead.
    """
    verts = list(itertools.product((-1, 1), repeat=4))
    edges = [(i, j) for i, j in itertools.combinations(range(16), 2)
             if sum(a != b for a, b in zip(verts[i], verts[j])) == 1]
    ty, tx = math.radians(-28), math.radians(20)

    def project(theta):
        c, s = math.cos(theta), math.sin(theta)
        pts = []
        for x, y, z, w in verts:
            x, w = x * c - w * s, x * s + w * c
            y, z = y * c - z * s, y * s + z * c
            k = 1 / (3 - w)
            x, y, z = x * k, y * k, z * k
            x, z = x * math.cos(ty) + z * math.sin(ty), -x * math.sin(ty) + z * math.cos(ty)
            y, z = y * math.cos(tx) - z * math.sin(tx), y * math.sin(tx) + z * math.cos(tx)
            k = 1 / (2.4 - z)
            pts.append((x * k, y * k))
        return pts

    shots = [project(math.pi / 2 * i / frames) for i in range(frames + 1)]
    extent = max(max(abs(a), abs(b)) for shot in shots for a, b in shot)
    shots = [[(cx + a * radius / extent, cy + b * radius / extent) for a, b in shot] for shot in shots]

    def d(p):
        return "".join(f"M{p[i][0]:.1f} {p[i][1]:.1f}L{p[j][0]:.1f} {p[j][1]:.1f}" for i, j in edges)

    def dots(shot, live):
        out = []
        for v, (x, y) in enumerate(shot):
            anim = ""
            if live:
                xs = ";".join(f"{s[v][0]:.1f}" for s in shots)
                ys = ";".join(f"{s[v][1]:.1f}" for s in shots)
                anim = (f'<animate attributeName="cx" dur="{seconds}s" repeatCount="indefinite" values="{xs}"/>'
                        f'<animate attributeName="cy" dur="{seconds}s" repeatCount="indefinite" values="{ys}"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{COBALT}" stroke="{IVORY}" stroke-width="2">{anim}</circle>')
        return "".join(out)

    lines = f'fill="none" stroke="#fff" stroke-width="{stroke}" stroke-linecap="round"'
    live = (f'<g class="tess-live"><g style="mix-blend-mode:difference"><path d="{d(shots[0])}" {lines}>'
            f'<animate attributeName="d" dur="{seconds}s" repeatCount="indefinite" values="{";".join(d(s) for s in shots)}"/>'
            f'</path></g>{dots(shots[0], True)}</g>')
    still = shots[frames // 3]
    return live + f'<g class="tess-still"><g style="mix-blend-mode:difference"><path d="{d(still)}" {lines}/></g>{dots(still, False)}</g>'


NAME_DEFS = f"""<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
<rect width="7" height="7" fill="{COBALT}"/><rect width="2.4" height="7" fill="{COBALT_DEEP}"/></pattern>
<filter id="grain" x="-3%" y="-15%" width="106%" height="130%">
<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="11" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 .96 0 0 0 0 .94 0 0 0 0 .9 0 0 0 -3 1.22" result="light"/>
<feComposite in="light" in2="SourceAlpha" operator="in" result="lightIn"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 .04 0 0 0 0 .1 0 0 0 0 .42 0 0 0 3 -1.5" result="dark"/>
<feComposite in="dark" in2="SourceAlpha" operator="in" result="darkIn"/>
<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="darkIn"/><feMergeNode in="lightIn"/></feMerge></filter>"""


def textured_name(x, y, size, width):
    """The name in hatched, grainy cobalt with an ivory halo and a hard black shadow; a sheen crosses it."""
    attrs = f'x="{x}" y="{y}" font-size="{size}" class="serif" letter-spacing="{-size / 32:.1f}"'
    halo = f'stroke-width="{size / 12:.0f}" stroke-linejoin="round"'
    return (f'<text {attrs} transform="translate({size / 20:.0f} {size / 20:.0f})" fill="{BLACK}" stroke="{BLACK}" {halo}>{NAME}</text>'
            f'<text {attrs} fill="{IVORY}" stroke="{IVORY}" {halo}>{NAME}</text>'
            f'<text {attrs} fill="url(#hatch)" filter="url(#grain)">{NAME}</text>'
            f'<clipPath id="namecut"><text {attrs}>{NAME}</text></clipPath>'
            f'<g clip-path="url(#namecut)"><rect class="sheen" style="--d:{width + 260}px" x="{x - 200}" y="{y - size}" '
            f'width="180" height="{size * 1.3:.0f}" fill="url(#gloss)" opacity=".55" transform="skewX(-18)"/></g>')


def status(x, y, anchor="start"):
    parts, w = tag(x, y, "OPEN TO COLLABORATE", BLACK, IVORY, 13, 28, 10, anchor, lead=16)
    left = x - w if anchor == "end" else x
    return parts + [f'<circle class="pulse" cx="{left + 19}" cy="{y + 14}" r="5" fill="{COBALT_LIGHT}"/>']


def contact_cue(x, y):
    parts, w = tag(x, y, "CONTACT", COBALT, IVORY, 14, 32, 12, tail=22)
    return parts + [f'<text x="{x + w - 26:g}" y="{y + 22:g}" font-size="16" fill="{IVORY}" class="num bob">↓</text>']


def intro(mobile):
    title = "Srinivasan — backend, ML and agentic AI"
    desc = (f"{TAGLINE}. Python and Java development: Spring Boot services, ML pipelines, local models, and agent "
            f"workflows. {SCHOOL}. The name is set in textured cobalt over drifting black and ivory stripes, "
            "with a rotating four-dimensional cube behind it.")
    if not mobile:
        w, h = 1200, 540
        body = stripes(w, h, 92, -28, 9) + [tesseract(925, 285, 245)]
        body += tag(42, 34, "SRINIVASAN / DEVELOPMENT PORTFOLIO", COBALT, IVORY)[0]
        body += status(1158, 35, "end")
        body.append(textured_name(36, 222, 164, 760))
        body += [r(42, 258, 760, 176, BLACK, 8),
                 t(66, 302, TAGLINE, 24, IVORY, weight="600"),
                 t(66, 342, "Python and Java development: Spring Boot services,", 20, "#D9D6CF"),
                 t(66, 372, "ML pipelines, local models, and agent workflows.", 20, "#D9D6CF"),
                 t(66, 410, STACK, 13, COBALT_LIGHT, "mono")]
        parts, sw = tag(42, 466, SCHOOL, IVORY, INK, 14, 32)
        body += parts + contact_cue(42 + sw + 12, 466)
        return svg(w, h, title, desc, body, CSS, BLACK, NAME_DEFS)
    w, h = 600, 780
    body = stripes(w, h, 72, -28, 9) + [tesseract(390, 250, 170, stroke=2)]
    body += tag(30, 28, "SRINIVASAN / PORTFOLIO", COBALT, IVORY, 14, 30)[0]
    body += status(30, 70)
    body.append(textured_name(24, 382, 112, 520))
    body += [r(30, 414, 540, 242, BLACK, 8),
             t(52, 456, "Backend engineering ·", 23, IVORY, weight="600"),
             t(52, 486, "Machine learning · Agentic AI", 23, IVORY, weight="600"),
             t(52, 526, "Python and Java development: Spring Boot", 18, "#D9D6CF"),
             t(52, 552, "services, ML pipelines, local models,", 18, "#D9D6CF"),
             t(52, 578, "and agent workflows.", 18, "#D9D6CF"),
             t(52, 624, STACK, 12, COBALT_LIGHT, "mono")]
    body += tag(30, 676, SCHOOL, IVORY, INK, 13, 30)[0]
    body += contact_cue(30, 720)
    return svg(w, h, title, desc, body, CSS, BLACK, NAME_DEFS)


# ---------------------------------------------------------------- contacts

def arrow(x, y, colour, size=1):
    return (f'<g transform="translate({x:g} {y:g}) scale({size:g})"><g class="nudge"><path d="M-7 7L7-7M-4-7H7V4" '
            f'stroke="{colour}" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g>')


def contact(index, mobile):
    key, label, handle = CONTACTS[index]
    title = f"{label.title()}: {handle}"
    lag = f"animation-delay:{index * 450}ms"
    if not mobile:
        size = 17 if len(handle) * .56 * 17 < 252 else 15
        body = [icon(key, 40, 40, .44, IVORY, "float", lag),
                t(70, 46, label, 13, "#CDD6F7", "mono"),
                arrow(272, 38, IVORY),
                t(24, 84, handle, size, IVORY, weight="600"),
                r(24, 100, 252, 3, "#5F7BE6", 1.5),
                r(24, 100, 252, 3, IVORY, 1.5, f' class="wipe" style="{lag}"')]
        return svg(300, 116, title, f"{label.title()} — {handle}. Opens in a new page.", body, CSS, COBALT)
    body = [icon(key, 75, 62, .78, IVORY, "float", lag),
            arrow(128, 22, IVORY, .9),
            t(75, 126, label, 19, IVORY, "mono", "middle"),
            r(28, 138, 94, 3, "#5F7BE6", 1.5),
            r(28, 138, 94, 3, IVORY, 1.5, f' class="wipe" style="{lag}"')]
    return svg(150, 150, title, f"{label.title()} — {handle}.", body, CSS, COBALT)


# ---------------------------------------------------------------- skills, tools, LLM, interests

def skills(mobile):
    title, desc = "Languages and backend skills", "My main development stack is Python, Java and Spring Boot, with SQL for relational data."
    if not mobile:
        body = [t(42, 46, "LANGUAGES & BACKEND", 15, COBALT_LIGHT, "mono"),
                t(38, 98, "Python. Java. Spring Boot.", 38, IVORY, "serif")]
        spots = [(42 + i * 287, 126, 255) for i in range(4)]
        h, th = 222, 70
    else:
        body = [t(30, 43, "LANGUAGES & BACKEND", 15, COBALT_LIGHT, "mono"),
                t(28, 94, "Python. Java.", 38, IVORY, "serif"),
                t(28, 138, "Spring Boot.", 38, IVORY, "serif")]
        spots = [(30 + (i % 2) * 277, 164 + (i // 2) * 78, 263) for i in range(4)]
        h, th = 330, 64
    for i, (name, (x, y, w)) in enumerate(zip(SKILLS, spots)):
        lag = f"animation-delay:{i * 400}ms"
        body += [r(x, y, w, th, GRAPHITE, 10),
                 f'<rect class="lit" style="--s:3.2s;animation-delay:{i * .8:.1f}s" x="{x + 1}" y="{y + 1}" width="{w - 2}" '
                 f'height="{th - 2}" rx="9" fill="none" stroke="{COBALT}" stroke-width="2"/>',
                 icon(name, x + 40, y + th / 2, .5, COBALT_LIGHT, "float", lag),
                 t(x + 78, y + th / 2 + 8, name, 21, IVORY, weight="600")]
    return svg(1200 if not mobile else 600, h, title, desc, body, lit_css(18), BLACK)


def tools(mobile):
    title = "Tools I work with"
    desc = "Tools: " + ", ".join(TOOLS) + ". Each icon takes a turn to bounce; the React atom spins."
    if not mobile:
        body = [t(42, 46, "TOOLS I WORK WITH", 15, PURPLE, "mono"),
                t(38, 98, "Services, models, and development tools.", 38, INK, "serif")]
        spots = [(42 + (i % 5) * 227.25, 126 + (i // 5) * 88, 207) for i in range(10)]
        h, th = 312, 72
    else:
        body = [t(30, 43, "TOOLS I WORK WITH", 15, PURPLE, "mono"),
                t(28, 94, "Services, models,", 38, INK, "serif"),
                t(28, 138, "and development tools.", 38, INK, "serif")]
        spots = [(30 + (i % 2) * 277, 164 + (i // 2) * 72, 263) for i in range(10)]
        h, th = 538, 60
    for i, (name, (x, y, w)) in enumerate(zip(TOOLS, spots)):
        cls = "spin" if name == "React" else "pop"
        body += [r(x, y, w, th, LAVENDER, 10),
                 icon(name, x + 38, y + th / 2, .45, PURPLE, cls, f"animation-delay:{i * 300}ms"),
                 t(x + 70, y + th / 2 + 7, name, 18, INK, weight="600")]
    return svg(1200 if not mobile else 600, h, title, desc, body, CSS, IVORY)


def pipeline(stages, rows, seconds=6.0):
    """Stage pills joined by flowing dashes; a packet hops along and lights each stage as it passes."""
    out, centers = [], []
    for row in rows:
        for i, (name, x, y, w, h) in enumerate(row):
            if i:
                px = row[i - 1][1] + row[i - 1][3]
                out.append(f'<path class="flow" d="M{px + 4:g} {y + h / 2:g}H{x - 4:g}" stroke="{IVORY}" stroke-opacity=".6" '
                           f'stroke-width="2" stroke-dasharray="4 6"/>')
            centers.append((x + 17, y + h / 2))  # inside the pill's left end, clear of the centred label
    css, times = hops("packet", centers, seconds)
    flat = [s for row in rows for s in row]
    for (name, x, y, w, h), at in zip(flat, times):
        out += [r(x, y, w, h, "none", h / 2, f' stroke="{IVORY}" stroke-width="1.6"'),
                t(x + w / 2, y + h / 2 + 5, name, 14, IVORY, "mono", "middle"),
                f'<g class="lit" style="--s:{seconds}s;animation-delay:{at:.2f}s">{r(x, y, w, h, IVORY, h / 2)}'
                f'{t(x + w / 2, y + h / 2 + 5, name, 14, COBALT, "num", "middle")}</g>']
    x, y = centers[0]
    out.append(f'<rect class="packet" transform="translate({x:g} {y:g})" x="-5" y="-5" width="10" height="10" rx="2" '
               f'fill="{BLACK}" stroke="{IVORY}" stroke-width="1.5"/>')
    return out, css


def llm(mobile):
    title = "LLM development"
    desc = "Coding agents, custom harnesses, and local models. " + LLM_TEXT + " Pipeline: " + " → ".join(PIPELINE).lower() + "."
    if not mobile:
        body = [t(42, 46, "LLM DEVELOPMENT", 15, "#CDD6F7", "mono"),
                t(38, 98, "Coding agents, custom harnesses, and local models.", 38, IVORY, "serif")]
        body += [t(42, 142 + i * 30, line, 20, COBALT_TEXT) for i, line in enumerate(LLM_LINES)]
        w = (1116 - 4 * 40) / 5
        rows = [[(name, 42 + i * (w + 40), 236, w, 46) for i, name in enumerate(PIPELINE)]]
        parts, css = pipeline(PIPELINE, rows)
        return svg(1200, 310, title, desc, body + parts, lit_css(14) + css, COBALT)
    body = [t(30, 43, "LLM DEVELOPMENT", 15, "#CDD6F7", "mono")]
    body += [t(28, 92 + i * 42, line, 36, IVORY, "serif") for i, line in enumerate(["Coding agents,", "custom harnesses,", "and local models."])]
    lines = wrap(LLM_TEXT, 18, 540)
    body += [t(30, 222 + i * 26, line, 18, COBALT_TEXT) for i, line in enumerate(lines)]
    top = 222 + len(lines) * 26 + 10
    w = (540 - 2 * 24) / 3
    rows = [[(name, 30 + i * (w + 24), top, w, 44) for i, name in enumerate(PIPELINE[:3])],
            [(name, 30 + i * (w + 24), top + 62, w, 44) for i, name in enumerate(PIPELINE[3:])]]
    parts, css = pipeline(PIPELINE, rows)
    return svg(600, top + 136, title, desc, body + parts, lit_css(14) + css, COBALT)


def glyph(kind, x, y):
    """Small animated marks for the interest cards: server lights, a jittering scatter, an orbit."""
    if kind == "server":
        out = []
        for i in range(3):
            out += [r(x - 16, y - 16 + i * 12, 32, 9, "none", 2, f' stroke="{FOREST}" stroke-width="1.8"'),
                    f'<circle class="led" style="animation-delay:{i * .6:.1f}s" cx="{x + 9}" cy="{y - 11.5 + i * 12}" r="2" fill="{FOREST}"/>']
        return "".join(out)
    if kind == "scatter":
        pts = [(-12, 6, 4, -3), (-4, -8, -3, 4), (6, 2, -4, -3), (12, -10, 3, 3), (0, 12, 4, -4)]
        return "".join(f'<circle class="jit" style="--jx:{jx}px;--jy:{jy}px;animation-delay:{i * .35:.2f}s" cx="{x + dx}" '
                       f'cy="{y + dy}" r="3" fill="{FOREST}"/>' for i, (dx, dy, jx, jy) in enumerate(pts)) + \
            f'<path d="M{x - 18} {y + 14}L{x + 18} {y - 14}" stroke="{FOREST}" stroke-width="1.5" stroke-dasharray="3 3"/>'
    return (f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="{FOREST}" stroke-width="1.8"/>'
            f'<circle cx="{x}" cy="{y}" r="4" fill="{FOREST}"/>'
            f'<g transform="translate({x} {y})"><g class="spin" style="animation-duration:4s">'
            f'<circle cx="15" cy="0" r="3.5" fill="{FOREST}"/><circle cx="-15" cy="0" r="2" fill="{FOREST}" opacity=".5"/></g></g>')


def interests(mobile):
    title, desc = "Interests", "Interests: " + "; ".join(f"{a}: {b} {c}" for a, b, c, _ in INTERESTS)
    if not mobile:
        body = [t(42, 46, "WHAT I AM INTERESTED IN", 15, FOREST, "mono"),
                t(38, 98, "Backend systems, ML, and agent infrastructure.", 38, INK, "serif")]
        spots, h, ch = [(42 + i * 383, 124, 350) for i in range(3)], 262, 114
    else:
        body = [t(30, 43, "WHAT I AM INTERESTED IN", 15, FOREST, "mono"),
                t(28, 94, "Backend systems, ML,", 36, INK, "serif"),
                t(28, 136, "and agent infrastructure.", 36, INK, "serif")]
        spots, h, ch = [(30, 164 + i * 114, 540) for i in range(3)], 526, 100
    for (head, a, b, kind), (x, y, w) in zip(INTERESTS, spots):
        body += [r(x, y, w, ch, SAGE, 10), glyph(kind, x + w - 40, y + 36),
                 t(x + 24, y + 40, head, 24, INK, "serif"),
                 t(x + 24, y + ch - 44, a, 18, MUTED), t(x + 24, y + ch - 20, b, 18, MUTED)]
    return svg(1200 if not mobile else 600, h, title, desc, body, CSS, IVORY)


PANELS = {"p5-intro": intro, "p5-skills": skills, "p5-tools": tools, "p5-llm": llm, "p5-interests": interests}
PANELS.update({f"p5-contact-{c[0]}": (lambda i: lambda mobile: contact(i, mobile))(i) for i, c in enumerate(CONTACTS)})


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for name, render in PANELS.items():
        for mobile in (False, True):
            path = os.path.join(args.out, f"{name}{'-mobile' if mobile else ''}.svg")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(render(mobile))
            print("wrote", path)


if __name__ == "__main__":
    main()
