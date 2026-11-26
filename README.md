# AoIR web mockups

Static HTML mockups for a redesigned aoir.org. No build step: open any `.html` file, or view them on GitHub Pages.

- `windowed/`: Direction A. Modern-retro cream windows floating on a solid backdrop.
- `classic/`: Direction B. 1-bit Mac Classic / OS 9 windows on a solid color desktop.
- `index.html`: landing page linking both.

Each direction has nine pages (home, about, news, conference, publications, membership, awards, ethics, login). The header, footer and color picker are injected by that folder's `site.js`, and all styling lives in its `style.css`.

Append `?bg=<hex>` to any page URL to preview a backdrop color, e.g. `classic/index.html?bg=0d97b0`.
