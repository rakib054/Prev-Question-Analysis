// The four pages: home, subject, lecture, search (plus a not-found page).
import { h, plural, prettyType, hashUrl, replaceHash, kwKey, cmpQuestions, cmpQuestionsOldestFirst } from './util.js';
import { loadSubjects, loadSubject } from './data.js';
import { search, popularKeywords } from './search.js';
import { renderSearchBar, searchUrl } from './searchbar.js';
import { mountCardList } from './card.js';
import { solvedCount, isSolved, hasSolution, solutionCount, isFavorite, favoriteCount } from './store.js';

const SUBJECT_TITLE = 'Question Bank';

function setTitle(...parts) {
  document.title = [...parts.filter(Boolean), SUBJECT_TITLE].join(' · ');
}

function crumbs(items) {
  const nav = h('nav', { class: 'crumbs', 'aria-label': 'Breadcrumb' });
  items.forEach((it, i) => {
    if (i) nav.append(h('span', { class: 'crumb-sep', 'aria-hidden': 'true' }, '›'));
    nav.append(it.href ? h('a', { href: it.href }, it.label) : h('span', { 'aria-current': 'page' }, it.label));
  });
  return nav;
}

function yearText(ds) {
  if (!ds.yearRange) return 'no exams yet';
  const [a, b] = ds.yearRange;
  return a === b ? String(a) : `${a}–${b}`;
}

function subjectCodes(subject) {
  const codes = (subject.codes || []).join(', ');
  const former = (subject.former_codes || []).join(', ');
  return [codes, former ? `formerly ${former}` : ''].filter(Boolean).join(' · ');
}

// ============================================================================
// Home  #/
// ============================================================================
export async function homePage(root) {
  setTitle();
  const subjects = await loadSubjects();
  const results = await Promise.allSettled(subjects.map((s) => loadSubject(s.id)));

  const grid = h('div', { class: 'card-grid' });
  subjects.forEach((s, i) => {
    const r = results[i];
    if (r.status === 'rejected') {
      console.error(r.reason);
      grid.append(h('div', { class: 'subject-card error' }, h('h2', null, s.name || s.id), h('p', null, `Could not load data: ${r.reason.message}`)));
      return;
    }
    const ds = r.value;
    grid.append(h('a', { class: 'subject-card', href: hashUrl(['s', s.id]) },
      h('h2', null, s.name),
      h('p', { class: 'codes' }, subjectCodes(s)),
      h('p', { class: 'stats' },
        h('span', null, plural(ds.questions.length, 'question')),
        h('span', null, yearText(ds)),
        h('span', null, plural(ds.lectures.length, 'lecture')))));
  });

  root.replaceChildren(
    h('section', { class: 'hero' },
      h('h1', null, 'Previous year questions'),
      h('p', { class: 'lead' }, 'Pick a subject, then a lecture, to see every past exam question on it.')),
    subjects.length ? grid : h('p', { class: 'empty' }, 'No subjects found in data/subjects.json.'));
}

// ============================================================================
// Subject  #/s/:id
// ============================================================================
export async function subjectPage(root, id) {
  const ds = await loadSubject(id);
  setTitle(ds.subject.name);

  const grid = h('div', { class: 'card-grid lectures' }, ds.lectures.map((lec) => {
    const n = lec.questions.length;
    return h('a', { class: 'lecture-card' + (n === 0 ? ' dim' : ''), href: hashUrl(['s', id, 'l', lec.lecture]) },
      h('span', { class: 'lecture-no' }, `Lecture ${lec.lecture}`),
      h('h2', null, lec.title),
      h('p', { class: 'stats' },
        h('span', null, plural(n, 'question')),
        h('span', null, plural(lec.topics.length, 'topic'))));
  }));

  root.replaceChildren(
    crumbs([{ label: 'Home', href: '#/' }, { label: ds.subject.name }]),
    h('div', { class: 'page-head' },
      h('h1', null, ds.subject.name),
      h('p', { class: 'muted' }, [subjectCodes(ds.subject), plural(ds.questions.length, 'question'), `exams ${yearText(ds)}`].filter(Boolean).join(' · ')),
      renderSearchBar(ds)),
    ds.lectures.length ? grid : h('p', { class: 'empty' }, 'This subject has no lectures yet. Add them to its topics file.'));
}

