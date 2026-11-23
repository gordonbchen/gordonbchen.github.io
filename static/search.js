// No framework: search the static index using paths and titles.
document.addEventListener('keydown', event => {
  if (event.key === '/' && !event.metaKey && !event.ctrlKey && !event.altKey && !event.target.matches('input, textarea, [contenteditable]')) {
    event.preventDefault();
    if (document.querySelector('#search')) document.querySelector('#search').focus();
    else location.href = '/search/';
  }
});
(async () => {
  const input = document.querySelector('#search');
  if (!input) return;
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#search-results');
  status.textContent = 'Loading posts…';
  try {
    const response = await fetch('/search.json');
    if (!response.ok) throw new Error('Index unavailable');
    const posts = await response.json();
    input.value = new URLSearchParams(location.search).get('q') || '';
    function render() {
      const query = input.value.trim().toLowerCase().replace(/^\/+/, '');
      const terms = query.split(/\s+/).filter(Boolean);
      const matches = posts.filter(post => terms.every(term => `${post.path} ${post.title}`.toLowerCase().includes(term)));
      results.replaceChildren();
      const list = document.createElement('ul');
      list.className = 'posts';
      for (const post of matches) {
        const row = document.createElement('li');
        const link = document.createElement('a');
        link.href = post.url;
        for (const [className, value] of [['post-title', post.title], ['path', post.path]]) {
          const span = document.createElement('span');
          span.className = className;
          span.textContent = value;
          link.append(span);
        }
        const date = document.createElement('time');
        date.dateTime = post.date;
        date.textContent = post.date;
        row.append(link, date);
        list.append(row);
      }
      results.append(list);
      status.textContent = matches.length ? `${matches.length} ${matches.length === 1 ? 'post' : 'posts'}` : 'No posts match this path or title.';
      const url = new URL(location.href);
      if (input.value) url.searchParams.set('q', input.value);
      else url.searchParams.delete('q');
      history.replaceState(null, '', url);
    }
    input.addEventListener('input', render);
    render();
    input.focus();
  } catch {
    status.textContent = 'Search could not load. Please reload or browse topics from the homepage.';
  }
})();
