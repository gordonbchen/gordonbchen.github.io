# Unjustified conclusions

A static blog. One small Python builder, one stylesheet, one search script. No theme, framework, database, or server at runtime.

## Preview locally

Requires Python 3.10 or newer.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/preview.py
```

Open http://localhost:8000. The preview script builds once, then automatically rebuilds when you save source files (including posts, CSS, images, and settings). Refresh the browser to see changes; browser refresh is manual. Stop with Ctrl+C.

After the initial setup, just run `.venv/bin/python scripts/preview.py` (or `python3 scripts/preview.py` if Markdown is already installed). If port 8000 is busy, use `--port 8001`.

For a one-time build without starting a server: `python3 scripts/build.py`.

## Add a post

Create `math/my-post.md`, or `math/my-post/index.md` with images next to it:

```markdown
---
title: My post
date: 2026-11-23
---

Write Markdown here. Inline math: $x^2$. Display math: $$x^2 + y^2 = 1$$.

![A diagram](diagram.png)
```

Use the folder form for images. For a standalone `.md` file, put attachments next to that file. Filenames and folder names become URLs; prefer lowercase names with hyphens. `index.md` represents its containing folder. Front matter supports simple, single-line `title`, `date` (YYYY-MM-DD), and `draft: true` fields. A date is recommended; if omitted, the file's modification date is used. Titles default to the filename.

Top-level content folders become topics automatically. For example, `physics/notes.md` creates `/physics/` and `/physics/notes/`. Nested folders get topic pages too. A folder with `index.md` is a post, so do not also put other posts inside that folder. Reserved folders: `assets`, `static`, `scripts`, `vendor`, `node_modules`, and names starting with `.` or `_`.

Posts are listed newest first. Search matches path and title; `math/` finds all math posts. Press `/` to open search.

## Tweak the site

- `site.json`: name, description, contact links, number of recent posts.
- `static/style.css`: colors, typography, width, spacing.
- `scripts/build.py`: HTML templates and content discovery.
- `static/search.js`: browser search.
- `assets/images/tao.svg`: favicon.

Markdown is the only Python dependency. MathJax loads from a CDN on posts containing math. Everything else is served from the static build. Existing post URLs and attachment paths are preserved.

## Where to change the appearance

Edit `static/style.css`; the rules are formatted separately so you can search for the selector:

| Setting | Location |
| --- | --- |
| Background and text colors | `:root` → `--bg`, `--text`, `--muted`, `--line` |
| Main font and body text size | `body` → `font` |
| Header title weight and size | `.brand` → `font-weight` (`400` is regular), `font-size` |
| Content width | `.shell` → `max-width` |
| Small-screen adjustments | `@media(max-width:560px)` at the end |
| Site name and contact links | `site.json` |
| Breadcrumb root label (`home`) | `breadcrumbs()` in `scripts/build.py` |
| Header HTML | `page()` in `scripts/build.py` |


With `scripts/preview.py` running, save your edit and refresh the local preview; rebuilding is automatic. Otherwise, run `python3 scripts/build.py` first. Hard-refresh (Ctrl+Shift+R) if the browser caches the old CSS.

## GitHub Pages

The included workflow builds `_site/` and deploys it when you push to `main` or `master`. In the repository's **Settings → Pages → Build and deployment**, select **GitHub Actions**. No Jekyll setup is required. The generated `_site/` folder is ignored by Git.

This site assumes it is hosted at the domain root, as it is for `gordonbchen.github.io`.

## Bundled font

Computer Modern Serif is served locally from `assets/fonts/`, with regular, italic, bold, and bold-italic faces. Source: https://github.com/dreampulse/computer-modern-web-font. Its license is in `assets/fonts/COMPUTER-MODERN-OFL.txt`.

Change `--font` in `static/style.css` to change the font across the site. The `@font-face` rules at the top load the font files. Embedded PDFs keep their own fonts; equations use MathJax’s mathematical glyphs.