// ============================================================================
// Lecture  #/s/:id/l/:n
// ============================================================================
export async function lecturePage(root, id, num, params) {
  const ds = await loadSubject(id);
  const lec = ds.lectureByNo.get(String(num));
  if (!lec) return notFoundPage(root, `Lecture ${num} does not exist in ${ds.subject.name}.`, hashUrl(['s', id]), 'Back to lectures');
  setTitle(`Lecture ${lec.lecture}: ${lec.title}`, ds.subject.name);

  const topicKeys = new Set(lec.topics.map((t) => kwKey(t.keyword)));
  const years = [...new Set(lec.questions.map((q) => q.year))].sort((a, b) => b - a);
  const types = [...new Set(lec.questions.map((q) => q.type))].sort();

  // ---- state (mirrored in the URL so links can be shared) ----
  const state = {
    kws: new Set((params.get('k') || '').split(',').map(kwKey).filter((k) => topicKeys.has(k))),
    year: years.map(String).includes(params.get('year')) ? params.get('year') : '',
    type: types.includes(params.get('type')) ? params.get('type') : '',
    rep: params.get('rep') === '1',
    hide: params.get('hide') === '1',
    hasSol: params.get('sol') === '1',
    showAllSol: params.get('showsol') === '1',
    oldest: params.get('order') === 'old',
  };

  const passesBase = (q) =>
    (!state.year || String(q.year) === state.year) &&
    (!state.type || q.type === state.type) &&
    (!state.rep || q.repeat) &&
    (!state.hide || !isSolved(id, q.id)) &&
    (!state.hasSol || hasSolution(id, q));
  const hasKw = (q, key) => q.kw.some((info) => info.key === key);
  const filtersActive = () => state.kws.size || state.year || state.type || state.rep || state.hide || state.hasSol;

  // ---- static parts ----
  const bar = renderSearchBar(ds);
  const sidebarList = h('ul', { class: 'kw-list' });
  const allBtn = h('button', { type: 'button', class: 'kw-all', onclick: () => { state.kws.clear(); update(); } });
  const toggle = h('button', { type: 'button', class: 'kw-toggle', 'aria-expanded': 'false', 'aria-controls': 'kw-body' });
  const body = h('div', { class: 'kw-body', id: 'kw-body' }, allBtn, sidebarList);
  const panel = h('aside', { class: 'kw-panel', 'aria-label': 'Keywords in this lecture' }, toggle, body);
  const setOpen = (open) => { panel.classList.toggle('open', open); toggle.setAttribute('aria-expanded', String(open)); };
  toggle.addEventListener('click', () => setOpen(!panel.classList.contains('open')));

  const yearSel = h('select', { 'aria-label': 'Filter by year', onchange: (e) => { state.year = e.target.value; update(); } },
    h('option', { value: '' }, 'All years'), years.map((y) => h('option', { value: String(y) }, String(y))));
  const typeSel = h('select', { 'aria-label': 'Filter by type', onchange: (e) => { state.type = e.target.value; update(); } },
    h('option', { value: '' }, 'All types'), types.map((t) => h('option', { value: t }, prettyType(t))));
  const repBox = h('input', { type: 'checkbox', onchange: (e) => { state.rep = e.target.checked; update(); } });
  const hideBox = h('input', { type: 'checkbox', onchange: (e) => { state.hide = e.target.checked; update(); } });
  const solBox = h('input', { type: 'checkbox', onchange: (e) => { state.hasSol = e.target.checked; update(); } });
  const toggleAllSolBtn = h('button', {
    type: 'button', class: 'btn',
    onclick: () => {
      state.showAllSol = !state.showAllSol;
      update();
    },
  });
  const orderBtn = h('button', { type: 'button', class: 'btn', onclick: () => { state.oldest = !state.oldest; update(); } });
  const clearBtn = h('button', { type: 'button', class: 'btn ghost', onclick: () => { state.kws.clear(); state.year = ''; state.type = ''; state.rep = false; state.hide = false; state.hasSol = false; update(); } }, 'Clear filters');

  const filters = h('div', { class: 'filters' },
    h('label', { class: 'field' }, h('span', null, 'Year'), yearSel),
    h('label', { class: 'field' }, h('span', null, 'Type'), typeSel),
    h('label', { class: 'check' }, repBox, h('span', null, 'Only repeated')),
    h('label', { class: 'check' }, hideBox, h('span', null, 'Hide solved')),
    h('label', { class: 'check' }, solBox, h('span', null, 'Has solution')),
    toggleAllSolBtn, orderBtn, clearBtn);

  const countLine = h('p', { class: 'result-count', role: 'status' });
  const list = h('div', { class: 'qlist' });
  let stopList = () => {};

  const ctx = {
    ds,
    showLectures: false,
    showAllSolutions: false,
    onKeyword: (info) => {
      if (topicKeys.has(info.key)) {
        state.kws = new Set([info.key]);
        update();
        countLine.scrollIntoView({ block: 'start', behavior: 'smooth' });
      } else {
        location.hash = searchUrl(ds, info.keyword, info.keyword);
      }
    },
    onSolved: () => (state.hide ? update() : updateCount()),
    onSolutionChange: () => (state.hasSol ? update() : updateCount()),
  };

  let visible = [];
  function updateCount() {
    const solved = solvedCount(id, visible.map((q) => q.id));
    const withSol = solutionCount(id, visible);
    const parts = [plural(visible.length, 'question')];
    if (withSol) parts.push(`${withSol} with solution`);
    if (solved) parts.push(`${solved} solved`);
    countLine.textContent = parts.join(' · ');
  }

  function update() {
    // sidebar counts follow the year/type/repeated/solved filters (not the keyword selection itself)
    const base = lec.questions.filter(passesBase);
    visible = base.filter((q) => !state.kws.size || [...state.kws].some((k) => hasKw(q, k)));
    visible.sort(state.oldest ? cmpQuestionsOldestFirst : cmpQuestions);

    allBtn.replaceChildren(h('span', null, 'All keywords'), h('span', { class: 'count' }, String(base.length)));
    allBtn.classList.toggle('active', state.kws.size === 0);
    allBtn.setAttribute('aria-pressed', String(state.kws.size === 0));
    toggle.replaceChildren(h('span', null, 'Keywords'), h('span', { class: 'count' }, state.kws.size ? `${state.kws.size} selected` : String(lec.topics.length)), h('span', { class: 'chev', 'aria-hidden': 'true' }, '▾'));

    sidebarList.replaceChildren(...lec.topics.map((t) => {
      const key = kwKey(t.keyword);
      const n = base.filter((q) => hasKw(q, key)).length;
      const on = state.kws.has(key);
      return h('li', null, h('button', {
        type: 'button', class: 'kw-item' + (on ? ' active' : '') + (n === 0 ? ' dim' : ''), 'aria-pressed': String(on),
        onclick: () => {
          if (on) state.kws.delete(key); else state.kws.add(key);
          if (window.matchMedia('(max-width: 899px)').matches) setOpen(false);
          update();
        },
      }, h('span', { class: 'kw-text' }, h('span', { class: 'kw-name' }, t.name), h('span', { class: 'kw-tag' }, t.keyword)),
        h('span', { class: 'count', 'aria-label': plural(n, 'question') }, String(n))));
    }));

    yearSel.value = state.year; typeSel.value = state.type;
    repBox.checked = state.rep; hideBox.checked = state.hide;
    solBox.checked = state.hasSol;
    toggleAllSolBtn.textContent = state.showAllSol ? 'Hide solutions 📚' : 'Show solutions 📚';
    toggleAllSolBtn.setAttribute('aria-pressed', String(state.showAllSol));
    toggleAllSolBtn.classList.toggle('primary', state.showAllSol);

    orderBtn.textContent = state.oldest ? 'Oldest first ↑' : 'Newest first ↓';
    orderBtn.setAttribute('aria-label', state.oldest ? 'Sorted oldest first. Switch to newest first' : 'Sorted newest first. Switch to oldest first');
    clearBtn.hidden = !filtersActive();
    updateCount();

    ctx.showAllSolutions = state.showAllSol;
    stopList();
    if (visible.length) {
      stopList = mountCardList(list, visible, ctx);
    } else {
      stopList = () => {};
      list.replaceChildren(h('div', { class: 'empty-state' },
        h('p', { class: 'empty-title' }, lec.questions.length ? 'No questions match these filters.' : 'No past questions for this lecture yet.'),
        lec.questions.length && filtersActive() ? h('button', { type: 'button', class: 'btn', onclick: () => clearBtn.click() }, 'Clear filters') : null));
    }

    replaceHash(hashUrl(['s', id, 'l', num], {
      k: [...state.kws].map((k) => ds.kwInfo.get(k)?.keyword || k).join(','),
      year: state.year, type: state.type, rep: state.rep, hide: state.hide,
      sol: state.hasSol ? '1' : '', showsol: state.showAllSol ? '1' : '', order: state.oldest ? 'old' : '',
    }));
  }

  const idx = ds.lectures.findIndex((l) => l.lecture === lec.lecture);
  const prev = ds.lectures[idx - 1], next = ds.lectures[idx + 1];
  const pager = h('nav', { class: 'pager', 'aria-label': 'Other lectures' },
    prev ? h('a', { class: 'btn', href: hashUrl(['s', id, 'l', prev.lecture]) }, `← Lecture ${prev.lecture}`) : h('span'),
    next ? h('a', { class: 'btn', href: hashUrl(['s', id, 'l', next.lecture]) }, `Lecture ${next.lecture} →`) : h('span'));

  root.replaceChildren(
    crumbs([{ label: 'Home', href: '#/' }, { label: ds.subject.name, href: hashUrl(['s', id]) }, { label: `Lecture ${lec.lecture}` }]),
    h('div', { class: 'page-head' },
      h('p', { class: 'eyebrow' }, `Lecture ${lec.lecture}`),
      h('h1', null, lec.title),
      bar),
    h('div', { class: 'lecture-layout' }, panel, h('section', { class: 'results', 'aria-label': 'Questions' }, filters, countLine, list)),
    pager);
  update();
}

