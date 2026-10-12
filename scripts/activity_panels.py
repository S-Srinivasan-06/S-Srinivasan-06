"""Render the profile's activity panels as SVG.

Reads public contribution data from the GitHub GraphQL API and draws three
panels in the portfolio's ivory palette, each with a desktop (1200 wide) and a
mobile (600 wide) composition:

  p5-activity   contribution heatmap, streaks and active days
  p5-commits    commits per month with summary figures
  p5-repos      most active repositories and the latest commits

Standard library only. Usage:

  GITHUB_TOKEN=... python scripts/activity_panels.py --login S-Srinivasan-06 --out out
  python scripts/activity_panels.py --fixture data.json --out out   # offline preview

Like the other p5 panels, the SVGs use no JavaScript or external files, and
every animation stops under prefers-reduced-motion. Labels and figures use
Profile Mono, a small Cascadia Code subset embedded in each SVG (see fonts/OFL.txt).
"""

import argparse
import base64
import json
import os
import urllib.request
from datetime import date, datetime, timedelta, timezone
from xml.sax.saxutils import escape

IVORY, INK = "#F1E7D2", "#252C36"  # IVORY is a light cream; cream panels also get a paper texture
MUTED = "#5E636B"
BURGUNDY, BLUSH = "#96394A", "#EAD5D4"
BLUE, MIST = "#315A88", "#D7E2ED"
AMBER, SAND = "#7B5725", "#EADFC6"
# Newer palette: black, cobalt and ivory, alternated with the original project colours.
BLACK, GRAPHITE, SMOKE = "#0E0F12", "#1B1E25", "#A9ADB5"
COBALT, COBALT_DEEP, COBALT_LIGHT = "#2347D9", "#1A38BC", "#8FA6FF"

# Slow background gradients: each list is one cycle of tones the panel drifts through.
COBALT_TONES = [COBALT, "#3A5BF0", "#3B2FC2", "#1B36B5"]
BLACK_TONES = [BLACK, "#121A33", BLACK, "#1A1430"]

THEMES = {
    "dark": {"bg": BLACK, "ink": IVORY, "muted": SMOKE, "accent": COBALT_LIGHT, "tile": GRAPHITE, "rule": "#2A2E37",
             "track": "#262A33", "mark": IVORY, "heat": ["#1F232B", "#1B3A9A", COBALT, "#5B7CFF", "#C9D4FF"]},
    "cobalt": {"bg": COBALT, "ink": IVORY, "muted": "#CDD6F7", "accent": IVORY, "tile": COBALT_DEEP, "rule": "#6A85EA",
               "track": "#3A5CE0", "mark": IVORY},
    "ivory": {"bg": IVORY, "ink": INK, "muted": MUTED, "accent": AMBER, "tile": SAND, "rule": "#DCD3C3",
              "track": "#E6DED0", "mark": INK},
}

# Featured projects keep their colour and display name from the project cards.
FEATURED = {
    "Taskflow-Local-hacktoberfest-weekend": ("Taskflow Local", BURGUNDY),
    "Taskflow": ("Taskflow", BLUE),
    "Razorpay-Buildathon-webui-and-cli": ("Reconciliation Agent", AMBER),
    "CrowdShield": ("CrowdShield", "#2A6252"),
    "sandman-ai-sandbox": ("Sandman", "#67487F"),
}

MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


def font_face(weight):
    with open(os.path.join(FONT_DIR, f"profile-mono-{weight}.woff2"), "rb") as fh:
        data = base64.b64encode(fh.read()).decode()
    return f"@font-face{{font-family:'Profile Mono';font-weight:{weight};src:url(data:font/woff2;base64,{data}) format('woff2')}}"


