"""Generate the AoIRchive 'Past executive committees' page in each mockup's style.
Run from the repo root:  python3 tools/build_committees.py
"""
import os, sys
from html import escape as e

sys.path.insert(0, os.path.dirname(__file__))
from committees_data import TERMS, slugify
from build_awards import head

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = "aoirchive-committees"
INTRO = "Every AoIR executive committee since 1999. Each committee serves a two-year term."


def portrait(name):
    s = slugify(name)
    f = s if os.path.exists(os.path.join(ROOT, "assets", "committee", s + ".jpg")) else "initials-" + s
    return f'<img src="../assets/committee/{f}.jpg" alt="{e(name)}" width="160" height="160" loading="lazy">'


def cards(members):
    return "\n".join(
        f'        <figure class="person-card">{portrait(n)}<figcaption><span class="role">{e(r)}</span><span class="who">{e(n)}</span></figcaption></figure>'
        for r, n in members)


def jump():
    return " · ".join(f'<a href="#t{y[:4]}">{y}</a>' for y, _c, _m in TERMS)


def tid(y):
    return "t" + y[:4]


# windowed / flat --------------------------------------------------------------
def page_windowed(site):
    out = head(site, "Past executive committees").replace('data-page="awards"', 'data-page="about"')
    out += '<div class="desk">\n  <header id="chrome-top"></header>\n\n'
    lab = (lambda tag, f, slug: "&lt;h1&gt;" if tag == "main" else f'&lt;{tag} id="{slug}"&gt;') if site == "flat" else (lambda tag, f, slug: f)
    out += (f'  <main class="win span-12" id="main">\n    <div class="win-bar c-yellow"><span class="file">{lab("main", "aoirchive/executive-committees.html", "")}</span><span class="ctl"><i></i><i></i></span></div>\n'
            f'    <div class="win-body">\n      <span class="tag"><a href="about.html">/about</a>/aoirchive/executive-committees</span>\n'
            f'      <h1 style="font-size:clamp(36px,5.5vw,60px)">Past executive <mark>committees</mark>.</h1>\n      <p style="font-size:19px;max-width:44em">{e(INTRO)}</p>\n'
            f'      <p class="tags">terms: {jump()}</p>\n    </div>\n  </main>\n\n')
    for y, cur, members in TERMS:
        bar = "c-green" if cur else ""
        label = lab("section", f"committees/{y[:4]}.csv", tid(y))
        out += (f'  <section class="win span-12" id="{tid(y)}">\n    <div class="win-bar {bar}"><span class="file">{label}</span><span class="ctl"><i></i><i></i></span></div>\n'
                f'    <div class="win-body">\n      <h2>{y}{" <mark>current</mark>" if cur else ""}</h2>\n      <div class="people">\n{cards(members)}\n      </div>\n    </div>\n  </section>\n\n')
    out += '  <footer id="chrome-bottom"></footer>\n</div>\n<script src="site.js"></script>\n</body>\n</html>\n'
    return out


# neon -------------------------------------------------------------------------
def page_neon():
    colors = ["c-yellow", "c-cyan", "c-pink", "c-green", "c-lilac", "c-orange"]
    out = head("neon", "Past executive committees").replace('data-page="awards"', 'data-page="archive"')
    out += ('<div class="zine">\n  <header id="chrome-top"></header>\n  <main style="display:contents" id="main">\n'
            '    <section class="blk c-lilac hero">\n      <span class="kicker">&gt;&gt; AoIRchive</span>\n'
            '      <h1 style="font-size:clamp(40px,7vw,96px)">Past executive<br>committees</h1>\n'
            f'      <p style="font-size:16px;max-width:44em">{e(INTRO)}</p>\n      <p class="meta-line" style="font-size:13px">{jump()}</p>\n    </section>\n')
    for i, (y, cur, members) in enumerate(TERMS):
        out += (f'    <section class="blk {colors[i % len(colors)]}" id="{tid(y)}">\n      <span class="kicker">{"Current committee" if cur else "Back issue"}</span>\n'
                f'      <h2>{y}</h2>\n      <div class="people">\n{cards(members)}\n      </div>\n    </section>\n')
    out += '  </main>\n  <footer id="chrome-bottom"></footer>\n</div>\n<script src="site.js"></script>\n</body>\n</html>\n'
    return out