// ============================================================================
// Search  #/s/:id/search?q=...&k=#Keyword
// ============================================================================
export async function searchPage(root, id, params) {
  const ds = await loadSubject(id);
  const state = { q: params.get('q') || '', k: params.get('k') || '' };
  let showAllSol = false;

  const info = h('div', { class: 'search-info' });
  const kwBox = h('div', { class: 'kw-matches' });
  const countLine = h('p', { class: 'result-count', role: 'status' });
  const toggleAllSolBtn = h('button', {
    type: 'button', class: 'btn',
    onclick: () => {
      showAllSol = !showAllSol;
      update();
    },
  });
  const searchControls = h('div', { class: 'search-controls', style: 'display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; margin: 8px 0;' }, countLine, toggleAllSolBtn);
  const list = h('div', { class: 'qlist' });
  let stopList = () => {};
  let bar;

  const run = (q, k) => {
    state.q = q; state.k = k || '';
    if (bar && bar.input.value !== q) bar.input.value = q;
    update();
  };

  const ctx = {
    ds,
    showLectures: true,
    showAllSolutions: false,
    onKeyword: (kw) => run(kw.keyword, kw.keyword),
    onSolutionChange: () => update(),
    onSolved: () => update(),
  };

  bar = renderSearchBar(ds, { value: state.q, onLive: (v) => run(v, state.k && kwKey(v) === kwKey(state.k) ? state.k : '') });

  function chip(inf, selected, onclick) {
    return h('button', {
      type: 'button', class: 'chip big' + (selected ? ' active' : ''), 'aria-pressed': String(selected), title: inf.name, onclick,
    }, inf.keyword, h('span', { class: 'count' }, String(inf.questions.length)), selected ? h('span', { class: 'x', 'aria-hidden': 'true' }, '×') : null);
  }

  function update() {
    if (bar && !bar.isConnected) return; // page was replaced while a debounced search was pending
    const res = search(ds, state.q, { exactKw: state.k });
    const q = state.q.trim();
    const selected = state.k ? ds.kwInfo.get(kwKey(state.k)) : null;
    setTitle(q ? `Search: ${q}` : 'Search', ds.subject.name);

    ctx.showAllSolutions = showAllSol;
    toggleAllSolBtn.textContent = showAllSol ? 'Hide solutions 📚' : 'Show solutions 📚';
    toggleAllSolBtn.setAttribute('aria-pressed', String(showAllSol));
    toggleAllSolBtn.classList.toggle('primary', showAllSol);

    // matching keyword chips (keywords with at least one question)
    const chips = res.keywords.filter((i) => i.questions.length);
    if (selected && !chips.includes(selected)) chips.unshift(selected);
    kwBox.replaceChildren();
    if (chips.length) {
      kwBox.append(
        h('p', { class: 'kw-matches-title' }, 'Matching keywords'),
        h('div', { class: 'chips' }, chips.map((i) => chip(i, i === selected, () => run(state.q, i === selected ? '' : i.keyword)))));
    }

    // note about exact mode
    info.replaceChildren();
    if (res.exact && !state.k) info.append(h('p', { class: 'muted' }, `Showing only questions tagged ${res.exact.keyword} (${res.exact.name}).`));
    if (state.k && selected) info.append(h('p', { class: 'muted' }, `Narrowed to ${selected.keyword}. Click the chip again to widen.`));

    stopList();
    stopList = () => {};
    if (!res.tokens.length && !state.k) {
      countLine.textContent = '';
      toggleAllSolBtn.hidden = true;
      list.replaceChildren(hintBox('Type a keyword or any words from a question.', ds, run));
    } else if (!res.results.length) {
      countLine.textContent = '0 results';
      toggleAllSolBtn.hidden = true;
      list.replaceChildren(hintBox(`No questions match “${q || state.k}”. Try a shorter word, or fewer words.`, ds, run));
    } else {
      toggleAllSolBtn.hidden = false;
      const withSol = solutionCount(id, res.results);
      const countParts = [`${plural(res.results.length, 'result')}${q ? ` for “${q}”` : ''}`];
      if (withSol) countParts.push(`${withSol} with solution`);
      countLine.textContent = countParts.join(' · ');
      stopList = mountCardList(list, res.results, ctx);
    }
    replaceHash(searchUrl(ds, q, state.k));
  }

  root.replaceChildren(
    crumbs([{ label: 'Home', href: '#/' }, { label: ds.subject.name, href: hashUrl(['s', id]) }, { label: 'Search' }]),
    h('div', { class: 'page-head' }, h('h1', null, 'Search'), bar),
    kwBox, info, searchControls, list);
  update();
  if (!state.q && !state.k) bar.input.focus();
}