# Every element that moves is either visible at rest (so reduced motion shows the
# finished chart) or decorative and transparent at rest (rings, drops, shine).
SPRING = "cubic-bezier(.34,1.56,.64,1)"
STYLE = ("<style>" + font_face(400) + font_face(600) + """
.sans{font-family:'Segoe UI',Helvetica,Arial,sans-serif}.serif{font-family:Georgia,'Times New Roman',serif}.mono,.num{font-family:'Profile Mono','Cascadia Code',Consolas,monospace}.num{font-weight:600}
.box{transform-box:fill-box;transform-origin:50% 50%}.pulse{animation:pulse 2.4s ease-in-out infinite}.blink{animation:blink 1.1s steps(1) infinite}
.popin{animation:popin .5s """ + SPRING + """ both}.rise{transform-box:fill-box;transform-origin:50% 100%;animation:rise 1.2s """ + SPRING + """ both}.grow{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.3s """ + SPRING + """ both}
.fade{animation:fade .6s ease-out both}.slide{animation:slide .7s cubic-bezier(.2,.8,.2,1) both}.ring{opacity:0;animation:ring var(--t) linear infinite}
.drop{opacity:0;animation:drop 4.2s cubic-bezier(.55,0,.75,.4) infinite}.bgdrift{animation:bgdrift var(--s) linear infinite}
@keyframes bgdrift{to{transform:translateX(var(--p))}}.shine{animation:shine 5s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.2}50%{opacity:1}}@keyframes blink{0%{opacity:1}50%{opacity:0}}
@keyframes popin{from{opacity:0;transform:scale(.2)}}@keyframes rise{from{transform:scaleY(0)}}@keyframes grow{from{transform:scaleX(0)}}
@keyframes fade{from{opacity:0}}@keyframes slide{from{opacity:0;transform:translateX(-14px)}}
@keyframes ring{0%{opacity:.9;transform:scale(1)}7%{opacity:0;transform:scale(2.4)}100%{opacity:0;transform:scale(2.4)}}
@keyframes drop{0%{opacity:0;transform:translateY(0)}12%{opacity:1}62%{opacity:1;transform:translateY(var(--fall))}70%,100%{opacity:0;transform:translateY(var(--fall)) scaleY(.4)}}
@keyframes shine{0%,55%{transform:translateX(0)}100%{transform:translateX(var(--d))}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
</style>""")


# ---------------------------------------------------------------- data

API = "https://api.github.com/graphql"


def graphql(token, query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(API, body, {"Authorization": f"bearer {token}", "User-Agent": "profile-activity-panels"})
    with urllib.request.urlopen(req, timeout=60) as res:
        payload = json.load(res)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]


def iso(d, end=False):
    return f"{d}T23:59:59Z" if end else f"{d}T00:00:00Z"


