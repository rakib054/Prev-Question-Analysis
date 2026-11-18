// Entry point: clean path router (HTML5 History API). Routes:
//   /home                   home
//   /archive                archive (all saved/solved/solutions)
//   /<subject>              subject (e.g. /toc)
//   /<subject>/lec_<n>      lecture (e.g. /toc/lec_01, /toc/lec_05)
//   /<subject>/search       search (e.g. /toc/search?q=…&k=#Keyword)
//   /<subject>/archive      archive for subject (e.g. /toc/archive)
import { h, scrollToTop } from './util.js';
import { homePage, subjectPage, lecturePage, searchPage, profilePage, notFoundPage } from './pages.js';

const app = document.getElementById('app');
const profileLink = document.querySelector('.profile-link');

function updateHeaderLink(currentSubject = 'toc') {
  if (profileLink) {
    profileLink.href = currentSubject ? `/${currentSubject}/archive` : '/archive';
  }
}

let token = 0;
let lastRoute = '';

function parsePath() {
  // If user arrives with a legacy hash route (e.g. #/s/toc/l/1), migrate to clean path
  if (location.hash && location.hash.startsWith('#/')) {
    const legacy = location.hash.replace(/^#\/?/, '');
    location.hash = '';
    history.replaceState(null, '', '/' + legacy);
  }

  const raw = (location.pathname || '/').replace(/^\/+|\/+$/g, '');
  const parts = raw.split('/').filter(Boolean).map((p) => {
    try { return decodeURIComponent(p); } catch (e) { return p; }
  });
  const params = new URLSearchParams(location.search);
  return { parts, params };
}

async function route() {
  const my = ++token;
  const { parts, params } = parsePath();
  const routeKey = parts.join('/') + '?' + params.toString();
  const sameRoute = routeKey === lastRoute;
  lastRoute = routeKey;

  // Derive current subject for the header archive link
  let currentSubject = 'toc';
  if (parts.length > 0 && parts[0] !== 'home' && parts[0] !== 'archive') {
    currentSubject = parts[0] === 's' && parts[1] ? parts[1] : parts[0];
  }
  updateHeaderLink(currentSubject);

  try {
    // 1. / or /home -> Home Page
    if (parts.length === 0 || parts[0] === 'home') {
      await homePage(app);
    }
    // 2. /archive -> Global Archive Page
    else if (parts.length === 1 && (parts[0] === 'archive' || parts[0] === 'profile')) {
      await profilePage(app, params.get('s') || 'toc', params);
    }
    // 3. /:subject (e.g. /toc) -> Subject Page
    else if (parts.length === 1 && parts[0] !== 's') {
      await subjectPage(app, parts[0]);
    }
    // 4. /:subject/lec_:num (e.g. /toc/lec_01, /toc/lec_05) or /:subject/:num -> Lecture Page
    else if (parts.length === 2 && /^lec_0*(\d+)$/i.test(parts[1])) {
      const match = parts[1].match(/^lec_0*(\d+)$/i);
      await lecturePage(app, parts[0], match[1], params);
    }
    else if (parts.length === 2 && /^\d+$/.test(parts[1])) {
      await lecturePage(app, parts[0], parts[1], params);
    }
    // 5. /:subject/search -> Search Page
    else if (parts.length === 2 && parts[1] === 'search') {
      await searchPage(app, parts[0], params);
    }
    // 6. /:subject/archive -> Subject Archive Page
    else if (parts.length === 2 && (parts[1] === 'archive' || parts[1] === 'profile')) {
      await profilePage(app, parts[0], params);
    }
    // Legacy routes support: /s/:subject, /s/:subject/l/:num, /s/:subject/search, /s/:subject/archive
    else if (parts[0] === 's' && parts.length === 2) {
      await subjectPage(app, parts[1]);
    }
    else if (parts[0] === 's' && parts[2] === 'l' && parts.length === 4) {
      await lecturePage(app, parts[1], parts[3], params);
    }
    else if (parts[0] === 's' && parts[2] === 'search' && parts.length === 3) {
      await searchPage(app, parts[1], params);
    }
    else if (parts[0] === 's' && (parts[2] === 'archive' || parts[2] === 'profile') && parts.length === 3) {
      await profilePage(app, parts[1], params);
    }
    else {
      notFoundPage(app);
    }
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
    h('a', { class: 'btn primary', href: '/home' }, 'Back to home')));
}

// The skip link must not trigger routing
document.querySelector('.skip-link')?.addEventListener('click', (e) => { e.preventDefault(); app.focus(); });

// Intercept internal link clicks to navigate smoothly without full page reloads
document.addEventListener('click', (e) => {
  const link = e.target.closest('a');
  if (!link) return;
  if (link.origin !== location.origin) return;
  if (link.target || link.hasAttribute('download') || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
  const rawHref = link.getAttribute('href') || '';
  if (rawHref.startsWith('#')) return;

  e.preventDefault();
  const nextPath = link.pathname + link.search + link.hash;
  if (location.pathname + location.search !== link.pathname + link.search) {
    history.pushState(null, '', nextPath);
    route();
  }
});

// Handle Back / Forward browser navigation
window.addEventListener('popstate', route);
window.addEventListener('hashchange', route);
route();

if (!window.marked || !window.katex) {
  console.warn('A CDN library (marked or KaTeX) did not load; questions will show as plain text. Check your internet connection.');
}
