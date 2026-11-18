// Entry point: hash router. Routes:
//   #/                      home
//   #/archive               archive (all saved/solved/solutions)
//   #/s/<subject>           subject (lecture grid)
//   #/s/<subject>/l/<n>     lecture
//   #/s/<subject>/search    search (?q=…&k=#Keyword)
//   #/s/<subject>/archive   archive for subject
import { h, scrollToTop } from './util.js';
import { homePage, subjectPage, lecturePage, searchPage, profilePage, notFoundPage } from './pages.js';

const app = document.getElementById('app');
const profileLink = document.querySelector('.profile-link');

function updateHeaderLink(currentSubject = 'toc') {
  if (profileLink) {
    profileLink.href = currentSubject ? `#/s/${currentSubject}/archive` : '#/archive';
  }
}

let token = 0;
let lastRoute = '';

function parseHash() {
  const raw = location.hash.replace(/^#/, '') || '/';
  const [path, query = ''] = raw.split('?');
  const parts = path.split('/').filter(Boolean).map((p) => {
    try { return decodeURIComponent(p); } catch (e) { return p; }
  });
  return { parts, params: new URLSearchParams(query) };
}

async function route() {
  const my = ++token;
  const { parts, params } = parseHash();
  const routeKey = parts.join('/');
  const sameRoute = routeKey === lastRoute;
  lastRoute = routeKey;

  const currentSubject = (parts[0] === 's' && parts[1]) ? parts[1] : 'toc';
  updateHeaderLink(currentSubject);

  try {
    if (parts.length === 0) await homePage(app);
    else if (parts[0] === 'archive' || parts[0] === 'profile') await profilePage(app, params.get('s') || 'toc', params);
    else if (parts[0] === 's' && parts.length === 2) await subjectPage(app, parts[1]);
    else if (parts[0] === 's' && parts[2] === 'l' && parts.length === 4) await lecturePage(app, parts[1], parts[3], params);
    else if (parts[0] === 's' && parts[2] === 'search' && parts.length === 3) await searchPage(app, parts[1], params);
    else if (parts[0] === 's' && (parts[2] === 'archive' || parts[2] === 'profile') && parts.length === 3) await profilePage(app, parts[1], params);
    else notFoundPage(app);
  } catch (e) {
    if (my !== token) return;
    console.error(e);
    showError(e);
  }
  if (my === token && !sameRoute) scrollToTop();
}

function showError(e) {
  const onFile = location.protocol === 'file:';
  app.replaceChildren(h('div', { class: 'empty-state' },
    h('h1', null, 'Something went wrong'),
    h('p', null, e && e.message ? e.message : String(e)),
    onFile
      ? h('p', null, 'This page was opened as a file. Browsers block loading the JSON data that way: start a local server instead (python -m http.server) and open http://localhost:8000.')
      : h('p', null, 'Check that the files in data/ exist and contain valid JSON (run python scripts/merge.py after editing per-year files).'),
    h('a', { class: 'btn primary', href: '#/' }, 'Back to home')));
}

// The skip link must not change the hash (that would be read as a route).
document.querySelector('.skip-link')?.addEventListener('click', (e) => { e.preventDefault(); app.focus(); });

window.addEventListener('hashchange', route);
route();

if (!window.marked || !window.katex) {
  console.warn('A CDN library (marked or KaTeX) did not load; questions will show as plain text. Check your internet connection.');
}