def month_start(d, back):
    m = d.year * 12 + d.month - 1 - back
    return date(m // 12, m % 12 + 1, 1)


def calendar_days(collection):
    return [(day["date"], day["contributionCount"])
            for week in collection["contributionCalendar"]["weeks"] for day in week["contributionDays"]]


def fetch(login, token, today):
    """Collect everything the panels need. Repository details are limited to public repositories."""
    months = [month_start(today, back) for back in range(11, -1, -1)]
    ranges = [(m, min(month_start(m, -1) - timedelta(days=1), today)) for m in months]
    month_fields = "\n".join(
        f'm{i}: contributionsCollection(from: "{iso(a)}", to: "{iso(b, True)}") {{'
        " totalPullRequestContributions totalIssueContributions totalPullRequestReviewContributions"
        " commitContributionsByRepository(maxRepositories: 25) {"
        " repository { name url isPrivate } contributions(first: 31) { nodes { commitCount } } } }"
        for i, (a, b) in enumerate(ranges))
    first = graphql(token, f"""query($login: String!, $from: DateTime!, $to: DateTime!) {{
      user(login: $login) {{
        id createdAt
        year: contributionsCollection(from: $from, to: $to) {{
          contributionCalendar {{ totalContributions weeks {{ contributionDays {{ date contributionCount }} }} }}
        }}
        {month_fields}
      }}
    }}""", {"login": login, "from": iso(today - timedelta(days=364)), "to": iso(today, True)})["user"]

    # Earlier years only feed the all-time totals and longest streak.
    years = range(int(first["createdAt"][:4]), today.year)
    history = {}
    if years:
        fields = "\n".join(
            f'y{y}: contributionsCollection(from: "{iso(date(y, 1, 1))}", to: "{iso(date(y, 12, 31), True)}") {{'
            " contributionCalendar { weeks { contributionDays { date contributionCount } } } }" for y in years)
        older = graphql(token, f"query($login: String!) {{ user(login: $login) {{ {fields} }} }}", {"login": login})["user"]
        for y in years:
            history.update(calendar_days(older[f"y{y}"]))
    history.update(calendar_days(first["year"]))

    recent_q = graphql(token, """query($login: String!, $uid: ID!) {
      user(login: $login) {
        repositories(first: 12, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false,
                     orderBy: {field: PUSHED_AT, direction: DESC}) {
          nodes { name defaultBranchRef { target { ... on Commit {
            history(first: 6, author: {id: $uid}) { nodes { messageHeadline committedDate url additions deletions } }
          } } } }
        }
      }
    }""", {"login": login, "uid": first["id"]})["user"]["repositories"]["nodes"]

    monthly, repos, kinds = [], {}, {"prs": 0, "issues": 0, "reviews": 0}
    for i, m in enumerate(months):
        coll = first[f"m{i}"]
        kinds["prs"] += coll["totalPullRequestContributions"]
        kinds["issues"] += coll["totalIssueContributions"]
        kinds["reviews"] += coll["totalPullRequestReviewContributions"]
        total = 0
        for entry in coll["commitContributionsByRepository"]:
            repo = entry["repository"]
            if repo["isPrivate"]:
                continue
            n = sum(node["commitCount"] for node in entry["contributions"]["nodes"])
            repos[repo["name"]] = repos.get(repo["name"], 0) + n
            total += n
        monthly.append({"month": f"{m:%Y-%m}", "count": total})

    recent = []
    for repo in recent_q:
        if repo["name"] == login or not repo["defaultBranchRef"]:
            continue
        for c in repo["defaultBranchRef"]["target"]["history"]["nodes"]:
            recent.append({"repo": repo["name"], "message": c["messageHeadline"], "date": c["committedDate"][:10],
                           "url": c["url"], "additions": c["additions"], "deletions": c["deletions"]})
    recent.sort(key=lambda c: c["date"], reverse=True)

    return {
        "login": login,
        "generated": str(today),
        "days": [{"date": d, "count": n} for d, n in calendar_days(first["year"])],
        "history": [{"date": d, "count": n} for d, n in sorted(history.items())],
        "totals": {"commits": sum(m["count"] for m in monthly), **kinds, "repos": sum(1 for n in repos.values() if n)},
        "monthly_commits": monthly,
        "repos": [{"name": k, "commits": v} for k, v in sorted(repos.items(), key=lambda kv: (-kv[1], kv[0])) if v],
        "recent": latest_per_repo(recent)[:8],
    }


# ---------------------------------------------------------------- figures

def parse(d):
    return date.fromisoformat(d)


def short_date(d, year=False):
    s = f"{d.day} {MONTHS[d.month - 1].title()}"
    return f"{s} {d.year}" if year else s


def streaks(days, today):
    """Return (current, (longest, start, end), last_active) from a date-sorted list."""
    counts = {parse(x["date"]): x["count"] for x in days}
    cursor = today if counts.get(today) else today - timedelta(days=1)
    current = 0
    while counts.get(cursor):
        current += 1
        cursor -= timedelta(days=1)
    best, run, run_start, span = 0, 0, None, (None, None)
    for d in sorted(counts):
        if counts[d]:
            run_start = d if run == 0 else run_start
            run += 1
            if run > best:
                best, span = run, (run_start, d)
        else:
            run = 0
    active = [d for d in counts if counts[d]]
    return current, (best, *span), max(active) if active else None


def figures(data):
    today = parse(data["generated"])
    days = data["days"]
    current, longest, last_active = streaks(data.get("history") or days, today)
    active = [x for x in days if x["count"]]
    best = max(days, key=lambda x: (x["count"], x["date"]))
    weekday_totals = [0] * 7
    for x in days:
        weekday_totals[parse(x["date"]).weekday()] += x["count"]
    busiest = max(data["monthly_commits"], key=lambda m: (m["count"], m["month"]))
    return {
        "today": today,
        "total": sum(x["count"] for x in days),
        "all_time": sum(x["count"] for x in data.get("history") or days),
        "current": current,
        "longest": longest,
        "last_active": last_active,
        "active_days": len(active),
        "span_days": len(days),
        "best_day": best,
        "weekday": WEEKDAYS[weekday_totals.index(max(weekday_totals))] if any(weekday_totals) else None,
        "busiest_month": busiest,
    }


def levels(days):
    """GitHub-style levels: quartiles of the non-zero days."""
    nonzero = sorted(x["count"] for x in days if x["count"])
    if not nonzero:
        return lambda n: 0
    q = [nonzero[min(len(nonzero) - 1, int(len(nonzero) * p))] for p in (.25, .5, .75)]
    return lambda n: 0 if n == 0 else 1 + sum(n > t for t in q)


# ---------------------------------------------------------------- drawing

MONO_ADVANCE = .586  # Cascadia's advance width per em, plus letter-spacing added in mono_width
WIDTH = {"sans": .54, "mono": .6, "num": .6, "serif": .5}


def mono_width(text, size, spacing=.4):
    return len(text) * (size * MONO_ADVANCE + spacing)


def fit(text, size, kind, max_width):
    text = " ".join(text.split())
    limit = int(max_width / (size * WIDTH[kind]))
    return text if len(text) <= limit else text[: max(1, limit - 1)].rstrip() + "…"


def t(x, y, s, size, fill=INK, kind="sans", anchor=None, weight=None, spacing=None):
    attrs = f'x="{x:g}" y="{y:g}" font-size="{size}" fill="{fill}" class="{kind}"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if spacing or kind == "mono":
        attrs += f' letter-spacing="{spacing or ".4"}"'
    return f"<text {attrs}>{escape(str(s))}</text>"


def r(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" fill="{fill}"{extra}/>'


def delay(ms, cls):
    return f' class="{cls}" style="animation-delay:{ms:.0f}ms"'


# Paper texture for cream panels: a pre-rendered grain tile (scripts/paper.png, made by
# make_paper.py) laid over the panel. A live noise filter would be recomputed on every frame.
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "paper.png"), "rb") as _fh:
    PAPER = ('<pattern id="paper" width="128" height="128" patternUnits="userSpaceOnUse"><image width="128" height="128" '
             f'href="data:image/png;base64,{base64.b64encode(_fh.read()).decode()}"/></pattern>')


