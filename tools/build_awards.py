"""Generate one page per award, in each mockup's style, from tools/awards_data.py.
Run from the repo root:  python3 tools/build_awards.py
"""
import os, re, sys
from html import escape as e
from itertools import groupby

sys.path.insert(0, os.path.dirname(__file__))
from awards_data import AWARDS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONTS = {
    "windowed": "family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@400;700;800",
    "flat": "family=Inter:wght@400;600;700;900&family=JetBrains+Mono:wght@400;700;800",
    "neon": "family=Archivo+Black&family=Space+Mono:wght@400;700",
    "classic": "family=Pixelify+Sans:wght@400;600;700",
}


def head(site, title):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} — AoIR</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS[site]}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body data-page="awards">
"""


def grouped(a):
    """Travel rows -> [(year, [names])]."""
    return [(y, [r[1] for r in rs]) for y, rs in groupby(a["rows"], key=lambda r: r[0])]


def who(r):
    """Recipient cell text: name, then affiliation/publisher."""
    return r[1], r[2]


def others(a):
    return [x for x in AWARDS if x is not a]


# --------------------------------------------------------------------------- windowed / flat
def win(site, tag, label, slug, cls, bar, body):
    if site == "flat":
        label = "&lt;h1&gt;" if tag == "main" else f'&lt;{tag} id="{slug}"&gt;'
    extra = ' id="main"' if tag == "main" else ""
    return (f'  <{tag} class="win {cls}"{extra}>\n'
            f'    <div class="win-bar {bar}"><span class="file">{label}</span><span class="ctl"><i></i><i></i></span></div>\n'
            f'    <div class="win-body">\n{body}\n    </div>\n  </{tag}>\n')


def page_windowed(site, a):
    c = "c-" + a["color"]
    intro = "\n".join(f'      <p{" style=\"font-size:19px\"" if i == 0 else ""}>{e(p)}</p>' for i, p in enumerate(a["intro"]))
    words = a["name"].rsplit(" ", 1)
    h1 = f'{e(words[0])} <mark>{e(words[1])}</mark>.'
    latest = "\n".join(f'        <li><b>{e(n)}</b><br><i>{e(w)}</i></li>' for n, w in a["latest"])
    facts = "\n".join(f'        <dt>{e(k.lower())}</dt><dd>{e(v)}</dd>' for k, v in a["facts"])
    rules = "\n".join(f"        <li>{e(r)}</li>" for r in a["rules"])
    if a.get("group_by_year"):
        rows = "\n".join(f'        <tr><td>{y}</td><td>{e(", ".join(ns))}</td></tr>' for y, ns in grouped(a))
    else:
        rows = "\n".join(
            f'        <tr><td>{r[0]}</td><td><b>{e(r[1])}</b>{(" · " + e(r[2])) if r[2] else ""}<br><i>{e(r[3])}</i></td>'
            f'<td class="kind">{e(r[4])}</td></tr>' for r in a["rows"])
    foot = f'\n      <p class="note" style="margin-top:12px">{e(a["footnote"])}</p>' if a["footnote"] else ""
    more = " · ".join(f'<a href="{x["slug"]}.html">{e(x["short"])}</a>' for x in others(a))
    out = head(site, a["name"]) + '<div class="desk">\n  <header id="chrome-top"></header>\n\n'
    out += win(site, "main", f'awards/{a["slug"][6:]}.html', "main", "span-8", c,
               f'      <span class="tag"><a href="awards.html">/awards</a>/{a["slug"][6:]}</span>\n      <h1 style="font-size:clamp(36px,5.5vw,60px)">{h1}</h1>\n{intro}')
    out += win(site, "aside", "latest.txt", "latest", "span-4 nudge-down tilt-r sticky-note", "",
               f'      <h2 class="sm">{e(a["latest_label"])}</h2>\n      <ul class="dash">\n{latest}\n      </ul>')
    out += win(site, "section", "recipients.csv", "recipients", "span-12", "",
               f'      <h2>Past recipients</h2>\n      <table class="index">\n{rows}\n      </table>{foot}')
    out += win(site, "section", "details.txt", "details", "span-6", c,
               f'      <h2 class="sm">Details</h2>\n      <dl class="kv">\n{facts}\n      </dl>')
    out += win(site, "section", "how.md", "how", "span-6 nudge-down", "",
               f'      <h2 class="sm">{e(a["rules_title"])}</h2>\n      <ul class="dash small">\n{rules}\n      </ul>\n      <p class="small" style="margin-top:12px">Other awards: {more}</p>')
    out += '\n  <footer id="chrome-bottom"></footer>\n</div>\n<script src="site.js"></script>\n</body>\n</html>\n'
    return out


# --------------------------------------------------------------------------- neon
def page_neon(a):
    c = "c-" + a["color"]
    intro = "\n".join(f'      <p style="font-size:16px;max-width:42em">{e(p)}</p>' for p in a["intro"])
    big = e(a["name"]).replace("Annual ", "").replace(" Award", "<br>Award").replace(" Travel Scholarship", "<br>Travel Scholarship").replace(" Student Paper", "<br>Student Paper")
    latest = "\n".join(f'        <li><span><b>{e(n)}</b><br>{e(w)}</span></li>' for n, w in a["latest"])
    facts = "\n".join(f'        <li><span><b>{e(k)}</b></span><span style="text-align:right">{e(v)}</span></li>' for k, v in a["facts"])
    rules = "\n".join(f"        <li>{e(r)}</li>" for r in a["rules"])
    if a.get("group_by_year"):
        rows = "\n".join(f'        <li><span class="d">{y}</span><span>{e(", ".join(ns))}</span></li>' for y, ns in grouped(a))
    else:
        rows = "\n".join(
            f'        <li><span class="d">{r[0]}</span><span><b>{e(r[1])}</b>{(" · " + e(r[2])) if r[2] else ""}{(" · <i>" + e(r[4]) + "</i>") if r[4] else ""}<br>{e(r[3])}</span></li>'
            for r in a["rows"])
    foot = f'\n      <p style="margin-top:12px;font-size:12px">{e(a["footnote"])}</p>' if a["footnote"] else ""
    more = "".join(f'<a class="btn alt" href="{x["slug"]}.html">{e(x["short"])}</a>' for x in others(a))
    return head("neon", a["name"]) + f'''<div class="zine">
  <header id="chrome-top"></header>
  <main style="display:contents" id="main">
    <section class="blk {c} hero s-8">
      <span class="kicker">&gt;&gt; <a href="awards.html">Awards</a></span>
      <h1 style="font-size:clamp(38px,6.5vw,80px)">{big}</h1>
{intro}
    </section>
    <section class="blk c-yellow s-4">
      <span class="kicker">{e(a["latest_label"])}</span>
      <ul class="rows">
{latest}
      </ul>
    </section>
    <section class="blk c-white">
      <h2>Back issues: past recipients</h2>
      <ul class="rows dated">
{rows}
      </ul>{foot}
    </section>
    <section class="blk c-lilac s-6">
      <h2 class="sm">Details</h2>
      <ul class="rows">
{facts}
      </ul>
    </section>
    <section class="blk c-white s-6">
      <h2 class="sm">{e(a["rules_title"])}</h2>
      <ul class="rows">
{rules}
      </ul>
      <div class="btn-row">{more}</div>
    </section>
  </main>
  <footer id="chrome-bottom"></footer>
</div>
<script src="site.js"></script>
</body>
</html>
'''


# --------------------------------------------------------------------------- classic
def cwin(cls, wid, title, body, extra=""):
    return (f'    <section class="window {cls}" aria-labelledby="{wid}">\n'
            f'      <div class="titlebar"><button class="close" aria-label="Collapse window"></button><span class="t" id="{wid}">{e(title)}</span><button class="shade" aria-label="Windowshade"></button></div>\n'
            f'{extra}      <div class="wbody">\n{body}\n      </div>\n    </section>\n\n')


def page_classic(a):
    intro = "\n".join(f'        <p class="read">{e(p)}</p>' for p in a["intro"])
    latest = "\n".join(f'            <p><b>{e(n)}</b><br><i>{e(w)}</i></p>' for n, w in a["latest"])
    facts = "\n".join(f'          <dt>{e(k)}:</dt><dd>{e(v)}</dd>' for k, v in a["facts"])
    rules = "\n".join(f"          <li>{e(r)}</li>" for r in a["rules"])
    if a.get("group_by_year"):
        g = grouped(a)
        head_row = "<tr><th>Year</th><th>Recipients</th></tr>"
        rows = "\n".join(f'            <tr><td class="meta"><span class="ico folder"></span>{y}</td><td>{e(", ".join(ns))}</td></tr>' for y, ns in g)
        count = f"{len(a['rows'])} items"
    else:
        head_row = f"<tr><th>{a['cols'][0]}</th><th>{a['cols'][1]}</th><th>{a['cols'][2]}</th></tr>"
        rows = "\n".join(
            f'            <tr><td class="meta">{r[0]}</td><td><span class="ico"></span><b>{e(r[1])}</b>{("<br><span class=small>" + e(r[2]) + "</span>") if r[2] else ""}</td>'
            f'<td><i>{e(r[3])}</i>{("<br><span class=small>" + e(r[4]) + "</span>") if r[4] else ""}</td></tr>' for r in a["rows"])
        count = f"{len(a['rows'])} items"
    foot = f'\n        <p class="small" style="padding:8px 12px;margin:0">{e(a["footnote"])}</p>' if a["footnote"] else ""
    more = "".join(f'<a class="btn" href="{x["slug"]}.html">{e(x["short"])}…</a>' for x in others(a))
    out = head("classic", a["name"]) + '<header id="menubar"></header>\n<div class="desktop">\n  <main class="stage" id="main">\n\n'
    out += cwin("span-8", "w1", a["name"], f'        <h1>{e(a["name"])}</h1>\n{intro}')
    out += cwin("alert span-4 push-down", "w2", a["latest_label"],
                f'        <svg viewBox="0 0 16 16" shape-rendering="crispEdges" aria-hidden="true"><circle cx="8" cy="6" r="4.5" fill="#fff" stroke="#000"/><circle cx="8" cy="6" r="2"/><path d="M5.5 9.5 L4.5 15 L6.5 13.5 L8 15 L9.5 13.5 L11.5 15 L10.5 9.5" fill="#fff" stroke="#000"/></svg>\n          <div>\n{latest}\n          </div>')
    out += (f'    <section class="window span-12" aria-labelledby="w3">\n'
            f'      <div class="titlebar"><button class="close" aria-label="Collapse window"></button><span class="t" id="w3">Past Recipients</span><button class="shade" aria-label="Windowshade"></button></div>\n'
            f'      <div class="infobar"><span>{count}</span><span>newest first</span></div>\n'
            f'      <div class="wbody flush">\n        <table class="list">\n          <thead>{head_row}</thead>\n          <tbody>\n{rows}\n          </tbody>\n        </table>{foot}\n      </div>\n    </section>\n\n')
    out += cwin("span-6", "w4", "Get Info", f'        <dl class="kv">\n{facts}\n        </dl>')
    out += cwin("span-6 push-down", "w5", a["rules_title"],
                f'        <div class="ruled small">\n        <ul>\n{rules}\n        </ul>\n        </div>\n        <div class="btn-row">{more}</div>')
    out += '    <footer id="strip"></footer>\n  </main>\n  <nav id="icons"></nav>\n</div>\n<script src="site.js"></script>\n</body>\n</html>\n'
    return out


def main():
    n = 0
    for a in AWARDS:
        for site in ("windowed", "flat", "neon", "classic"):
            html = page_neon(a) if site == "neon" else page_classic(a) if site == "classic" else page_windowed(site, a)
            open(os.path.join(ROOT, site, a["slug"] + ".html"), "w").write(html)
            n += 1
    print(f"wrote {n} pages")


if __name__ == "__main__":
    main()
