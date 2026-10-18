"""Small static blog builder. The website itself needs no Python or framework."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re
import shutil
from urllib.parse import quote, urlsplit
import xml.etree.ElementTree as ET

import markdown
from markdown.extensions.toc import slugify_unicode
import yaml

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
SITE = json.loads((ROOT / 'site.json').read_text())
BASE = SITE['url'].rstrip('/')
YEAR = datetime.now(timezone.utc).year


def template(name, **values):
    text = (ROOT / 'templates' / (name + '.html')).read_text()
    for key, value in values.items():
        text = text.replace('{{' + key + '}}', str(value))
    unresolved = re.findall(r'\{\{\w+\}\}', text)
    if unresolved:
        raise ValueError(f'Unresolved template variables in {name}: {unresolved}')
    return text


def url(path):
    return quote(path, safe='/#?=&%')


def tag_url(tag):
    return '/tags/' + quote(tag, safe='') + '/'


def plain(html):
    from html import unescape
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', html))).strip()


def write(path, text):
    target = OUT / path.lstrip('/')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')


def page(route, title, content, active='', description='', extra_head='', og_type='website'):
    description = description or SITE['description']
    html = template('layout', title=escape(title), description=escape(description, quote=True),
                    canonical=escape(BASE + url(route), quote=True), year=YEAR, content=content,
                    home_active='aria-current="page"' if active == 'home' else '',
                    posts_active='aria-current="page"' if active == 'posts' else '',
                    about_active='aria-current="page"' if active == 'about' else '',
                    github=escape(SITE['github']), extra_head=extra_head, og_type=og_type)
    write(route + 'index.html' if route.endswith('/') else route, html)


def redirect(route, target):
    write(route.rstrip('/') + '/index.html', '<!doctype html><html lang="zh-CN"><meta charset="utf-8">'
          f'<meta http-equiv="refresh" content="0;url={escape(target, quote=True)}">'
          f'<link rel="canonical" href="{BASE}{target}"><title>页面已迁移 · 右郁石</title>'
          f'<p>页面已迁移，<a href="{escape(target, quote=True)}">继续阅读</a>。</p></html>')


def post_row(post, number):
    return (f'<li><a class="writing-row" href="{url(post["url"])}">'
            f'<span class="row-number">{number:02d}</span><span class="row-content">'
            f'<h3>{escape(post["title"])}</h3><p>{escape(post["excerpt"])}</p></span>'
            f'<time datetime="{post["date"]}">{post["date"][:7].replace("-", " / ")}</time>'
            '<span class="row-arrow" aria-hidden="true">↗</span></a></li>')


if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'assets', OUT / 'assets')
write('/.nojekyll', '')

posts = []
for source in sorted((ROOT / 'content' / 'posts').glob('*.md')):
    raw = source.read_text(encoding='utf-8')
    _, header, body = raw.split('---', 2)
    post = yaml.safe_load(header)
    post['date'] = str(post['date'])[:10]
    # Reject route traversal and duplicates before writing any article.
    route = post['url']
    if not re.fullmatch(r'/\d{4}/\d{2}/\d{2}/[^/]+/', route) or '..' in Path(route).parts:
        raise ValueError(f'Invalid post URL: {route}')
    md = markdown.Markdown(extensions=['fenced_code', 'tables', 'toc', 'sane_lists'],
                           extension_configs={'toc': {'permalink': False, 'slugify': slugify_unicode}})
    post['html'] = md.convert(body.strip())
    post['toc'] = md.toc.replace('class="toc"', 'class="toc-list"') if md.toc_tokens else '<p class="muted">这是一篇短记。</p>'
    post['plain'] = plain(post['html'])
    post['excerpt'] = re.sub(r'\$[^$]+\$', '〔公式〕', post['plain'])[:115]
    if len(post['plain']) > 115:
        post['excerpt'] += '…'
    post['minutes'] = max(1, round(len(post['plain']) / 400))
    post['topics'] = list(dict.fromkeys(post.get('tags', []) + post.get('categories', [])))
    posts.append(post)
posts.sort(key=lambda p: (p['date'], p['url']), reverse=True)
assert len({p['url'] for p in posts}) == len(posts), 'Duplicate post URLs'
counts = Counter(tag for p in posts for tag in p['topics'])
topic_order = sorted(counts, key=lambda t: (-counts[t], t))

# Empty and test entries stay in the full archive, while the homepage highlights reading.
selected = [p for p in posts if p['plain'] and p['title'] not in {'test', 'test1'}]
latest = selected[0]
featured = (f'<a class="featured-link" href="{url(latest["url"])}">'
            f'<div class="featured-meta"><span class="blue-dot"></span><time datetime="{latest["date"]}">{latest["date"].replace("-", " / ")}</time><span>{latest["minutes"]} 分钟阅读</span></div>'
            f'<div class="featured-body"><div><p class="eyebrow">{escape(" / ".join(latest["topics"]) or "学习笔记")}</p><h3>{escape(latest["title"])}</h3><p>{escape(latest["excerpt"])}</p></div><span class="featured-arrow" aria-hidden="true">↗</span></div>'
            '<span class="featured-read">继续阅读 <span aria-hidden="true">→</span></span></a>')
topics_html = ''.join(f'<a class="topic" href="{tag_url(tag)}"><span>{escape(tag)}</span><span class="topic-count">{counts[tag]:02d} <span aria-hidden="true">↗</span></span></a>' for tag in topic_order)
page('/', SITE['title'] + ' · 记录编程、学习与日常',
     template('home', featured=featured, post_count=len(posts),
              recent=''.join(post_row(p, i + 1) for i, p in enumerate(selected[1:6])),
              topics=topics_html, github=SITE['github'], csdn=SITE['csdn']), active='home')


def archive(route, heading, intro, subset, current=None):
    filters = '<a class="filter' + (' selected' if current is None else '') + '" href="/posts/">全部</a>'
    filters += ''.join(f'<a class="filter{" selected" if tag == current else ""}" href="{tag_url(tag)}"' + (' aria-current="page"' if tag == current else '') + f'>{escape(tag)}</a>' for tag in topic_order)
    years = defaultdict(list)
    for post in subset:
        years[post['date'][:4]].append(post)
    content = ''.join(f'<section class="archive-year" aria-labelledby="year-{year}"><h2 id="year-{year}">{year}<sup>{len(items):02d}</sup></h2><ol class="writing-list">' + ''.join(post_row(p, i + 1) for i, p in enumerate(items)) + '</ol></section>' for year, items in years.items())
    page(route, heading + ' · 右郁石', template('archive', heading=escape(heading), intro=intro,
         filters=filters, count=len(subset), archive=content), active='posts')


archive('/posts/', '写下的，留下的', '关于编程、学习，也关于生活。按时间慢慢读。', posts)
for tag in topic_order:
    archive('/tags/' + tag + '/', tag, '循着一个话题，把零散的思考连起来。',
            [p for p in posts if tag in p['topics']], current=tag)
page('/tags/', '话题 · 右郁石', '<section class="page-heading"><p class="eyebrow">FOLLOW A THREAD</p><h1>循着话题<span class="brand-dot">.</span></h1><p>从一个感兴趣的词，走进这些年的记录。</p></section><div class="topic-grid all-topics">' + topics_html + '</div>', active='posts')
page('/about/', '关于 · 右郁石', template('about', github=SITE['github'], csdn=SITE['csdn']), active='about')

for i, post in enumerate(posts):
    tag_links = ''.join(f'<a href="{tag_url(t)}">{escape(t)}</a>' for t in post['topics'])
    older = posts[i + 1] if i + 1 < len(posts) else None
    newer = posts[i - 1] if i else None
    previous = f'<a href="{url(older["url"])}"><small>← 上一篇</small><span>{escape(older["title"])}</span></a>' if older else '<span></span>'
    following = f'<a href="{url(newer["url"])}"><small>下一篇 →</small><span>{escape(newer["title"])}</span></a>' if newer else '<span></span>'
    math_head = ''
    if '$' in post['plain']:
        math_head = '<script>window.MathJax={tex:{inlineMath:[["$","$"],["\\\\(","\\\\)"]]},options:{skipHtmlTags:["script","noscript","style","textarea","pre","code"]}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script>'
    page(post['url'], post['title'] + ' · 右郁石', template('post',
         date=post['date'], display_date=post['date'].replace('-', ' / '), minutes=post['minutes'],
         post_title=escape(post['title']), category='', tags=tag_links, toc=post['toc'],
         body=post['html'] or '<p class="empty-note">这是一篇尚未写下正文的旧日记录。</p>',
         previous=previous, next=following), active='posts',
         description=post['excerpt'] or post['title'], extra_head=math_head, og_type='article')

# Existing archive/category URLs keep working after migration.
redirect('/archives/', '/posts/')
for year in {p['date'][:4] for p in posts}:
    redirect('/archives/' + year + '/', '/posts/#year-' + year)
for month in {p['date'][:7].replace('-', '/') for p in posts}:
    redirect('/archives/' + month + '/', '/posts/#year-' + month[:4])
for tag in topic_order:
    redirect('/categories/' + tag + '/', tag_url(tag))
redirect('/categories/', '/tags/')
for n in (2, 3):
    redirect(f'/page/{n}/', '/posts/')
redirect('/feeds/', '/atom.xml')
redirect('/home/', '/')
page('/404.html', '页面未找到 · 右郁石', '<section class="page-heading not-found"><p class="eyebrow">404 / A LITTLE DETOUR</p><h1>走到了一处空白。</h1><p>这页可能已经搬走，去文章里找找吧。</p><a class="solid-link" href="/posts/">浏览所有文章 ↗</a></section>')

# Search stays local to the browser; no service, API key, or tracking.
write('/search.json', json.dumps([{'title': p['title'], 'url': url(p['url']), 'date': p['date'],
      'tags': p['topics'], 'excerpt': p['excerpt'], 'text': p['plain']} for p in posts], ensure_ascii=False))

atom = 'http://www.w3.org/2005/Atom'
ET.register_namespace('', atom)
feed = ET.Element('{' + atom + '}feed')
def add(parent, tag, value):
    element = ET.SubElement(parent, '{' + atom + '}' + tag)
    element.text = value
    return element
add(feed, 'title', SITE['title'])
add(feed, 'id', BASE + '/')
add(feed, 'updated', posts[0]['date'] + 'T00:00:00Z')
ET.SubElement(feed, '{' + atom + '}link', {'href': BASE + '/atom.xml', 'rel': 'self'})
for post in posts:
    entry = ET.SubElement(feed, '{' + atom + '}entry')
    add(entry, 'title', post['title'])
    add(entry, 'id', BASE + url(post['url']))
    ET.SubElement(entry, '{' + atom + '}link', {'href': BASE + url(post['url'])})
    add(entry, 'updated', post['date'] + 'T00:00:00Z')
    add(entry, 'author', '')
    add(entry[-1], 'name', SITE['author'])
    add(entry, 'summary', post['excerpt'])
write('/atom.xml', '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(feed, encoding='unicode'))
routes = ['/', '/posts/', '/tags/', '/about/'] + [p['url'] for p in posts] + ['/tags/' + t + '/' for t in topic_order]
sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for route in routes:
    node = ET.SubElement(sitemap, 'url')
    ET.SubElement(node, 'loc').text = BASE + url(route)
write('/sitemap.xml', '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(sitemap, encoding='unicode'))
write('/robots.txt', 'User-agent: *\nAllow: /\nSitemap: ' + BASE + '/sitemap.xml\n')
print(f'Built {len(posts)} articles, {len(topic_order)} topics → {OUT}')