def drift_layer(gid, w, h, tones, seconds=26, lag=0.0):
    """A gradient band twice as wide as one cycle, slid left by exactly one cycle per loop.

    The tones repeat once inside the band, so the end of the loop matches its start.
    Returns the gradient definition and the moving rectangle that uses it.
    """
    period = w * 1.5
    stops = tones + tones + tones[:1]
    n = len(stops) - 1
    grad = (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{2 * period:g}" y2="0">'
            + "".join(f'<stop offset="{i / n:.4f}" stop-color="{c}"/>' for i, c in enumerate(stops)) + "</linearGradient>")
    band = (f'<rect class="bgdrift" style="--p:{-period:g}px;--s:{seconds}s;animation-delay:{lag:.2f}s" '
            f'x="0" y="0" width="{2 * period:g}" height="{h}" fill="url(#{gid})"/>')
    return grad, band


def svg(w, h, title, desc, body, css="", bg=IVORY, defs="", shift=0, paper=False, drift=None, lag=0.0):
    grad, band = drift_layer("drift", w, h, drift, lag=lag) if drift else ("", "")
    texture = f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#paper)"/>' if paper else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            f'{STYLE}{f"<style>{css}</style>" if css else ""}<defs><clipPath id="frame"><rect x="0" y="0" width="{w}" '
            f'height="{h}" rx="14" fill="{bg}"/></clipPath><linearGradient id="gloss"><stop offset="0" stop-color="#fff" '
            f'stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff" '
            f'stop-opacity="0"/></linearGradient>{PAPER if paper else ""}{grad}{defs}</defs><g clip-path="url(#frame)">{r(0, 0, w, h, bg)}{band}'
            f'<g transform="translate(0 {-shift})">{"".join(body)}</g>{texture}</g></svg>\n')


def hops(name, points, seconds):
    """CSS that hops an element through points at even intervals, then fades and restarts.

    Returns the CSS and the arrival time of each point, so other elements can react on arrival.
    """
    n, span = len(points), 92.0
    frames, times = [], []
    for i, (x, y) in enumerate(points):
        p = span * i / max(1, n - 1)
        times.append(seconds * p / 100)
        frames.append(f"{p:.3f}%{{transform:translate({x:g}px,{y:g}px);opacity:1;"
                      f"animation-timing-function:cubic-bezier(.6,0,.25,1)}}")
    last, start = points[-1], points[0]
    frames.append(f"96%{{transform:translate({last[0]:g}px,{last[1]:g}px);opacity:0}}")
    frames.append(f"96.1%,100%{{transform:translate({start[0]:g}px,{start[1]:g}px);opacity:0}}")
    css = f".{name}{{animation:{name} {seconds:.1f}s linear infinite}}@keyframes {name}{{{''.join(frames)}}}"
    return css, times


def tile(th, x, y, w, h, label, value, sub, value_size=38, pad=24, cursor=False):
    out = [r(x, y, w, h, th["tile"], 10),
           t(x + pad, y + 32, label, 15, th["accent"], weight="600"),
           t(x + pad - 1, y + 32 + value_size + 2, value, value_size, th["ink"], "num", spacing="-.5"),
           t(x + pad, y + h - 20, fit(sub, 15, "sans", w - 2 * pad), 15, th["muted"])]
    if cursor:
        cx = x + pad - 1 + len(value) * (value_size * MONO_ADVANCE - .5) + 6
        out.append(r(cx, y + 34 + value_size * .3, value_size * .42, value_size * .72, th["accent"], 1, ' class="blink"'))
    return out


