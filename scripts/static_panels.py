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

from activity_panels import BLACK, BLACK_TONES, COBALT, COBALT_LIGHT, COBALT_TONES, GRAPHITE, INK, IVORY, MUTED, hops, r, svg, t

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "icons.json"), encoding="utf-8") as fh:
    ICONS = json.load(fh)
with open(os.path.join(HERE, "diagrams.json"), encoding="utf-8") as fh:
    DIAGRAMS = json.load(fh)

PURPLE, LAVENDER = "#67487F", "#E0D8E9"
FOREST, SAGE = "#2A6252", "#D5E4DC"
NAME_GRAY = "#33373D"
COBALT_TEXT = "#E4E9FB"  # body text on cobalt
PLATE_TEXT = "#D9D6CF"   # body text on black

# ---------------------------------------------------------------- copy

NAME = "Srinivasan"
STATUS = "Open to collaborate"
LEAD = "I build backend services, ML pipelines and AI agents."
ABOUT = "Mostly Python and Java: Spring Boot APIs, computer vision, and local models wired into agent loops."
SCHOOL = "Computer Science at KIIT, 2024–2028"
CUE = "Get in touch"

CONTACTS = [  # (icon, label, handle, tile colour, text colour): each tile in its platform's colour
    ("github", "GitHub", "S-Srinivasan-06", "#24292F", IVORY),
    ("linkedin", "LinkedIn", "Connect with me", "#0A66C2", IVORY),
    ("email", "Email", "srinivasansubr2006@gmail.com", "#C5221F", IVORY),
    ("leetcode", "LeetCode", "aKpXSchpeo", "#FFA116", INK),
    ("instagram", "Instagram", "@s__srinivasan", "#D62976", IVORY),
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
# Each card is meant to be read in a few seconds: one line on what it is, three highlights,
# the stack and one line of proof. Every claim was checked against the repository's code.
PROJECTS = [
    {"key": "backend", "file": "p5-backend", "name": "Taskflow", "accent": "#315A88", "tint": "#D7E2ED",
     "line": "A full-stack task manager with user accounts, deployed online",
     "points": ["Each user's tasks are isolated, with tests on every task endpoint",
                "Stale edits are rejected with HTTP 409 (optimistic locking)",
                "Session login, CSRF protection and login rate limiting"],
     "stack": "Java 21, Spring Boot, PostgreSQL, React, TypeScript",
     "proof": "Live demo, CI, integration tests on PostgreSQL"},
    {"key": "local", "file": "p5-local", "name": "Taskflow Local", "accent": "#96394A", "tint": "#EAD5D4",
     "line": "A Windows task manager that runs a local AI model offline",
     "points": ["Type a request or drop in a screenshot; Gemma drafts the tasks",
                "Every AI change is validated and waits for your approval",
                "SQLite storage, a tray app and in-app reminders"],
     "stack": "Tauri, React, TypeScript, llama.cpp, SQLite",
     "proof": "Windows installer, 32 unit tests, model ~3.4 GB separate"},
    {"key": "finance", "file": "p5-finance", "name": "Payment Reconciliation", "accent": "#7B5725", "tint": "#EADFC6",
     "line": "Matches sales, payment gateway and bank records (Razorpay buildathon)",
     "points": ["A resumable 15-step pipeline that pauses for human review",
                "Audit log that exposes edits (SHA-256 hash chain)",
                "Exports accounting journal entries as CSV"],
     "stack": "Python, FastAPI, pandas, WebSockets, Docker",
     "proof": "41 passing tests, CI on Python 3.10–3.12"},
    {"key": "research", "file": "p5-research", "name": "EEG Seizure Detection", "accent": "#67487F", "tint": "#E0D8E9",
     "line": "An attempt to reproduce a published EEG seizure-detection model (DGDCN)",
     "points": ["Audited 8,140 EEG recordings and excluded 630, with reasons",
                "Rebuilt the paper's 12-second setup from the authors' code",
                "AUROC 0.880 vs the paper's 0.887 (best checkpoint, picked on eval data)"],
     "stack": "Python, PyTorch, NumPy, SciPy, scikit-learn",
     "proof": "Every run, audit and caveat documented"},
    {"key": "vision", "file": "p5-vision", "name": "CrowdShield", "accent": "#2A6252", "tint": "#D5E4DC",
     "line": "A web dashboard that counts people in video and flags crowd risk",
     "points": ["Detects and tracks heads with YOLOv8, on CPU with OpenVINO",
                "Streams live video and 10 Hz telemetry to the browser",
                "Draggable watch zone with a four-level risk alert"],
     "stack": "Python, YOLOv8, OpenVINO, OpenCV, NumPy",
     "proof": "Team project: I built the original pipeline and the dashboard"},
]
DEMOS = {  # extra buttons under a card: (label, link)
    "local": ("Download for Windows",
              "https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/releases/latest"),
    "backend": ("Live demo (first load takes about a minute)", "https://taskflow-olive-psi.vercel.app/"),
}

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


def tesseract(cx, cy, radius, frames=48, seconds=11, stroke=2.4):
    """A 4D hypercube turning in two orthogonal planes (XW and YZ), projected to the page.

    A quarter turn in both planes maps the cube's vertices and edges onto themselves, so
    animating a quarter turn and repeating it gives an endless, seamless rotation.
    SMIL drives the geometry; under reduced motion a still frame is shown instead. The white lines use
    a difference blend, so they read ivory on black stripes and black on cream stripes.
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


def plain_name(x, y, size, slab_x, slab_w):
    """The name in plain dark gray on a cream block, so it reads the same over either stripe colour."""
    top = y - size * .86
    return (r(slab_x, top, slab_w, size * 1.04, IVORY, 8)
            + f'<text x="{x}" y="{y}" font-size="{size}" class="heavy" letter-spacing="{-size / 34:.1f}" '
              f'fill="{NAME_GRAY}">{NAME}</text>')


def status(x, y):
    parts, _ = chip(x, y, STATUS, BLACK, IVORY, 14, 30, 11, lead=16)
    return parts + [f'<circle class="pulse" cx="{x + 18}" cy="{y + 15}" r="5" fill="{COBALT_LIGHT}"/>']


def contact_cue(x, y):
    parts, w = chip(x, y, CUE, COBALT, IVORY, 15, 32, 13, tail=20)
    return parts + [f'<text x="{x + w - 26:g}" y="{y + 22:g}" font-size="16" fill="{IVORY}" class="num bob">↓</text>']


def intro(mobile):
    title = f"{NAME}: backend, machine learning and agents"
    desc = (f"{LEAD} {ABOUT} {SCHOOL}. Drifting black and cream stripes, with a rotating "
            "four-dimensional cube behind the name.")
    if not mobile:
        w, h = 1200, 486
        body = stripes(w, h, 92, -28, 9) + [tesseract(925, 250, 230)] + status(42, 34)
        body.append(plain_name(66, 206, 132, 42, 760))
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
    body.append(plain_name(40, 350, 96, 30, 540))
    body.append(r(30, 386, 540, plate, BLACK, 8))
    body += [t(52, 428 + i * 30, line, 23, IVORY, weight="600") for i, line in enumerate(lead)]
    top = 428 + len(lead) * 30 + 10
    body += [t(52, top + i * 26, line, 18, PLATE_TEXT) for i, line in enumerate(about)]
    body += chip(30, y, SCHOOL, IVORY, INK)[0] + contact_cue(30, y + 44)
    return svg(w, h, title, desc, body, CSS, BLACK, paper=True)


# ---------------------------------------------------------------- contacts

def contact(index, mobile):
    """One tile per contact, five to a row, so each shows its icon and name; the handle is in the alt text."""
    key, label, handle, fill, ink = CONTACTS[index]
    title = f"{label}: {handle}"
    lag = f"animation-delay:{index * 450}ms"
    if not mobile:
        body = [icon(key, 40, 56, .56, ink, "float", lag),
                t(76, 65, label, 24, ink, weight="600"),
                arrow(216, 24, ink, .8),
                r(24, 96, 192, 3, ink, 1.5, ' opacity=".3"'),
                r(24, 96, 192, 3, ink, 1.5, f' class="wipe" style="{lag}"')]
        return svg(240, 116, title, title, body, CSS, fill)
    body = [icon(key, 75, 62, .78, ink, "float", lag),
            arrow(128, 22, ink, .9),
            t(75, 126, label, 21, ink, anchor="middle", weight="600"),
            r(28, 138, 94, 3, ink, 1.5, ' opacity=".3"'),
            r(28, 138, 94, 3, ink, 1.5, f' class="wipe" style="{lag}"')]
    return svg(150, 150, title, title, body, CSS, fill)


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
    return svg(1200 if not mobile else 600, h - 34, SKILLS_TITLE, desc, body, lit_css(18), BLACK, shift=34, drift=BLACK_TONES)


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
        return svg(1200, 276, LLM_TITLE, desc, body + parts, lit_css(14) + css, COBALT, shift=34, drift=COBALT_TONES)
    body = [t(28, 94, LLM_TITLE, 38, IVORY, "serif")]
    lines = [line for text in LLM_LINES for line in wrap(text, 18, 540)]
    body += [t(30, 140 + i * 26, line, 18, COBALT_TEXT) for i, line in enumerate(lines)]
    top = 140 + len(lines) * 26 + 6
    w = (540 - 2 * 24) / 3
    parts, css = pipeline([[(name, 30 + i * (w + 24), top, w, 44) for i, name in enumerate(PIPELINE[:3])],
                           [(name, 30 + i * (w + 24), top + 62, w, 44) for i, name in enumerate(PIPELINE[3:])]])
    return svg(600, top + 102, LLM_TITLE, desc, body + parts, lit_css(14) + css, COBALT, shift=34, drift=COBALT_TONES)


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

def bullets(points, x, y, size, width, gap, colour):
    """Short highlights, each behind a small square; returns the drawing and the next free y."""
    out = []
    for point in points:
        lines = wrap(point, size, width)
        out.append(r(x, y - size * .45, 8, 8, colour, 1.5))
        out += [t(x + 20, y + i * (size + 6), line, size, IVORY) for i, line in enumerate(lines)]
        y += len(lines) * (size + 6) + gap
    return out, y


def project(index, mobile):
    """A project card made to be skimmed: what it is in one line, three verified highlights,
    the stack, and one line of proof. The architecture diagram sits small on the right."""
    p = PROJECTS[index]
    desc = f"{p['line']} {'; '.join(p['points'])}. Built with {p['stack']}. {p.get('proof', '')}"
    diagram = DIAGRAMS[p["key"]].replace("#F5F0E7", IVORY)
    underline = f' class="wipe" style="animation-delay:{index * 300}ms"'
    if not mobile:
        body = [t(38, 66, p["name"], 44, IVORY, "serif"),
                r(42, 82, len(p["name"]) * 22, 3, p["tint"], 1.5, underline),
                arrow(1150, 32, IVORY),
                t(42, 118, p["line"], 22, IVORY, weight="600")]
        points, y = bullets(p["points"], 44, 160, 19, 760, 9, p["tint"])
        body += points
        footer = [t(42, y + 22, p["stack"], 15, p["tint"], "mono")]
        if p.get("proof"):
            footer.append(t(1158, y + 22, p["proof"], 15, p["tint"], anchor="end", weight="600"))
        body += footer + [f'<g transform="translate(884 64) scale(.68)">{diagram}</g>']
        return svg(1200, y + 50, p["name"], desc, body, CSS, p["accent"])
    lead = wrap(p["line"], 20, 560)
    body = [t(28, 62, p["name"], 40, IVORY, "serif"),
            r(30, 78, len(p["name"]) * 20, 3, p["tint"], 1.5, underline),
            arrow(560, 36, IVORY)]
    body += [t(30, 118 + i * 27, line, 20, IVORY, weight="600") for i, line in enumerate(lead)]
    points, y = bullets(p["points"], 32, 118 + len(lead) * 27 + 22, 18, 560, 8, p["tint"])
    body += points + [t(30, y + 18, p["stack"], 15, p["tint"], "mono")]
    if p.get("proof"):
        body.append(t(30, y + 46, p["proof"], 15, p["tint"], weight="600"))
    return svg(600, y + (74 if p.get("proof") else 46), p["name"], desc, body, CSS, p["accent"])


def button(key):
    """A small button under a project card, such as a download or a live demo."""
    p = next(p for p in PROJECTS if p["key"] == key)
    label = DEMOS[key][0]
    w = len(label) * 17 * .56 + 64
    body = [t(22, 34, label, 17, IVORY, weight="600"), arrow(w - 26, 27, IVORY, .8)]
    return svg(round(w), 54, f"{p['name']}: {label}", f"{label} for {p['name']}", body, CSS, p["accent"])


def panels():
    """Every output file name with its renderer; each renderer takes `mobile`."""
    out = {"p5-intro": intro, "p5-skills": skills, "p5-tools": tools, "p5-llm": llm, "p5-interests": interests}
    for i, c in enumerate(CONTACTS):
        out[f"p5-contact-{c[0]}"] = lambda mobile, i=i: contact(i, mobile)
    for i, p in enumerate(PROJECTS):
        out[p["file"]] = lambda mobile, i=i: project(i, mobile)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="assets")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    jobs = [(f"{name}{'-mobile' if mobile else ''}", render, mobile) for name, render in panels().items() for mobile in (False, True)]
    jobs += [(f"p5-button-{key}", lambda mobile, key=key: button(key), False) for key in DEMOS]
    for name, render, mobile in jobs:
        path = os.path.join(args.out, name + ".svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(mobile))
        print("wrote", path)


if __name__ == "__main__":
    main()