# classic ----------------------------------------------------------------------
def page_classic():
    out = head("classic", "Past executive committees").replace('data-page="awards"', 'data-page="about"')
    out += '<header id="menubar"></header>\n<div class="desktop">\n  <main class="stage" id="main">\n\n'
    out += ('    <section class="window span-12" aria-labelledby="w0">\n'
            '      <div class="titlebar"><button class="close" aria-label="Collapse window"></button><span class="t" id="w0">AoIRchive: Executive Committees</span><button class="shade" aria-label="Windowshade"></button></div>\n'
            f'      <div class="infobar"><span>{len(TERMS)} folders</span><span>1999 to now</span></div>\n'
            f'      <div class="wbody">\n        <h1>Past executive committees</h1>\n        <p class="read">{e(INTRO)}</p>\n        <p class="small">{jump()}</p>\n      </div>\n    </section>\n\n')
    for i, (y, cur, members) in enumerate(TERMS):
        out += (f'    <section class="window span-12" id="{tid(y)}" aria-labelledby="w{i+1}">\n'
                f'      <div class="titlebar"><button class="close" aria-label="Collapse window"></button><span class="t" id="w{i+1}">{y}{" (current)" if cur else ""}</span><button class="shade" aria-label="Windowshade"></button></div>\n'
                f'      <div class="infobar"><span>{len(members)} items</span><span>icon view</span></div>\n'
                f'      <div class="wbody">\n      <div class="people">\n{cards(members)}\n      </div>\n      </div>\n    </section>\n\n')
    out += '    <footer id="strip"></footer>\n  </main>\n  <nav id="icons"></nav>\n</div>\n<script src="site.js"></script>\n</body>\n</html>\n'
    return out


CSS = {
    "windowed": """
/* committee portraits */
.people { display: grid; grid-template-columns: repeat(auto-fill, minmax(132px, 1fr)); gap: 20px 18px; }
.person-card { margin: 0; }
.person-card img { width: 100%; height: auto; aspect-ratio: 1; display: block; border: 2px solid var(--ink); background: #f8f8f8; }
.person-card figcaption { margin-top: 8px; line-height: 1.3; }
.person-card .role { display: block; font: 11px/1.3 var(--mono); text-transform: uppercase; letter-spacing: .04em; color: var(--muted); }
.person-card .who { display: block; font-weight: 700; font-size: 15px; }
""",
    "neon": """
/* committee portraits */
.people { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 16px; margin-top: 8px; }
.person-card { margin: 0; background: var(--white); border: 3px solid var(--ink); }
.person-card img { width: 100%; height: auto; aspect-ratio: 1; display: block; border-bottom: 3px solid var(--ink); }
.person-card figcaption { padding: 8px 10px 10px; line-height: 1.25; }
.person-card .role { display: block; font: 700 11px var(--mono); text-transform: uppercase; letter-spacing: .06em; }
.person-card .who { display: block; font: 400 15px/1.15 var(--head); text-transform: uppercase; margin-top: 3px; }
""",
    "classic": """
/* committee portraits: Finder icon view */
.people { display: grid; grid-template-columns: repeat(auto-fill, minmax(128px, 1fr)); gap: 18px 14px; }
.person-card { margin: 0; text-align: center; }
.person-card img { width: 112px; height: 112px; display: block; margin: 0 auto; border: 2px solid var(--black); box-shadow: 2px 2px 0 var(--black); filter: grayscale(1) contrast(1.05); }
.person-card figcaption { margin-top: 8px; }
.person-card .who { display: inline-block; font-size: 13px; padding: 0 4px; }
.person-card:hover .who { background: var(--black); color: var(--white); }
.person-card .role { display: block; font-size: 11px; color: #333; }
""",
}
CSS["flat"] = CSS["windowed"].replace("border: 2px solid var(--ink); background: #f8f8f8;", "border: 0; background: transparent;")


def main():
    for site in ("windowed", "flat", "neon", "classic"):
        html = page_neon() if site == "neon" else page_classic() if site == "classic" else page_windowed(site)
        open(os.path.join(ROOT, site, PAGE + ".html"), "w").write(html)
        css_path = os.path.join(ROOT, site, "style.css")
        css = open(css_path).read()
        if "/* committee portraits" not in css:
            open(css_path, "a").write(CSS[site])
    print("wrote 4 pages")


if __name__ == "__main__":
    main()