def plural(n, word, many=None):
    return f"{n:,} {word if n == 1 else many or word + 's'}"


def heatmap(th, days, today, x0, y0, weeks, pitch, cell, label_x):
    """Draw the grid; a small square hops through the active days in date order, rippling each one."""
    level = levels(days)
    heat = th["heat"]
    counts = {parse(x["date"]): x["count"] for x in days}
    first = today - timedelta(days=(today.weekday() + 1) % 7 + 7 * (weeks - 1))
    out = [t(label_x, y0 + pitch * row + cell - 3, name, 12, th["muted"], "mono")
           for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri"))]
    active, last_label = [], -9
    for col in range(weeks):
        sunday = first + timedelta(days=7 * col)
        starts_month = sunday.day <= 7 if col == 0 else sunday.month != (sunday - timedelta(days=7)).month
        if starts_month and col - last_label >= 3 and col < weeks - 2:
            out.append(t(x0 + col * pitch, y0 - 12, MONTHS[sunday.month - 1].title(), 12, th["muted"], "mono"))
            last_label = col
        for row in range(7):
            d = sunday + timedelta(days=row)
            if d > today:
                break
            n, x, y = counts.get(d, 0), x0 + col * pitch, y0 + row * pitch
            out.append(r(x, y, cell, cell, heat[level(n)], 3, delay((col + row) * 14, "box popin")))
            if n:
                active.append((x + cell / 2, y + cell / 2))
    col, row = weeks - 1, (today.weekday() + 1) % 7
    out.append(f'<rect class="pulse" x="{x0 + col * pitch - 2.5:g}" y="{y0 + row * pitch - 2.5:g}" width="{cell + 5}" '
               f'height="{cell + 5}" rx="4" fill="none" stroke="{th["mark"]}" stroke-width="1.5"/>')
    if len(active) < 2:
        return out, ""
    seconds = min(45, max(12, .5 * len(active)))
    css, times = hops("bot", active, seconds)
    for (x, y), at in zip(active, times):
        out.append(f'<rect class="box ring" style="--t:{seconds:.1f}s;animation-delay:{at:.2f}s" x="{x - cell / 2:g}" '
                   f'y="{y - cell / 2:g}" width="{cell}" height="{cell}" rx="3" fill="none" stroke="{th["accent"]}" stroke-width="2"/>')
    x, y = active[-1]
    out.append(f'<rect class="bot" transform="translate({x:g} {y:g})" x="-4.5" y="-4.5" width="9" height="9" rx="2" '
               f'fill="{th["mark"]}" stroke="{th["bg"]}" stroke-width="1.5"/>')
    return out, css


def legend(th, x_end, y):
    out, x = [t(x_end, y, "More", 12, th["muted"], "mono", "end")], x_end - 44
    for colour in reversed(th["heat"]):
        x -= 18
        out.append(r(x, y - 11, 13, 13, colour, 3))
    out.append(t(x - 8, y, "Less", 12, th["muted"], "mono", "end"))
    return out


def activity_tiles(f):
    longest, start, end = f["longest"]
    if f["current"]:
        current_sub = f"through {short_date(f['today'])}"
    else:
        current_sub = f"last active {short_date(f['last_active'])}" if f["last_active"] else "no activity yet"
    if longest:
        span = short_date(start) if start == end else f"{short_date(start)} – {short_date(end)}"
        longest_sub = f"{span} {end.year}" if end.year != f["today"].year or start.year != end.year else span
    else:
        longest_sub = "no activity yet"
    best = f["best_day"]
    return [
        ("Current streak", plural(f["current"], "day"), current_sub),
        ("Longest streak", plural(longest, "day"), longest_sub),
        ("Active days", f"{f['active_days']}", f"out of {f['span_days']}"),
        ("Best day", f"{best['count']}", f"contributions on {short_date(parse(best['date']))}" if best["count"] else "none yet"),
    ]


def activity_panel(data, mobile):
    th = THEMES["dark"]
    f = figures(data)
    stamp = f"updated {short_date(f['today'], True)}"
    desc = (f"{plural(f['total'], 'contribution')} in the last year, {f['active_days']} active days. "
            f"Current streak {plural(f['current'], 'day')}, longest {plural(f['longest'][0], 'day')}. "
            f"Heatmap of daily contributions; a small square hops from one active day to the next and today's square pulses.")
    if not mobile:
        body = [t(1158, 106, stamp, 13, th["muted"], "mono", "end"),
                t(38, 106, f"{plural(f['total'], 'contribution')} in the last year", 42, th["ink"], "serif")]
        grid, css = heatmap(th, data["days"], f["today"], 88, 160, 53, 20, 16, 42)
        body += grid
        body += [t(88, 328, f"{f['all_time']:,} since joining", 12, th["muted"], "mono")] if f["all_time"] != f["total"] else []
        body += legend(th, 1144, 328)
        for i, (label, value, sub) in enumerate(activity_tiles(f)):
            body += tile(th, 42 + i * 287, 350, 255, 112, label, value, sub, cursor=i == 0)
        return svg(1200, 460, "Contribution activity", desc, body, css, th["bg"], shift=30, drift=BLACK_TONES)
    body = [t(28, 100, plural(f["total"], "contribution"), 40, th["ink"], "serif"),
            t(28, 146, "in the last year", 40, th["ink"], "serif")]
    grid, css = heatmap(th, data["days"], f["today"], 72, 204, 26, 19, 15, 30)
    body += grid
    body += [t(30, 364, stamp, 12, th["muted"], "mono")] + legend(th, 568, 364)
    for i, (label, value, sub) in enumerate(activity_tiles(f)):
        body += tile(th, 30 + (i % 2) * 277, 388 + (i // 2) * 124, 263, 108, label, value, sub, 34, 22, cursor=i == 0)
    return svg(600, 620, "Contribution activity", desc, body, css, th["bg"], shift=30, drift=BLACK_TONES)


def bars(th, monthly, x0, x1, base, height, bar, sky):
    """Monthly bars that spring up, with small commit squares falling into each one."""
    pitch = (x1 - x0) / len(monthly)
    top = max(1, max(m["count"] for m in monthly))
    out = [r(x0, base, x1 - x0, 1.5, th["rule"])]
    for i, m in enumerate(monthly):
        cx = x0 + pitch * i + pitch / 2
        h = max(2, height * m["count"] / top) if m["count"] else 0
        if h:
            out.append(r(cx - bar / 2, base - h, bar, h, th["mark"], 4, delay(i * 70, "rise")))
            for j in range(min(3, 1 + m["count"] // 20)):
                start = 1300 + ((i * 530 + j * 1400) % 4200)
                out.append(r(cx - 3.5, sky, 7, 7, th["mark"], 1.5,
                             f' class="drop" style="--fall:{base - h - sky - 8:g}px;animation-delay:{start}ms"'))
        out.append(f'<g{delay(600 + i * 70, "fade")}>'
                   + t(cx, base - h - 10, m["count"], 14, th["ink"] if m["count"] else th["muted"], "num", "middle") + "</g>")
        year, month = map(int, m["month"].split("-"))
        out.append(t(cx, base + 24, MONTHS[month - 1].title(), 12, th["muted"], "mono", "middle"))
        if month == 1 or i == 0:
            out.append(t(cx, base + 42, year, 12, th["accent"], "mono", "middle"))
    return out


def commit_tiles(data, f):
    busiest = f["busiest_month"]
    year, month = map(int, busiest["month"].split("-"))
    active = sum(1 for m in data["monthly_commits"] if m["count"])
    return [
        ("Commits", f"{data['totals']['commits']:,}", "in public repos"),
        ("Repositories", f"{data['totals']['repos']}", "with commits"),
        ("Busiest month", f"{busiest['count']}", f"{MONTHS[month - 1].title()} {year}"),
        ("Active months", f"{active}", "out of 12"),
    ]


def footnote(totals, f):
    parts = [f"most active on {f['weekday']}s"] if f["weekday"] else []
    parts += [plural(totals[k], w) for k, w in (("prs", "pull request"), ("issues", "issue"), ("reviews", "review")) if totals[k]]
    text = ", ".join(parts)
    return text[:1].upper() + text[1:]


def commits_panel(data, mobile):
    th = THEMES["cobalt"]
    f = figures(data)
    tot = data["totals"]
    first_month = data["monthly_commits"][0]["month"]
    y, m = map(int, first_month.split("-"))
    repos = plural(tot["repos"], "repository", "repositories")
    headline = f"{plural(tot['commits'], 'commit')} across {repos}"
    desc = (f"{headline}. Monthly commit counts since {MONTHS[m - 1].title()} {y}: "
            + ", ".join(f"{x['month']} {x['count']}" for x in data["monthly_commits"]) + ".")
    extra = footnote(tot, f)
    if not mobile:
        body = [t(1158, 106, f"since {MONTHS[m - 1].title()} {y}", 13, th["muted"], "mono", "end"),
                t(38, 106, headline, 42, th["ink"], "serif")]
        body += bars(th, data["monthly_commits"], 42, 752, 340, 160, 30, 128)
        for i, (label, value, sub) in enumerate(commit_tiles(data, f)):
            body += tile(th, 800 + (i % 2) * 187, 140 + (i // 2) * 122, 171, 108, label, value, sub, 34, 20)
        body.append(t(1158, 408, extra, 14, th["muted"], anchor="end"))
        return svg(1200, 402, "Commits by month", desc, body, bg=th["bg"], shift=30, drift=COBALT_TONES)
    body = [t(28, 100, plural(tot["commits"], "commit"), 40, th["ink"], "serif"),
            t(28, 146, f"across {repos}", 40, th["ink"], "serif")]
    body += bars(th, data["monthly_commits"], 30, 570, 380, 160, 24, 168)
    for i, (label, value, sub) in enumerate(commit_tiles(data, f)):
        body += tile(th, 30 + (i % 2) * 277, 446 + (i // 2) * 124, 263, 108, label, value, sub, 34, 22)
    body.append(t(30, 726, fit(extra, 15, "sans", 540), 15, th["muted"]))
    return svg(600, 722, "Commits by month", desc, body, bg=th["bg"], shift=30, drift=COBALT_TONES)


def repo_rows(th, repos, login, x0, x1, y0, pitch, count):
    """Bars grow in, then a gloss sweeps across each one in turn."""
    rows = [x for x in repos if x["name"] != login][:count]
    top = max([x["commits"] for x in rows] or [1])
    out = []
    for i, repo in enumerate(rows):
        name, colour = FEATURED.get(repo["name"], (repo["name"], th["ink"]))
        y = y0 + i * pitch
        w = max(8, (x1 - x0) * repo["commits"] / top)
        out.append(t(x0, y, fit(name, 19, "sans", x1 - x0 - 110), 19, th["ink"], "sans", weight="600"))
        out.append(t(x1, y, plural(repo["commits"], "commit"), 14, th["muted"], "mono", "end"))
        out.append(r(x0, y + 12, x1 - x0, 8, th["track"], 4))
        out.append(r(x0, y + 12, w, 8, colour, 4, delay(i * 90, "grow")))
        out.append(f'<clipPath id="bar{i}">{r(x0, y + 12, w, 8, "#000", 4)}</clipPath><g clip-path="url(#bar{i})">'
                   + r(x0 - 70, y + 12, 70, 8, "url(#gloss)", 0,
                       f' class="shine" style="--d:{w + 70:g}px;animation-delay:{1500 + i * 420}ms"') + "</g>")
    return out


def commit_rows(th, recent, x0, x1, y0, pitch, count, size):
    """A git-log style list: a rail of commit dots, HEAD on top, and a dot that runs down the rail."""
    rows = recent[:count]
    if not rows:
        return [], ""
    accent = th["accent"]
    rail, tx = x0 + 6, x0 + 28
    out = [f'<path d="M{rail} {y0 - 4}V{y0 - 4 + (len(rows) - 1) * pitch}" stroke="{th["rule"]}" stroke-width="2"/>']
    points = []
    for i, c in enumerate(rows):
        y = y0 + i * pitch
        points.append((rail, y - 4))
        name = FEATURED.get(c["repo"], (c["repo"],))[0]
        diff = f"+{c['additions']:,} −{c['deletions']:,}" if "additions" in c else ""
        meta = fit(f"{short_date(parse(c['date']))}  {name}", 12, "mono",
                   x1 - tx - (mono_width(diff, 12) + 16 if diff else 0) - (58 if i == 0 else 0))
        row = [f'<circle cx="{rail}" cy="{y - 4}" r="5.5" fill="{accent if i == 0 else th["bg"]}" stroke="{accent}" stroke-width="2"/>',
               t(tx, y, meta, 12, accent, "mono")]
        if i == 0:
            px = tx + mono_width(meta, 12) + 10
            row += [f'<g class="glow">{r(px, y - 13, 46, 17, accent, 8.5)}'
                    f'{t(px + 23, y - 0.5, "HEAD", 11, th["bg"], "num", "middle", spacing=".6")}</g>']
        if diff:
            row.append(t(x1, y, diff, 12, th["muted"], "mono", "end"))
        row.append(t(tx, y + 25, fit(c["message"], size, "sans", x1 - tx), size, th["ink"]))
        out.append(f'<g{delay(300 + i * 110, "slide")}>{"".join(row)}</g>')
    if len(points) < 2:
        return out, ""
    seconds = 1.1 * len(points) + 2
    css, times = hops("head", points, seconds)
    for (x, y), at in zip(points, times):
        out.append(f'<circle class="box ring" style="--t:{seconds:.1f}s;animation-delay:{at:.2f}s" cx="{x}" cy="{y:g}" '
                   f'r="6" fill="none" stroke="{accent}" stroke-width="2"/>')
    out.append(f'<circle class="head" transform="translate({points[0][0]} {points[0][1]:g})" r="3" fill="{th["mark"]}"/>')
    return out, css + ".glow{animation:glow 2.4s ease-in-out infinite}@keyframes glow{50%{opacity:.55}}"


def latest_per_repo(recent):
    """Most recent meaningful commit per repository; merge commits say little about the work."""
    seen, out = set(), []
    for c in recent:
        message = c["message"].strip()
        if len(message) < 3 or message.startswith(("Merge pull request", "Merge branch", "Merge remote")):
            continue
        if c["repo"] not in seen:
            seen.add(c["repo"])
            out.append(c)
    return out


def repos_panel(data, mobile):
    th = THEMES["ivory"]
    login = data["login"]
    shown = [x for x in data["repos"] if x["name"] != login]
    latest = latest_per_repo(data["recent"])
    desc = ("Commits per repository over 12 months: "
            + ", ".join(f"{FEATURED.get(x['name'], (x['name'],))[0]} {x['commits']}" for x in shown[:6])
            + ". Latest commits: "
            + "; ".join(f"{c['date']} {c['repo']}: {c['message']}" for c in latest[:6]) + ".")
    if not mobile:
        body = [t(38, 106, "Where my commits went", 42, th["ink"], "serif"),
                r(42, 132, 1116, 1.5, th["rule"]),
                t(42, 172, "Last 12 months", 15, th["accent"], weight="600"),
                t(640, 172, "Latest commit in each repo", 15, th["accent"], weight="600"),
                r(608, 150, 1.5, 336, th["rule"])]
        body += repo_rows(th, data["repos"], login, 42, 568, 214, 52, 6)
        log, css = commit_rows(th, latest, 640, 1158, 210, 52, 6, 18)
        return svg(1200, 490, "Repository activity", desc, body + log, css, th["bg"], shift=30, paper=True)
    body = [t(28, 100, "Where my", 40, th["ink"], "serif"),
            t(28, 146, "commits went", 40, th["ink"], "serif"),
            t(30, 194, "Last 12 months", 15, th["accent"], weight="600")]
    body += repo_rows(th, data["repos"], login, 30, 570, 236, 54, 5)
    body += [r(30, 498, 540, 1.5, th["rule"]), t(30, 536, "Latest commit in each repo", 15, th["accent"], weight="600")]
    log, css = commit_rows(th, latest, 30, 570, 578, 60, 5, 19)
    return svg(600, 836, "Repository activity", desc, body + log, css, th["bg"], shift=30, paper=True)


PANELS = {"p5-activity": activity_panel, "p5-commits": commits_panel, "p5-repos": repos_panel}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--login", default=os.environ.get("GITHUB_REPOSITORY_OWNER"))
    parser.add_argument("--out", default="assets")
    parser.add_argument("--fixture", help="render from a saved JSON file instead of the API")
    parser.add_argument("--save", help="also write the fetched data to this JSON file")
    args = parser.parse_args()

    if args.fixture:
        with open(args.fixture, encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token or not args.login:
            raise SystemExit("Set GITHUB_TOKEN and pass --login (or use --fixture).")
        data = fetch(args.login, token, datetime.now(timezone.utc).date())
    if args.save:
        with open(args.save, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, ensure_ascii=False)

    os.makedirs(args.out, exist_ok=True)
    for name, render in PANELS.items():
        for mobile in (False, True):
            path = os.path.join(args.out, f"{name}{'-mobile' if mobile else ''}.svg")
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(render(data, mobile))
            print("wrote", path)


if __name__ == "__main__":
    main()
