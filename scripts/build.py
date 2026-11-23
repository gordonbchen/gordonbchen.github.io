"""Build a static site: python3 scripts/build.py. Content lives in top-level folders."""
from pathlib import Path
from datetime import date
import html
import json
import re
import shutil
import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '_site'
CONFIG = json.loads((ROOT / 'site.json').read_text())
EXCLUDED = {'scripts', 'static', 'assets', 'vendor', 'node_modules'}
esc = lambda value: html.escape(str(value), quote=True)


def page(title, body, math=False):
    math_scripts = r'''<script>window.MathJax={tex:{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['$$','$$'],['\\[','\\]']]}};</script><script async src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>''' if math else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {esc(CONFIG['title'])}</title><meta name="description" content="{esc(CONFIG['description'])}">
<link rel="icon" type="image/svg+xml" href="/assets/images/tao.svg"><link rel="stylesheet" href="/static/style.css">
<script src="/static/search.js" defer></script>{math_scripts}</head>
<body><a class="skip" href="#main">Skip to content</a><div class="shell">
<header><a class="brand" href="/"><img src="/assets/images/tao.svg" width="32" height="32" alt=""><span>{esc(CONFIG['title'])}</span></a>
<nav aria-label="Main"><a href="/about/">About</a><a href="/search/">Search <span class="key" aria-hidden="true">/</span></a></nav></header>
<main id="main">{body}</main></div></body></html>'''


def write(url, content):
    target = OUT / url.strip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def rows(posts):
    return '<ul class="posts">' + ''.join(f'<li><a href="{p["url"]}"><span class="post-title">{esc(p["title"])}</span><span class="path">{esc(p["path"])}</span></a><time datetime="{p["date"]}">{p["date"]}</time></li>' for p in posts) + '</ul>'


def breadcrumbs(path):
    parts = path.split('/') if path else []
    links = ['<a href="/">home</a>']
    for i, part in enumerate(parts):
        url = '/' + '/'.join(parts[:i + 1]) + '/'
        links.append(f'<a href="{esc(url)}">{esc(part)}</a>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(links) + '</nav>'


def directory_rows(directories, posts, parent=''):
    children = [d for d in directories if d.rpartition('/')[0] == parent]
    if not children:
        return ''
    rows = []
    for child in children:
        count = sum(p['path'].startswith(child + '/') for p in posts)
        label = child.rsplit('/', 1)[-1]
        rows.append(f'<li><a href="/{esc(child)}/"><span>{esc(label)}/</span><span class="count">{count} {"post" if count == 1 else "posts"}</span></a></li>')
    return '<section><h2>' + ('Subtopics' if parent else 'Topics') + '</h2><ul class="directories">' + ''.join(rows) + '</ul></section>'


def icon(name):
    paths = {
        'Email': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
        'GitHub': '<path d="M9 19c-4.3 1.3-4.3-2.2-6-2.7m12 5v-3.4a3 3 0 0 0-.8-2.3c2.7-.3 5.5-1.3 5.5-6A4.7 4.7 0 0 0 18.4 6a4.3 4.3 0 0 0-.1-3.5s-1-.3-3.6 1.3a12.3 12.3 0 0 0-6.5 0C5.7 2.2 4.6 2.5 4.6 2.5A4.3 4.3 0 0 0 4.5 6a4.7 4.7 0 0 0-1.3 3.3c0 4.7 2.8 5.7 5.5 6a3 3 0 0 0-.8 2.3v3.7"/>',
        'Twitter': '<path d="M22 5.8a8.3 8.3 0 0 1-2.4.7 4.2 4.2 0 0 0 1.8-2.3 8.3 8.3 0 0 1-2.6 1 4.2 4.2 0 0 0-7.2 3.8 11.8 11.8 0 0 1-8.6-4.4 4.2 4.2 0 0 0 1.3 5.6 4.2 4.2 0 0 1-1.9-.5c0 2 1.4 3.7 3.3 4.1a4.2 4.2 0 0 1-1.9.1 4.2 4.2 0 0 0 3.9 2.9A8.4 8.4 0 0 1 2 18.5a11.8 11.8 0 0 0 18.2-10 8.5 8.5 0 0 0 1.8-2.7Z"/>',
    }
    return '<svg class="contact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths[name] + '</svg>'


def build():
    # Only generated output is replaced; source posts and assets stay untouched.
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    posts = []
    for folder in sorted(ROOT.iterdir()):
        if not folder.is_dir() or folder.name.startswith(('.', '_')) or folder.name in EXCLUDED:
            continue
        for source in sorted(folder.rglob('*.md')):
            raw = source.read_text()
            meta = {}
            if raw.startswith('---\n'):
                front, raw = raw[4:].split('\n---', 1)
                for line in front.splitlines():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        meta[key.strip()] = value.strip().strip('"\'')
            # Old hand-written directory listings are replaced by generated topic pages.
            if meta.get('layout') == 'page' or meta.get('draft') == 'true':
                continue
            relative = source.relative_to(ROOT)
            path = relative.parent if source.stem == 'index' else relative.with_suffix('')
            url = '/' + path.as_posix() + '/'
            post_date = meta.get('date', date.fromtimestamp(source.stat().st_mtime).isoformat())
            date.fromisoformat(post_date)
            title = meta.get('title', source.stem.replace('-', ' ').replace('_', ' ').capitalize())
            posts.append(dict(title=title, date=post_date, path=path.as_posix(), url=url, source=source, body=raw))
        # Copy local images, PDFs and other attachments alongside their posts.
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.pdf', '.avif', '.mp4'}:
                target = OUT / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
    posts.sort(key=lambda p: (p['date'], p['path']), reverse=True)
    directories = sorted({ '/'.join(p['path'].split('/')[:i]) for p in posts for i in range(1, len(p['path'].split('/'))) })
    write('/', page('Posts', directory_rows(directories, posts) + f'<section><h2>Recent posts</h2>{rows(posts[:CONFIG["recent_posts"]])}</section>'))
    urls = {p['url'] for p in posts}
    for directory in directories:
        url = '/' + directory + '/'
        if url in urls:
            raise ValueError(f'Post conflicts with topic: {directory}')
        selected = [p for p in posts if p['path'].startswith(directory + '/')]
        write(url, page(directory + '/', breadcrumbs(directory.rpartition('/')[0]) + f'<h1 class="directory-title">{esc(directory)}/</h1>' + directory_rows(directories, posts, directory) + f'<section><h2>Posts</h2>{rows(selected)}</section>'))
    for post in posts:
        # Protect TeX from Markdown's backslash and underscore handling.
        equations = []
        def protect(match):
            equations.append(match.group())
            return f'MATHPLACEHOLDER{len(equations)-1}END'
        body = re.sub(r'\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)[^\n$]+?\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)', protect, post['body'])
        body = markdown.markdown(body, extensions=['fenced_code', 'tables', 'md_in_html'])
        for i, equation in enumerate(equations):
            body = body.replace(f'MATHPLACEHOLDER{i}END', esc(equation))
        # Relative attachments for a standalone topic/post.md live one level up.
        if post['source'].stem != 'index':
            body = re.sub(r'(src|href)="(?![a-z]+:|/|#)([^"]+)"', r'\1="../\2"', body)
        parent = post['path'].rsplit('/', 1)[0]
        write(post['url'], page(post['title'], breadcrumbs(parent) + f'<article><div class="post-heading"><h1>{esc(post["title"])}</h1><time datetime="{post["date"]}">{post["date"]}</time></div><div class="prose">{body}</div></article>', math='$' in post['body'] or '\\[' in post['body']))
    write('/about/', page('About', f'<h1>About</h1><p>{esc(CONFIG["description"])}</p><ul class="contacts"><li><span>{icon('Email')}Email</span><a href="mailto:{esc(CONFIG["email"])}">{esc(CONFIG["email"])}</a></li><li><span>{icon('GitHub')}GitHub</span><a href="{esc(CONFIG["github"])}">{esc(CONFIG["github"].split("/")[-1])}</a></li><li><span>{icon('Twitter')}Twitter</span><a href="{esc(CONFIG["twitter"])}">@{esc(CONFIG["twitter"].split("/")[-1])}</a></li></ul>'))
    write('/search/', page('Search', '<h1>Search</h1><label for="search">Find a post by path or title</label><input id="search" type="search" placeholder="math/" autocomplete="off" spellcheck="false"><p id="search-status" class="muted" aria-live="polite"></p><div id="search-results"></div><noscript>Search needs JavaScript. You can browse all posts from the <a href="/">homepage</a>.</noscript>'))
    (OUT / 'search.json').write_text(json.dumps([{k:p[k] for k in ('title', 'date', 'path', 'url')} for p in posts]))
    (OUT / '404.html').write_text(page('404 · Page not found', breadcrumbs('') + '<h1>404</h1><div class="prose"><p class="muted">This page could not be found.</p><p><a href="/">Browse topics</a> or <a href="/search/">search for a post</a>.</p></div>'))
    shutil.copytree(ROOT / 'static', OUT / 'static')
    shutil.copytree(ROOT / 'assets', OUT / 'assets')
    (OUT / '.nojekyll').touch()
    print(f'Built {len(posts)} posts and {len(directories)} topic pages in {OUT}')


if __name__ == '__main__':
    build()
