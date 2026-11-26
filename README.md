# AoIR web mockups

Static HTML mockups for a redesigned aoir.org. No build step: open any `.html` file, or view them on GitHub Pages.

- `windowed/`: 1. Modern-retro cream windows floating on a solid backdrop.
- `flat/`: 2. The original modern-retro page: one cream column, no windows.
- `neon/`: 3. E-zine neon color blocks on white (black option).
- `classic/`: also explored. 1-bit Mac Classic / OS 9 windows on a solid color desktop.
- `index.html`: landing page linking all of them.

Each version has nine pages (home, about, news, conference, publications, membership, awards, ethics, login). The header, footer and color picker are injected by that folder's `site.js`, and all styling lives in its `style.css`.

Append `?bg=<hex>` to any page URL to preview a backdrop color, e.g. `classic/index.html?bg=0d97b0`.
