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

Like the other p5 panels, the SVGs use no JavaScript, external fonts or images,
and every animation stops under prefers-reduced-motion.
"""

import argparse
import json
import os
import urllib.request
from datetime import date, datetime, timedelta, timezone
from xml.sax.saxutils import escape

IVORY, INK = "#F5F0E7", "#252C36"
MUTED = "#5E636B"
BURGUNDY, BLUSH = "#96394A", "#EAD5D4"
BLUE, MIST = "#315A88", "#D7E2ED"
AMBER, SAND = "#7B5725", "#EADFC6"
HEAT = ["#E6DED0", "#E4C4C7", "#CC8B97", "#B05868", BURGUNDY]

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

STYLE = """<style>
.sans{font-family:'Segoe UI',Helvetica,Arial,sans-serif}.serif{font-family:Georgia,'Times New Roman',serif}.mono{font-family:Consolas,'Courier New',monospace}
.sweep{animation:sweep 14s ease-in-out infinite}.pulse{animation:pulse 3s ease-in-out infinite}.rise{transform-box:fill-box;transform-origin:50% 100%;animation:rise 1.1s cubic-bezier(.2,.8,.2,1) both}.grow{transform-box:fill-box;transform-origin:0 50%;animation:grow 1.1s cubic-bezier(.2,.8,.2,1) both}
@keyframes sweep{0%,100%{transform:translateX(0);opacity:0}8%,92%{opacity:.5}50%{transform:translateX(var(--d))}}@keyframes pulse{0%,100%{opacity:.25}50%{opacity:1}}@keyframes rise{from{transform:scaleY(0)}}@keyframes grow{from{transform:scaleX(0)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
</style>"""


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

WIDTH = {"sans": .54, "mono": .55, "serif": .5}


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


def svg(w, h, title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            f'{STYLE}<defs><clipPath id="frame"><rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{IVORY}"/>'
            f'</clipPath></defs><g clip-path="url(#frame)">{r(0, 0, w, h, IVORY)}{"".join(body)}</g></svg>\n')


def tile(x, y, w, h, label, value, sub, accent, tint, value_size=38, pad=24):
    return [r(x, y, w, h, tint, 10),
            t(x + pad, y + 32, label, 13, accent, "mono"),
            t(x + pad - 2, y + 32 + value_size + 4, value, value_size, INK, "serif"),
            t(x + pad, y + h - 20, fit(sub, 15, "sans", w - 2 * pad), 15, MUTED)]


def plural(n, word, many=None):
    return f"{n:,} {word if n == 1 else many or word + 's'}"


def heatmap(days, today, x0, y0, weeks, pitch, cell, label_x):
    level = levels(days)
    counts = {parse(x["date"]): x["count"] for x in days}
    first = today - timedelta(days=(today.weekday() + 1) % 7 + 7 * (weeks - 1))
    out = [t(label_x, y0 + pitch * row + cell - 3, name, 12, MUTED, "mono")
           for row, name in ((1, "MON"), (3, "WED"), (5, "FRI"))]
    last_label = -9
    for col in range(weeks):
        sunday = first + timedelta(days=7 * col)
        starts_month = sunday.day <= 7 if col == 0 else sunday.month != (sunday - timedelta(days=7)).month
        if starts_month and col - last_label >= 3 and col < weeks - 2:
            out.append(t(x0 + col * pitch, y0 - 12, MONTHS[sunday.month - 1], 12, MUTED, "mono"))
            last_label = col
        for row in range(7):
            d = sunday + timedelta(days=row)
            if d > today:
                break
            out.append(r(x0 + col * pitch, y0 + row * pitch, cell, cell, HEAT[level(counts.get(d, 0))], 3))
    col, row = weeks - 1, (today.weekday() + 1) % 7
    out.append(f'<rect class="pulse" x="{x0 + col * pitch - 2.5:g}" y="{y0 + row * pitch - 2.5:g}" width="{cell + 5}" '
               f'height="{cell + 5}" rx="4" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    travel = (weeks - 1) * pitch
    out.append(f'<rect class="sweep" style="--d:{travel}px" x="{x0 + cell / 2 - 1:g}" y="{y0 - 4}" width="2" '
               f'height="{7 * pitch:g}" fill="{BURGUNDY}" opacity="0"/>')
    return out


def legend(x_end, y):
    out, x = [t(x_end, y, "MORE", 12, MUTED, "mono", "end")], x_end - 44
    for colour in reversed(HEAT):
        x -= 18
        out.append(r(x, y - 11, 13, 13, colour, 3))
    out.append(t(x - 8, y, "LESS", 12, MUTED, "mono", "end"))
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
        ("CURRENT STREAK", plural(f["current"], "day"), current_sub),
        ("LONGEST STREAK", plural(longest, "day"), longest_sub),
        ("ACTIVE DAYS", f"{f['active_days']}", f"of the last {f['span_days']}"),
        ("BEST DAY", f"{best['count']}", f"contributions · {short_date(parse(best['date']))}" if best["count"] else "—"),
    ]


def activity_panel(data, mobile):
    f = figures(data)
    stamp = f"UPDATED {f['today'].day} {MONTHS[f['today'].month - 1]} {f['today'].year}"
    desc = (f"{plural(f['total'], 'contribution')} in the last year, {f['active_days']} active days. "
            f"Current streak {plural(f['current'], 'day')}, longest {plural(f['longest'][0], 'day')}. "
            f"Heatmap of daily contributions; a slow sweep crosses the grid and today's square pulses.")
    if not mobile:
        body = [t(42, 49, "CONTRIBUTIONS / LAST 12 MONTHS", 15, BURGUNDY, "mono"),
                t(1158, 49, stamp, 13, MUTED, "mono", "end"),
                t(38, 111, f"{plural(f['total'], 'contribution')} in the last year.", 44, INK, "serif")]
        body += heatmap(data["days"], f["today"], 88, 172, 53, 20, 16, 42)
        body += [t(88, 342, f"{f['all_time']:,} ALL TIME", 12, MUTED, "mono")] if f["all_time"] != f["total"] else []
        body += legend(1144, 342)
        for i, (label, value, sub) in enumerate(activity_tiles(f)):
            body += tile(42 + i * 287, 370, 255, 118, label, value, sub, BURGUNDY, BLUSH)
        return svg(1200, 520, "Contribution activity", desc, body)
    body = [t(30, 43, "CONTRIBUTIONS / 26 WEEKS", 15, BURGUNDY, "mono"),
            t(28, 104, plural(f["total"], "contribution"), 41, INK, "serif"),
            t(28, 152, "in the last year.", 41, INK, "serif")]
    body += heatmap(data["days"], f["today"], 72, 214, 26, 19, 15, 30)
    body += [t(30, 374, stamp, 12, MUTED, "mono")] + legend(568, 374)
    for i, (label, value, sub) in enumerate(activity_tiles(f)):
        body += tile(30 + (i % 2) * 277, 400 + (i // 2) * 130, 263, 112, label, value, sub, BURGUNDY, BLUSH, 34, 22)
    return svg(600, 672, "Contribution activity", desc, body)


def bars(monthly, x0, x1, base, height, bar):
    pitch = (x1 - x0) / len(monthly)
    top = max(1, max(m["count"] for m in monthly))
    out = [r(x0, base, x1 - x0, 1.5, "#C9CED6")]
    for i, m in enumerate(monthly):
        cx = x0 + pitch * i + pitch / 2
        h = max(2, height * m["count"] / top) if m["count"] else 0
        if h:
            out.append(r(cx - bar / 2, base - h, bar, h, BLUE, 4, f' class="rise" style="animation-delay:{i * 70}ms"'))
        out.append(t(cx, base - h - 10, m["count"], 14, INK if m["count"] else MUTED, "mono", "middle"))
        year, month = map(int, m["month"].split("-"))
        out.append(t(cx, base + 24, MONTHS[month - 1], 12, MUTED, "mono", "middle"))
        if month == 1 or i == 0:
            out.append(t(cx, base + 42, year, 12, BLUE, "mono", "middle"))
    return out


def commit_tiles(data, f):
    busiest = f["busiest_month"]
    year, month = map(int, busiest["month"].split("-"))
    active = sum(1 for m in data["monthly_commits"] if m["count"])
    return [
        ("COMMITS", f"{data['totals']['commits']:,}", "public repos"),
        ("REPOSITORIES", f"{data['totals']['repos']}", "with commits"),
        ("BUSIEST MONTH", f"{busiest['count']}", f"{MONTHS[month - 1].title()} {year}"),
        ("ACTIVE MONTHS", f"{active}", "of the last 12"),
    ]


def footnote(totals, f):
    parts = [f"most active on {f['weekday']}s"] if f["weekday"] else []
    parts += [plural(totals[k], w) for k, w in (("prs", "pull request"), ("issues", "issue"), ("reviews", "review")) if totals[k]]
    return " · ".join(parts).upper()


def commits_panel(data, mobile):
    f = figures(data)
    tot = data["totals"]
    first_month = data["monthly_commits"][0]["month"]
    y, m = map(int, first_month.split("-"))
    repos = plural(tot["repos"], "repository", "repositories")
    headline = f"{plural(tot['commits'], 'commit')} across {repos}."
    desc = (f"{headline} Monthly commit counts since {MONTHS[m - 1].title()} {y}: "
            + ", ".join(f"{x['month']} {x['count']}" for x in data["monthly_commits"]) + ".")
    extra = footnote(tot, f)
    if not mobile:
        body = [t(42, 49, "COMMITS / BY MONTH", 15, BLUE, "mono"),
                t(1158, 49, f"SINCE {MONTHS[m - 1]} {y}", 13, MUTED, "mono", "end"),
                t(38, 111, headline, 44, INK, "serif")]
        body += bars(data["monthly_commits"], 42, 752, 362, 170, 30)
        for i, (label, value, sub) in enumerate(commit_tiles(data, f)):
            body += tile(800 + (i % 2) * 187, 156 + (i // 2) * 128, 171, 112, label, value, sub, BLUE, MIST, 34, 20)
        body.append(t(1158, 440, extra, 13, BLUE, "mono", "end"))
        return svg(1200, 470, "Commits by month", desc, body)
    body = [t(30, 43, "COMMITS / BY MONTH", 15, BLUE, "mono"),
            t(28, 104, plural(tot["commits"], "commit"), 41, INK, "serif"),
            t(28, 152, f"across {repos}.", 41, INK, "serif")]
    body += bars(data["monthly_commits"], 30, 570, 398, 170, 24)
    for i, (label, value, sub) in enumerate(commit_tiles(data, f)):
        body += tile(30 + (i % 2) * 277, 468 + (i // 2) * 130, 263, 112, label, value, sub, BLUE, MIST, 34, 22)
    body.append(t(30, 760, fit(extra, 13, "mono", 540), 13, BLUE, "mono"))
    return svg(600, 790, "Commits by month", desc, body)


def repo_rows(repos, login, x0, x1, y0, pitch, count):
    rows = [x for x in repos if x["name"] != login][:count]
    top = max([x["commits"] for x in rows] or [1])
    out = []
    for i, repo in enumerate(rows):
        name, colour = FEATURED.get(repo["name"], (repo["name"], INK))
        y = y0 + i * pitch
        out.append(t(x0, y, fit(name, 19, "sans", x1 - x0 - 110), 19, INK, "sans", weight="600"))
        out.append(t(x1, y, plural(repo["commits"], "commit"), 14, MUTED, "mono", "end"))
        out.append(r(x0, y + 12, x1 - x0, 8, "#E6DED0", 4))
        out.append(r(x0, y + 12, max(8, (x1 - x0) * repo["commits"] / top), 8, colour, 4,
                     f' class="grow" style="animation-delay:{i * 90}ms"'))
    return out


def commit_rows(recent, x0, x1, y0, pitch, count, size):
    out = []
    for i, c in enumerate(recent[:count]):
        y = y0 + i * pitch
        name = FEATURED.get(c["repo"], (c["repo"],))[0]
        meta = f"{short_date(parse(c['date'])).upper()}  ·  {name.upper()}"
        diff = f"+{c['additions']:,} −{c['deletions']:,}" if "additions" in c else ""
        out.append(t(x0, y, fit(meta, 12, "mono", x1 - x0 - 110), 12, AMBER, "mono"))
        if diff:
            out.append(t(x1, y, diff, 12, MUTED, "mono", "end"))
        out.append(t(x0, y + 25, fit(c["message"], size, "sans", x1 - x0), size, INK))
    return out


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
    login = data["login"]
    shown = [x for x in data["repos"] if x["name"] != login]
    latest = latest_per_repo(data["recent"])
    desc = ("Commits per repository over 12 months: "
            + ", ".join(f"{FEATURED.get(x['name'], (x['name'],))[0]} {x['commits']}" for x in shown[:6])
            + ". Latest commits: "
            + "; ".join(f"{c['date']} {c['repo']}: {c['message']}" for c in latest[:6]) + ".")
    if not mobile:
        body = [t(42, 49, "REPOSITORIES / WHERE THE COMMITS WENT", 15, AMBER, "mono"),
                t(38, 111, "Most active repositories.", 44, INK, "serif"),
                r(42, 140, 1116, 1.5, "#DCD3C3"),
                t(42, 182, "LAST 12 MONTHS", 13, AMBER, "mono"),
                t(640, 182, "LATEST COMMIT PER REPOSITORY", 13, AMBER, "mono"),
                r(608, 160, 1.5, 356, "#DCD3C3")]
        body += repo_rows(data["repos"], login, 42, 568, 228, 56, 6)
        body += commit_rows(latest, 640, 1158, 220, 56, 6, 18)
        return svg(1200, 560, "Repository activity", desc, body)
    body = [t(30, 43, "REPOSITORIES", 15, AMBER, "mono"),
            t(28, 104, "Most active", 41, INK, "serif"),
            t(28, 152, "repositories.", 41, INK, "serif"),
            t(30, 202, "LAST 12 MONTHS", 13, AMBER, "mono")]
    body += repo_rows(data["repos"], login, 30, 570, 246, 56, 5)
    body += [r(30, 516, 540, 1.5, "#DCD3C3"), t(30, 556, "LATEST COMMIT PER REPOSITORY", 13, AMBER, "mono")]
    body += commit_rows(latest, 30, 570, 596, 62, 5, 19)
    return svg(600, 900, "Repository activity", desc, body)


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
