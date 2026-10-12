"""Render the hand-written panels: intro, contacts, skills, tools, LLM workflow, interests and projects.

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

from activity_panels import BLACK, COBALT, COBALT_LIGHT, GRAPHITE, INK, IVORY, MUTED, hops, r, svg, t

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "icons.json"), encoding="utf-8") as fh:
    ICONS = json.load(fh)
with open(os.path.join(HERE, "diagrams.json"), encoding="utf-8") as fh:
    DIAGRAMS = json.load(fh)

PURPLE, LAVENDER = "#67487F", "#E0D8E9"
FOREST, SAGE = "#2A6252", "#D5E4DC"
COBALT_TEXT = "#E4E9FB"  # body text on cobalt
PLATE_TEXT = "#D9D6CF"   # body text on black

# ---------------------------------------------------------------- copy

NAME = "Srinivasan"
STATUS = "Open to collaborate"
LEAD = "I build backend services, ML pipelines and AI agents."
ABOUT = "Mostly Python and Java: Spring Boot APIs, computer vision, and local models wired into agent loops."
SCHOOL = "Computer Science at KIIT, 2024–2028"
CUE = "Get in touch"

CONTACTS = [  # (icon, label, handle)
    ("github", "GitHub", "S-Srinivasan-06"),
    ("linkedin", "LinkedIn", "Connect with me"),
    ("email", "Email", "srinivasansubr2006@gmail.com"),
    ("leetcode", "LeetCode", "aKpXSchpeo"),
    ("instagram", "Instagram", "@s__srinivasan"),
]
SKILLS_TITLE, SKILLS = "What I write most", ["Python", "Java", "Spring Boot", "SQL"]
TOOLS_TITLE = "Tools I reach for"
TOOLS = ["FastAPI", "Docker", "PostgreSQL", "React", "OpenCV", "LangGraph", "MCP", "Ollama", "Codex", "Claude Code"]
LLM_TITLE = "How I use LLMs"
LLM_LINES = [
    "I use Codex and Claude Code every day to read code, write it, debug it and review it.",
    "In Taskflow Local, model output is schema-checked and reviewed before anything is saved.",
    "Sandman runs coding agents in Docker workspaces with MCP tools; LangGraph handles retries and cleanup.",
]
PIPELINE = ["context", "model", "tools", "validation", "review"]
INTERESTS_TITLE = "What I'm into"
INTERESTS = [
    ("Backend systems", "API design, relational data,", "ownership and concurrency", "server"),
    ("Machine learning", "Computer vision, tabular models", "and evaluation", "scatter"),
    ("Agents", "Local inference, custom harnesses,", "tool use and orchestration", "orbit"),
]
PROJECTS = [  # featured order; colours match the activity panels and tabs
    {"key": "local", "file": "p5-local", "name": "Taskflow Local", "short": "TL", "accent": "#96394A", "tint": "#EAD5D4",
     "stack": "llama.cpp, Gemma, React, SQLite",
     "desc": "An offline task manager with a local model built in. Type a task or add an image, the model "
             "proposes changes, and nothing is saved until it passes a schema check and you approve it. "
             "Ships as a Windows app with reminders."},
    {"key": "backend", "file": "p5-backend", "name": "Taskflow", "short": "TF", "accent": "#315A88", "tint": "#D7E2ED",
     "stack": "Java, Spring Boot, PostgreSQL",
     "desc": "A task manager on Spring Boot and PostgreSQL. Every request is checked against its owner, "
             "versioned updates stop two edits from overwriting each other, and integration tests cover the API."},
    {"key": "finance", "file": "p5-finance", "name": "Reconciliation Agent", "tab": "Reconciliation", "short": "RA",
     "accent": "#7B5725", "tint": "#EADFC6", "stack": "Python, FastAPI, pandas, WebSockets",
     "desc": "Matches sales records, payment gateway ledgers and bank statements. It runs in stages you can "
             "resume, sends mismatches to review, exports journal entries and keeps a hash-chained audit log."},
    {"key": "vision", "file": "p5-vision", "name": "CrowdShield", "short": "CS", "accent": "#2A6252", "tint": "#D5E4DC",
     "stack": "Python, OpenCV, OpenVINO, NumPy",
     "desc": "Crowd monitoring from video. It detects and tracks heads, estimates density inside regions you "
             "can redraw, streams live video and telemetry, and archives every run."},
    {"key": "agents", "file": "p5-agents", "name": "Sandman", "short": "SM", "accent": "#67487F", "tint": "#E0D8E9",
     "stack": "Python, LangGraph, MCP, Docker, Ollama",
     "desc": "A coding agent that works in isolated Docker workspaces with MCP tools. LangGraph drives "
             "execution, retries and cleanup, and each request can go to a local or a hosted model."},
]

CSS = """
.drift{animation:drift var(--s) linear infinite}@keyframes drift{to{transform:translateX(var(--p))}}
.bob{animation:bob 1.6s ease-in-out infinite}@keyframes bob{50%{transform:translateY(5px)}}
.float{animation:float 3.2s ease-in-out infinite}@keyframes float{50%{transform:translateY(-5px)}}
.nudge{animation:nudge 2.2s ease-in-out infinite}@keyframes nudge{0%,60%,100%{transform:translate(0,0)}30%{transform:translate(4px,-4px)}}
.wipe{transform-box:fill-box;transform-origin:0 50%;animation:wipe 4s cubic-bezier(.7,0,.3,1) infinite}
@keyframes wipe{0%{transform:scaleX(0)}45%,60%{transform:scaleX(1);opacity:1}100%{transform:scaleX(1);opacity:0}}
.lit{opacity:0;animation:lit var(--s) linear infinite}
.pop{transform-box:fill-box;transform-origin:50% 50%;animation:pop 6s ease-in-out infinite}
@keyframes pop{0%,10%,100%{transform:scale(1) rotate(0)}4%{transform:scale(1.28) rotate(-10deg)}7%{transform:scale(.94) rotate(4deg)}}
.spin{transform-box:fill-box;transform-origin:50% 50%;animation:spin 9s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
.flow{animation:flow 7s linear infinite}@keyframes flow{to{stroke-dashoffset:-140}}
.led{animation:led 1.8s steps(1) infinite}@keyframes led{0%{opacity:1}50%{opacity:.25}}
.jit{animation:jit 2.6s ease-in-out infinite}@keyframes jit{50%{transform:translate(var(--jx),var(--jy))}}
.packet{animation:packet 8s ease-in-out infinite}@keyframes packet{0%,100%{transform:translateX(0)}50%{transform:translateX(120px)}}
.scan{animation:scan 9s ease-in-out infinite}@keyframes scan{0%,100%{transform:translateX(0)}50%{transform:translateX(144px)}}
.grid-step{animation:grid-step 12s ease-in-out infinite}
@keyframes grid-step{0%,100%{transform:translate(0,0)}25%{transform:translate(48px,0)}50%{transform:translate(48px,48px)}75%{transform:translate(0,48px)}}
.heavy{font-family:'Arial Black','Segoe UI Black','Helvetica Neue',Arial,sans-serif;font-weight:900}
.tess-still{display:none}
@media(prefers-reduced-motion:reduce){.tess-live{display:none}.tess-still{display:inline}}
"""


def lit_css(hold_pct):
    """The shared CSS plus keyframes for a highlight that stays on for hold_pct of its cycle."""
    return CSS + f"@keyframes lit{{0%,{hold_pct:.1f}%{{opacity:1}}{hold_pct + 4:.1f}%,100%{{opacity:0}}}}"


def icon(name, x, y, scale, colour, cls="", style=""):
    inner = f'<g class="{cls}"{f" style={chr(34)}{style}{chr(34)}" if style else ""}>{ICONS[name]}</g>' if cls else ICONS[name]
    return f'<g transform="translate({x:g} {y:g}) scale({scale:g})" style="color:{colour}">{inner}</g>'


def chip(x, y, text, fill, ink, size=15, h=32, pad=13, lead=0, tail=0):
    """A short label on a solid chip; lead and tail reserve room for a mark before or after the text."""
    w = len(text) * size * .55 + 2 * pad + lead + tail
    return [r(x, y, w, h, fill, 5), t(x + pad + lead, y + h / 2 + size * .36, text, size, ink, weight="600")], w


def wrap(text, size, width, kind="sans"):
    limit, lines, line = int(width / (size * {"sans": .54, "serif": .5}[kind])), [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > limit:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line]


def arrow(x, y, colour, size=1):
    return (f'<g transform="translate({x:g} {y:g}) scale({size:g})"><g class="nudge"><path d="M-7 7L7-7M-4-7H7V4" '
            f'stroke="{colour}" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g></g>')


# ---------------------------------------------------------------- intro

def stripe_layer(w, h, period, angle, seconds, fill):
    """Stripes of `fill` that drift sideways by one period per cycle, so the loop is seamless."""
    span = math.hypot(w, h) + 4 * period
    count = int(span / period) + 2
    start = -span / 2 - period
    path = "".join(f"M{start + i * period:g} {-span / 2:g}h{period / 2:g}v{span:g}h{-period / 2:g}Z" for i in range(count))
    return (f'<g transform="translate({w / 2:g} {h / 2:g}) rotate({angle})"><g class="drift" style="--p:{period}px;--s:{seconds}s">'
            f'<path d="{path}" fill="{fill}"/></g></g>')


def stripes(w, h, period, angle, seconds):
    """Cream stripes on black."""
    return [r(0, 0, w, h, BLACK), stripe_layer(w, h, period, angle, seconds, IVORY)]


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


def woven_name(x, y, size, w, h, period, angle, seconds):
    """The name woven into the stripes: cream where it crosses black, cobalt where it crosses cream.

    The cobalt copy is masked by the same drifting stripes as the background, so the colour bands
    slide through the letters as the stripes move.
    """
    attrs = f'x="{x}" y="{y}" font-size="{size}" class="heavy" letter-spacing="{-size / 34:.1f}"'
    return (f'<mask id="weave" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}">'
            f'{stripe_layer(w, h, period, angle, seconds, "#fff")}</mask>'
            f'<text {attrs} fill="{IVORY}" stroke="{COBALT}" stroke-width="{size / 22:.1f}" stroke-linejoin="round" '
            f'paint-order="stroke">{NAME}</text>'
            f'<text {attrs} fill="{COBALT}" mask="url(#weave)">{NAME}</text>')


def status(x, y):
    parts, _ = chip(x, y, STATUS, BLACK, IVORY, 14, 30, 11, lead=16)
    return parts + [f'<circle class="pulse" cx="{x + 18}" cy="{y + 15}" r="5" fill="{COBALT_LIGHT}"/>']


def contact_cue(x, y):
    parts, w = chip(x, y, CUE, COBALT, IVORY, 15, 32, 13, tail=20)
    return parts + [f'<text x="{x + w - 26:g}" y="{y + 22:g}" font-size="16" fill="{IVORY}" class="num bob">↓</text>']


def intro(mobile):
    title = f"{NAME}: backend, machine learning and agents"
    desc = (f"{LEAD} {ABOUT} {SCHOOL}. The name is woven into drifting black and cream stripes, turning cobalt "
            "where it crosses cream, with a rotating four-dimensional cube behind it.")
    if not mobile:
        w, h = 1200, 486
        body = stripes(w, h, 92, -28, 9) + [tesseract(925, 250, 230)] + status(42, 34)
        body.append(woven_name(34, 206, 140, w, h, 92, -28, 9))
        body += [r(42, 250, 760, 136, BLACK, 8), t(66, 294, LEAD, 24, IVORY, weight="600")]
        body += [t(66, 330 + i * 30, line, 20, PLATE_TEXT) for i, line in enumerate(wrap(ABOUT, 20, 700))]
        parts, sw = chip(42, 414, SCHOOL, IVORY, INK)
        body += parts + contact_cue(42 + sw + 12, 414)
        return svg(w, h, title, desc, body, CSS, BLACK, paper=True)
    lead, about = wrap(LEAD, 23, 500), wrap(ABOUT, 18, 500)
    plate = 40 + len(lead) * 30 + len(about) * 26 + 18
    y = 386 + plate + 22
    w, h = 600, y + 100
    body = stripes(w, h, 72, -28, 9) + [tesseract(390, 220, 165, stroke=2)] + status(30, 30)
    body.append(woven_name(24, 350, 96, w, h, 72, -28, 9))
    body.append(r(30, 386, 540, plate, BLACK, 8))
    body += [t(52, 428 + i * 30, line, 23, IVORY, weight="600") for i, line in enumerate(lead)]
    top = 428 + len(lead) * 30 + 10
    body += [t(52, top + i * 26, line, 18, PLATE_TEXT) for i, line in enumerate(about)]
    body += chip(30, y, SCHOOL, IVORY, INK)[0] + contact_cue(30, y + 44)
    return svg(w, h, title, desc, body, CSS, BLACK, paper=True)


# ---------------------------------------------------------------- contacts

def contact(index, mobile):
    """One tile per contact, five to a row, so each shows its icon and name; the handle is in the alt text."""
    key, label, handle = CONTACTS[index]
    title = f"{label}: {handle}"
    lag = f"animation-delay:{index * 450}ms"
    if not mobile:
        body = [icon(key, 40, 56, .56, IVORY, "float", lag),
                t(76, 65, label, 24, IVORY, weight="600"),
                arrow(216, 24, IVORY, .8),
                r(24, 96, 192, 3, "#5F7BE6", 1.5),
                r(24, 96, 192, 3, IVORY, 1.5, f' class="wipe" style="{lag}"')]
        return svg(240, 116, title, title, body, CSS, COBALT)
    body = [icon(key, 75, 62, .78, IVORY, "float", lag),
            arrow(128, 22, IVORY, .9),
            t(75, 126, label, 21, IVORY, anchor="middle", weight="600"),
            r(28, 138, 94, 3, "#5F7BE6", 1.5),
            r(28, 138, 94, 3, IVORY, 1.5, f' class="wipe" style="{lag}"')]
    return svg(150, 150, title, title, body, CSS, COBALT)


# ---------------------------------------------------------------- skills, tools, LLM, interests
# These panels have no label row, so the drawing is laid out as if it had one and `shift` moves it up.

def skills(mobile):
    desc = "Python, Java, Spring Boot and SQL."
    if not mobile:
        body = [t(38, 98, SKILLS_TITLE, 38, IVORY, "serif")]
        spots, h, th = [(42 + i * 287, 126, 255) for i in range(4)], 222, 70
    else:
        body = [t(28, 94, SKILLS_TITLE, 38, IVORY, "serif")]
        spots, h, th = [(30 + (i % 2) * 277, 120 + (i // 2) * 78, 263) for i in range(4)], 286, 64
    for i, (name, (x, y, w)) in enumerate(zip(SKILLS, spots)):
        body += [r(x, y, w, th, GRAPHITE, 10),
                 f'<rect class="lit" style="--s:3.2s;animation-delay:{i * .8:.1f}s" x="{x + 1}" y="{y + 1}" width="{w - 2}" '
                 f'height="{th - 2}" rx="9" fill="none" stroke="{COBALT}" stroke-width="2"/>',
                 icon(name, x + 40, y + th / 2, .5, COBALT_LIGHT, "float", f"animation-delay:{i * 400}ms"),
                 t(x + 78, y + th / 2 + 8, name, 21, IVORY, weight="600")]
    return svg(1200 if not mobile else 600, h - 34, SKILLS_TITLE, desc, body, lit_css(18), BLACK, shift=34)


def tools(mobile):
    desc = ", ".join(TOOLS) + ". Each icon takes a turn to bounce; the React atom spins."
    if not mobile:
        body = [t(38, 98, TOOLS_TITLE, 38, INK, "serif")]
        spots, h, th = [(42 + (i % 5) * 227.25, 126 + (i // 5) * 88, 207) for i in range(10)], 312, 72
    else:
        body = [t(28, 94, TOOLS_TITLE, 38, INK, "serif")]
        spots, h, th = [(30 + (i % 2) * 277, 120 + (i // 2) * 72, 263) for i in range(10)], 494, 60
    for i, (name, (x, y, w)) in enumerate(zip(TOOLS, spots)):
        body += [r(x, y, w, th, LAVENDER, 10),
                 icon(name, x + 38, y + th / 2, .45, PURPLE, "spin" if name == "React" else "pop", f"animation-delay:{i * 300}ms"),
                 t(x + 70, y + th / 2 + 7, name, 18, INK, weight="600")]
    return svg(1200 if not mobile else 600, h - 34, TOOLS_TITLE, desc, body, CSS, IVORY, shift=34, paper=True)


def pipeline(rows, seconds=6.0):
    """Stage pills joined by flowing dashes; a marker hops along and lights each stage as it passes."""
    out, stops = [], []
    for row in rows:
        for i, (name, x, y, w, h) in enumerate(row):
            if i:
                px = row[i - 1][1] + row[i - 1][3]
                out.append(f'<path class="flow" d="M{px + 4:g} {y + h / 2:g}H{x - 4:g}" stroke="{IVORY}" stroke-opacity=".6" '
                           f'stroke-width="2" stroke-dasharray="4 6"/>')
            stops.append((x + 17, y + h / 2))  # inside the pill's left end, clear of the centred label
    css, times = hops("runner", stops, seconds)
    for (name, x, y, w, h), at in zip([s for row in rows for s in row], times):
        out += [r(x, y, w, h, "none", h / 2, f' stroke="{IVORY}" stroke-width="1.6"'),
                t(x + w / 2, y + h / 2 + 5, name, 15, IVORY, "mono", "middle"),
                f'<g class="lit" style="--s:{seconds}s;animation-delay:{at:.2f}s">{r(x, y, w, h, IVORY, h / 2)}'
                f'{t(x + w / 2, y + h / 2 + 5, name, 15, COBALT, "num", "middle")}</g>']
    x, y = stops[0]
    out.append(f'<rect class="runner" transform="translate({x:g} {y:g})" x="-5" y="-5" width="10" height="10" rx="2" '
               f'fill="{BLACK}" stroke="{IVORY}" stroke-width="1.5"/>')
    return out, css


def llm(mobile):
    desc = " ".join(LLM_LINES) + " Steps: " + ", ".join(PIPELINE) + "."
    if not mobile:
        body = [t(38, 98, LLM_TITLE, 38, IVORY, "serif")]
        body += [t(42, 142 + i * 30, line, 19, COBALT_TEXT) for i, line in enumerate(LLM_LINES)]
        w = (1116 - 4 * 40) / 5
        parts, css = pipeline([[(name, 42 + i * (w + 40), 236, w, 46) for i, name in enumerate(PIPELINE)]])
        return svg(1200, 276, LLM_TITLE, desc, body + parts, lit_css(14) + css, COBALT, shift=34)
    body = [t(28, 94, LLM_TITLE, 38, IVORY, "serif")]
    lines = [line for text in LLM_LINES for line in wrap(text, 18, 540)]
    body += [t(30, 140 + i * 26, line, 18, COBALT_TEXT) for i, line in enumerate(lines)]
    top = 140 + len(lines) * 26 + 6
    w = (540 - 2 * 24) / 3
    parts, css = pipeline([[(name, 30 + i * (w + 24), top, w, 44) for i, name in enumerate(PIPELINE[:3])],
                           [(name, 30 + i * (w + 24), top + 62, w, 44) for i, name in enumerate(PIPELINE[3:])]])
    return svg(600, top + 102, LLM_TITLE, desc, body + parts, lit_css(14) + css, COBALT, shift=34)


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
    desc = "; ".join(f"{a}: {b} {c}" for a, b, c, _ in INTERESTS) + "."
    if not mobile:
        body = [t(38, 98, INTERESTS_TITLE, 38, INK, "serif")]
        spots, h, ch = [(42 + i * 383, 124, 350) for i in range(3)], 262, 114
    else:
        body = [t(28, 94, INTERESTS_TITLE, 38, INK, "serif")]
        spots, h, ch = [(30, 120 + i * 114, 540) for i in range(3)], 482, 100
    for (head, a, b, kind), (x, y, w) in zip(INTERESTS, spots):
        body += [r(x, y, w, ch, SAGE, 10), glyph(kind, x + w - 40, y + 36),
                 t(x + 24, y + 40, head, 24, INK, "serif"),
                 t(x + 24, y + ch - 44, a, 18, MUTED), t(x + 24, y + ch - 20, b, 18, MUTED)]
    return svg(1200 if not mobile else 600, h - 34, INTERESTS_TITLE, desc, body, CSS, IVORY, shift=34, paper=True)


# ---------------------------------------------------------------- projects

def project(index, mobile):
    """A project card: name, plain description, stack, and the project's architecture diagram."""
    p = PROJECTS[index]
    desc = f"{p['desc']} Built with {p['stack']}."
    diagram = DIAGRAMS[p["key"]].replace("#F5F0E7", IVORY)
    underline = f' class="wipe" style="animation-delay:{index * 300}ms"'
    if not mobile:
        lines = wrap(p["desc"], 21, 670)
        body = [t(38, 86, p["name"], 52, IVORY, "serif"),
                r(42, 104, len(p["name"]) * 26, 3, p["tint"], 1.5, underline),
                arrow(1140, 46, IVORY)]
        body += [t(42, 146 + i * 31, line, 21, IVORY) for i, line in enumerate(lines)]
        stack_y = 146 + len(lines) * 31 + 22
        body += [t(42, stack_y, p["stack"], 15, p["tint"], "mono"),
                 f'<g transform="translate(756 74) scale(.94)">{diagram}</g>']
        return svg(1200, max(330, stack_y + 40), p["name"], desc, body, CSS, p["accent"])
    lines = wrap(p["desc"], 20, 540)
    body = [t(28, 74, p["name"], 46, IVORY, "serif"),
            r(30, 92, len(p["name"]) * 23, 3, p["tint"], 1.5, underline),
            arrow(560, 44, IVORY)]
    body += [t(30, 134 + i * 29, line, 20, IVORY) for i, line in enumerate(lines)]
    stack_y = 134 + len(lines) * 29 + 14
    body += [t(30, stack_y, p["stack"], 15, p["tint"], "mono"),
             f'<g transform="translate(40 {stack_y + 28}) scale(1.29)">{diagram}</g>']
    return svg(600, stack_y + 28 + 302 + 30, p["name"], desc, body, CSS, p["accent"])


def tab(index, mobile):
    p = PROJECTS[index]
    title = f"{p['name']}: open repository"
    if not mobile:
        body = [r(0, 0, 236, 5, p["accent"]), t(18, 47, p.get("tab", p["name"]), 18, p["accent"], weight="600"),
                arrow(212, 38, p["accent"], .8)]
        return svg(236, 76, title, p["name"], body, CSS, p["tint"])
    body = [r(0, 0, 118, 6, p["accent"]), t(59, 62, p["short"], 36, p["accent"], "serif", "middle")]
    return svg(118, 90, title, p["name"], body, CSS, p["tint"])


def download(mobile):
    body = [t(22, 34, "Download for Windows", 17, IVORY, weight="600"), arrow(272, 27, IVORY, .8)]
    return svg(300, 54, "Download Taskflow Local for Windows", "Latest Windows release of Taskflow Local",
               body, CSS, PROJECTS[0]["accent"])


def panels():
    """Every output file name with its renderer; each renderer takes `mobile`."""
    out = {"p5-intro": intro, "p5-skills": skills, "p5-tools": tools, "p5-llm": llm, "p5-interests": interests}
    for i, c in enumerate(CONTACTS):
        out[f"p5-contact-{c[0]}"] = lambda mobile, i=i: contact(i, mobile)
    for i, p in enumerate(PROJECTS):
        out[p["file"]] = lambda mobile, i=i: project(i, mobile)
        out[f"p5-tab-{i + 1}"] = lambda mobile, i=i: tab(i, mobile)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    jobs = [(f"{name}{'-mobile' if mobile else ''}", render, mobile) for name, render in panels().items() for mobile in (False, True)]
    jobs.append(("p5-download", download, False))
    for name, render, mobile in jobs:
        path = os.path.join(args.out, name + ".svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(mobile))
        print("wrote", path)


if __name__ == "__main__":
    main()
