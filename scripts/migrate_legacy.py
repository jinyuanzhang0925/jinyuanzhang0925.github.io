"""One-time import from the published master branch, not the stale Hexo source.

Usage: python scripts/migrate_legacy.py /path/to/extracted/master
Requires: beautifulsoup4==4.15.0 markdownify==1.2.3 PyYAML==6.0.3
"""
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from markdownify import markdownify
import yaml

ROOT = Path(__file__).resolve().parents[1]
source = Path(sys.argv[1])
destination = ROOT / 'content' / 'posts'
destination.mkdir(parents=True, exist_ok=True)
report = []
for path in sorted(source.glob('20*/**/index.html')):
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    article = soup.select_one('#article-container')
    if article is None:
        continue
    route = '/' + path.parent.relative_to(source).as_posix() + '/'
    title = soup.select_one('h1').get_text(' ', strip=True)
    date = soup.select_one('time')['datetime'][:10]
    tags = list(dict.fromkeys(
        unquote(urlsplit(a['href']).path).strip('/').split('/')[1]
        for a in soup.select('a[href^="/tags/"]')
        if len(urlsplit(a['href']).path.strip('/').split('/')) > 1
    ))
    categories = [a.get_text(strip=True) for a in soup.select('#post-meta a.post-meta-categories')]
    if not categories:
        categories = list(dict.fromkeys(a.get_text(strip=True) for a in soup.select('.post-meta a[href^="/categories/"]')))
    for a in article.select('a.headerlink'):
        a.decompose()
    code_blocks = []
    for figure in article.select('figure.highlight'):
        lines = figure.select('td.code .line')
        code = '\n'.join(line.get_text() for line in lines)
        if not lines:
            block = figure.select_one('td.code pre')
            code = block.get_text() if block else figure.get_text()
        language = next((x for x in figure.get('class', []) if x != 'highlight'), '')
        language = language if language != 'plaintext' else ''
        fence = '`' * max(3, max((len(x) + 1 for x in re.findall(r'`+', code)), default=3))
        code_blocks.append(fence + language + '\n' + code + '\n' + fence)
        placeholder = soup.new_tag('p')
        placeholder.string = f'MIGRATIONCODEBLOCK{len(code_blocks) - 1:04d}'
        figure.replace_with(placeholder)
    missing_images = []
    for image in article.select('img'):
        url = image.get('src', '')
        if '\\' in url:
            missing_images.append(url)
            note = soup.new_tag('p')
            note.string = '〔原文配图在旧站中已缺失〕'
            image.replace_with(note)
    for a in article.select('a[href]'):
        url = a['href']
        # Repair malformed legacy links where the real URL was put in title/quotes.
        if url == 'link' and a.get('title', '').startswith(('https://', 'http://')):
            url = a['title']
            a['href'] = url
            del a['title']
        if url.startswith('%22https://') and url.endswith('%22'):
            url = url[3:-3]
            a['href'] = url
        if url.startswith(('http://zhangjinyuan.top/', 'https://zhangjinyuan.top/')):
            parts = urlsplit(url)
            a['href'] = parts.path + ('#' + parts.fragment if parts.fragment else '')
    body = markdownify(str(article), heading_style='ATX', bullets='-',
                       escape_underscores=False, escape_asterisks=False,
                       code_language_callback=lambda el: next((x.removeprefix('language-') for x in el.select_one('code').get('class', []) if x.startswith('language-')), '') if el.select_one('code') else '')
    # Root-level fences are portable across Markdown renderers, including code
    # originally nested inside ordered lists in the legacy HTML.
    body = re.sub(r'(?m)^[ \t]*MIGRATIONCODEBLOCK(\d+)[ \t]*$',
                  lambda match: '\n\n' + code_blocks[int(match[1])] + '\n\n', body)
    body = re.sub(r'\n{3,}', '\n\n', body).strip() + '\n'
    metadata = {'title': title, 'date': date, 'url': route, 'tags': tags, 'categories': categories}
    filename = date + '-' + path.parent.name + '.md'
    (destination / filename).write_text('---\n' + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + '---\n\n' + body, encoding='utf-8')
    report.append({'title': title, 'url': route, 'file': 'content/posts/' + filename,
                   'published_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                   'empty_in_original': not bool(article.get_text(strip=True)),
                   'missing_images_in_original': missing_images})
(ROOT / 'migration-manifest.json').write_text(json.dumps({
    'source': 'https://github.com/Jeremy-zjy/Jeremy-zjy.github.io/tree/master',
    'original_source_branch': 'hexo', 'published_posts': len(report), 'posts': report,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Imported {len(report)} published articles with original URLs.')