function hintBox(message, ds, run) {
  const pop = popularKeywords(ds, 10);
  return h('div', { class: 'empty-state' },
    h('p', { class: 'empty-title' }, message),
    pop.length ? h('p', { class: 'muted' }, 'Popular keywords:') : null,
    pop.length ? h('div', { class: 'chips center' }, pop.map((i) => h('button', { type: 'button', class: 'chip big', onclick: () => run(i.keyword, i.keyword) }, i.keyword, h('span', { class: 'count' }, String(i.questions.length))))) : null);
}

// ============================================================================
// Archive  #/archive or #/s/:id/archive?tab=favorites|solved|solutions
// ============================================================================
export async function profilePage(root, subjectId, params) {
  const subjects = await loadSubjects();
  const sid = subjectId || subjects[0]?.id || 'toc';
  const ds = await loadSubject(sid);

  setTitle('Archive', ds.subject.name);

  const state = {
    tab: ['favorites', 'solved', 'solutions'].includes(params.get('tab')) ? params.get('tab') : 'favorites',
    showAllSol: params.get('showsol') === '1',
    oldest: params.get('order') === 'old',
  };

  const countLine = h('p', { class: 'result-count', role: 'status' });
  const list = h('div', { class: 'qlist' });
  let stopList = () => {};

  const orderBtn = h('button', {
    type: 'button', class: 'btn',
    onclick: () => {
      state.oldest = !state.oldest;
      update();
    },
  });

  const toggleAllSolBtn = h('button', {
    type: 'button', class: 'btn',
    onclick: () => {
      state.showAllSol = !state.showAllSol;
      update();
    },
  });

  const tabFav = h('button', {
    type: 'button', class: 'profile-tab-btn',
    onclick: () => setTab('favorites'),
  });

  const tabSolved = h('button', {
    type: 'button', class: 'profile-tab-btn',
    onclick: () => setTab('solved'),
  });

  const tabSol = h('button', {
    type: 'button', class: 'profile-tab-btn',
    onclick: () => setTab('solutions'),
  });

  const tabsNav = h('div', { class: 'profile-tabs', role: 'tablist' }, tabFav, tabSolved, tabSol);

  function setTab(tab) {
    state.tab = tab;
    update();
  }

  const ctx = {
    ds,
    showLectures: true,
    showAllSolutions: false,
    onFavorite: () => update(),
    onSolved: () => update(),
    onSolutionChange: () => update(),
  };

  // Stats cards
  const statFavVal = h('span', { class: 'stat-num' });
  const statSolvedVal = h('span', { class: 'stat-num' });
  const statSolVal = h('span', { class: 'stat-num' });
  const statTotalVal = h('span', { class: 'stat-num' }, String(ds.questions.length));

  const statsGrid = h('div', { class: 'profile-stats-grid' },
    h('div', { class: 'stat-card', onclick: () => setTab('favorites'), role: 'button', tabindex: 0 },
      h('span', { class: 'stat-icon' }, '⭐'),
      h('div', null, statFavVal, h('span', { class: 'stat-label' }, 'Favorites'))),
    h('div', { class: 'stat-card', onclick: () => setTab('solved'), role: 'button', tabindex: 0 },
      h('span', { class: 'stat-icon' }, '✅'),
      h('div', null, statSolvedVal, h('span', { class: 'stat-label' }, 'Solved'))),
    h('div', { class: 'stat-card', onclick: () => setTab('solutions'), role: 'button', tabindex: 0 },
      h('span', { class: 'stat-icon' }, '📚'),
      h('div', null, statSolVal, h('span', { class: 'stat-label' }, 'With Solution'))),
    h('div', { class: 'stat-card total' },
      h('span', { class: 'stat-icon' }, '📋'),
      h('div', null, statTotalVal, h('span', { class: 'stat-label' }, 'Total Questions'))));

  function update() {
    const total = ds.questions.length;
    const favs = ds.questions.filter((q) => isFavorite(sid, q.id));
    const solved = ds.questions.filter((q) => isSolved(sid, q.id));
    const withSol = ds.questions.filter((q) => hasSolution(sid, q));

    statFavVal.textContent = String(favs.length);
    statSolvedVal.textContent = `${solved.length} (${Math.round((solved.length / (total || 1)) * 100)}%)`;
    statSolVal.textContent = `${withSol.length} (${Math.round((withSol.length / (total || 1)) * 100)}%)`;

    tabFav.replaceChildren(h('span', null, '⭐ Favorites'), h('span', { class: 'count' }, String(favs.length)));
    tabFav.classList.toggle('active', state.tab === 'favorites');
    tabFav.setAttribute('aria-selected', String(state.tab === 'favorites'));

    tabSolved.replaceChildren(h('span', null, '✅ Solved'), h('span', { class: 'count' }, String(solved.length)));
    tabSolved.classList.toggle('active', state.tab === 'solved');
    tabSolved.setAttribute('aria-selected', String(state.tab === 'solved'));

    tabSol.replaceChildren(h('span', null, '📚 Has Solution'), h('span', { class: 'count' }, String(withSol.length)));
    tabSol.classList.toggle('active', state.tab === 'solutions');
    tabSol.setAttribute('aria-selected', String(state.tab === 'solutions'));

    orderBtn.textContent = state.oldest ? 'Oldest first ↑' : 'Newest first ↓';
    toggleAllSolBtn.textContent = state.showAllSol ? 'Hide solutions 📚' : 'Show solutions 📚';
    toggleAllSolBtn.classList.toggle('primary', state.showAllSol);

    let listItems = [];
    let emptyTitle = '';
    let emptySub = '';
    if (state.tab === 'favorites') {
      listItems = [...favs];
      emptyTitle = 'No favorite questions yet';
      emptySub = 'Click the ☆ Save icon on any question to bookmark it here for quick revision.';
    } else if (state.tab === 'solved') {
      listItems = [...solved];
      emptyTitle = 'No solved questions yet';
      emptySub = 'Check the "Solved" box on questions as you complete them to track your progress.';
    } else {
      listItems = [...withSol];
      emptyTitle = 'No questions with solutions yet';
      emptySub = 'Click the 📚 Solution button on any question to view or write a solution.';
    }

    listItems.sort(state.oldest ? cmpQuestionsOldestFirst : cmpQuestions);
    countLine.textContent = `${plural(listItems.length, 'question')} in ${state.tab}`;

    ctx.showAllSolutions = state.showAllSol;
    stopList();
    if (listItems.length) {
      stopList = mountCardList(list, listItems, ctx);
    } else {
      stopList = () => {};
      list.replaceChildren(h('div', { class: 'empty-state' },
        h('p', { class: 'empty-title' }, emptyTitle),
        h('p', { class: 'muted' }, emptySub),
        h('a', { class: 'btn primary', href: hashUrl(['s', sid]) }, 'Browse Questions')));
    }

    replaceHash(hashUrl(['s', sid, 'archive'], {
      tab: state.tab, order: state.oldest ? 'old' : '', showsol: state.showAllSol ? '1' : '',
    }));
  }

  const profileToolbar = h('div', { class: 'profile-toolbar' }, tabsNav, h('div', { class: 'profile-actions' }, toggleAllSolBtn, orderBtn));

  root.replaceChildren(
    crumbs([{ label: 'Home', href: '#/' }, { label: ds.subject.name, href: hashUrl(['s', sid]) }, { label: 'Archive' }]),
    h('div', { class: 'page-head profile-head' },
      h('h1', null, 'Archive & Saved Questions'),
      h('p', { class: 'muted' }, `${ds.subject.name} · Track your revision progress and bookmarked questions.`)),
    statsGrid,
    profileToolbar,
    countLine,
    list);

  update();
}

// ============================================================================
// Not found
// ============================================================================
export function notFoundPage(root, message = 'That page does not exist.', href = '#/', label = 'Back to home') {
  setTitle('Not found');
  root.replaceChildren(h('div', { class: 'empty-state' },
    h('h1', null, 'Not found'), h('p', null, message), h('a', { class: 'btn primary', href }, label)));
}
