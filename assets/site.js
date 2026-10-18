/* Progressive enhancement only. Articles and navigation work without JavaScript. */
(() => {
  const themeButton = document.querySelector('.theme-toggle');
  function syncThemeButton() {
    const dark = document.documentElement.dataset.theme === 'dark';
    themeButton.setAttribute('aria-pressed', String(dark));
    themeButton.setAttribute('aria-label', dark ? '切换浅色模式' : '切换深色模式');
  }
  syncThemeButton();
  themeButton.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('theme', theme); } catch (_) {}
    syncThemeButton();
  });

  const dialog = document.querySelector('.search-dialog');
  const input = document.querySelector('#search-input');
  const results = document.querySelector('#search-results');
  const status = document.querySelector('#search-status');
  let index;
  let indexPromise;
  async function loadIndex() {
    if (index) return index;
    if (!indexPromise) {
      indexPromise = fetch('/search.json').then(response => {
        if (!response.ok) throw new Error('Search index unavailable');
        return response.json();
      }).then(data => { index = data; return data; }).catch(error => {
        indexPromise = null;
        throw error;
      });
    }
    return indexPromise;
  }
  async function search() {
    const query = input.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    if (!query) { status.textContent = '搜索这些年写下的文字。'; return; }
    status.textContent = '正在查找…';
    try {
      const posts = await loadIndex();
      if (query !== input.value.trim().toLocaleLowerCase()) return;
      const words = query.split(/\s+/);
      const hits = posts.filter(post => {
        const haystack = [post.title, ...post.tags, post.text].join(' ').toLocaleLowerCase();
        return words.every(word => haystack.includes(word));
      });
      status.textContent = hits.length ? `找到 ${hits.length} 篇文章` : '没有找到相关记录。试试“Java”“算法”或“随笔”。';
      for (const post of hits) {
        const link = document.createElement('a');
        link.href = post.url;
        const title = document.createElement('h3');
        title.textContent = post.title;
        const time = document.createElement('time');
        time.dateTime = post.date;
        time.textContent = post.date;
        const excerpt = document.createElement('p');
        excerpt.textContent = post.excerpt;
        link.append(time, title, excerpt);
        results.append(link);
      }
    } catch (_) {
      status.textContent = '暂时无法加载搜索，请稍后重试。也可以前往文章归档浏览。';
    }
  }
  function openSearch() {
    if (!dialog.open) dialog.showModal();
    input.focus();
  }
  document.querySelector('.search-trigger').addEventListener('click', openSearch);
  document.querySelector('.close-search').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  }});
  document.addEventListener('keydown', event => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault(); openSearch();
    }
  });
  input.addEventListener('input', search);

  const progress = document.querySelector('.reading-progress');
  if (progress) {
    let ticking = false;
    function updateProgress() {
      const total = document.documentElement.scrollHeight - innerHeight;
      progress.style.width = (total > 0 ? Math.min(100, scrollY / total * 100) : 0) + '%';
      ticking = false;
    }
    addEventListener('scroll', () => {
      if (!ticking) { requestAnimationFrame(updateProgress); ticking = true; }
    }, { passive: true });
    addEventListener('resize', updateProgress);
    updateProgress();
  }
})();
