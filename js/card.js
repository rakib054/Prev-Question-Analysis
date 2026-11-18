// Question card, figure lightbox and the progressively-rendered card list.
import { SHOW_REVIEW_FLAGS, PAGE_SIZE } from './config.js';
import { h, prettyType, hashUrl } from './util.js';
import { renderMarkdown } from './render.js';
import { isSolved, setSolved, getSolution, hasSolution, setSolution, deleteSolution, isFavorite, setFavorite } from './store.js';

// ---- helpers ---------------------------------------------------------------

export function questionLabel(q) {
  const parts = [];
  if (q.year) parts.push(String(q.year));
  parts.push(`Q${q.qno ?? '?'}${q.part ? `(${q.part})` : ''}`);
  if (q.marks !== null && q.marks !== undefined && q.marks !== '') parts.push(`${q.marks} marks`);
  if (q.co !== null && q.co !== undefined && String(q.co).trim() !== '') {
    const co = String(q.co).trim();
    parts.push(/^co/i.test(co) ? co.toUpperCase() : `CO${co}`);
  }
  return parts;
}

// ---- lightbox --------------------------------------------------------------

let lightbox;
function getLightbox() {
  if (lightbox) return lightbox;
  const img = h('img', { alt: '' });
  const caption = h('p', { class: 'lightbox-caption' });
  const close = h('button', { class: 'lightbox-close', type: 'button', 'aria-label': 'Close figure' }, '×');
  const dlg = h('dialog', { class: 'lightbox', 'aria-label': 'Figure' }, close, img, caption);
  dlg.addEventListener('click', () => dlg.close());
  dlg.img = img;
  dlg.caption = caption;
  document.body.append(dlg);
  lightbox = dlg;
  return dlg;
}

function zoom(fig) {
  const dlg = getLightbox();
  dlg.img.src = fig.src;
  dlg.img.alt = fig.alt || '';
  dlg.caption.textContent = fig.alt || '';
  if (typeof dlg.showModal === 'function') dlg.showModal(); else window.open(fig.src, '_blank');
}

// ---- card ------------------------------------------------------------------

/**
 * @param q   enriched question (see data.js)
 * @param ctx { ds, onKeyword(info), onSolved(q, value), onSolutionChange(q, value), showLectures:boolean, showAllSolutions:boolean }
 */
export function renderCard(q, ctx) {
  const ds = ctx.ds;
  const label = questionLabel(q);
  const examTitle = [q.exam.term, q.exam.paper_code, q.section ? `Section ${q.section}` : ''].filter(Boolean).join(' · ');

  // header
  const head = h('div', { class: 'qhead' });
  const meta = h('h3', { class: 'qmeta', title: examTitle || null });
  label.forEach((part, i) => {
    if (i) meta.append(h('span', { class: 'sep', 'aria-hidden': 'true' }, ' · '));
    meta.append(h('span', { class: i === 0 ? 'qyear' : null }, part));
  });

  const solved = h('input', {
    type: 'checkbox', class: 'solved-box',
    onchange: (e) => {
      setSolved(ds.id, q.id, e.target.checked);
      card.classList.toggle('is-solved', e.target.checked);
      if (ctx.onSolved) ctx.onSolved(q, e.target.checked);
    },
  });
  solved.checked = isSolved(ds.id, q.id);
  const solvedLabel = h('label', { class: 'solved' }, solved, h('span', null, 'Solved'));

  // save / favorite button in header
  let isFav = isFavorite(ds.id, q.id);
  const favIcon = h('span', { class: 'fav-icon', 'aria-hidden': 'true' }, isFav ? '★' : '☆');
  const btnFavText = h('span', { class: 'btn-fav-text' }, isFav ? 'Saved' : 'Save');
  const favBadge = h('span', { class: 'badge fav-badge', title: 'Saved question' }, '★ Saved');

  const btnFav = h('button', {
    type: 'button',
    class: 'btn-fav-toggle' + (isFav ? ' is-fav' : ''),
    'aria-label': isFav ? 'Remove from favorites' : 'Save question to favorites',
    title: isFav ? 'Saved (click to remove)' : 'Save question',
    onclick: () => {
      isFav = !isFav;
      setFavorite(ds.id, q.id, isFav);
      favIcon.textContent = isFav ? '★' : '☆';
      btnFavText.textContent = isFav ? 'Saved' : 'Save';
      btnFav.classList.toggle('is-fav', isFav);
      btnFav.title = isFav ? 'Saved (click to remove)' : 'Save question';
      btnFav.setAttribute('aria-label', isFav ? 'Remove from favorites' : 'Save question to favorites');
      card.classList.toggle('is-fav', isFav);
      if (isFav) {
        if (!badges.contains(favBadge)) badges.prepend(favBadge);
      } else {
        favBadge.remove();
      }
      if (ctx.onFavorite) ctx.onFavorite(q, isFav);
    },
  }, favIcon, btnFavText);

  // solution toggle button in header
  let isOpen = !!ctx.showAllSolutions;
  let isEditing = false;

  const solToggleText = h('span', { class: 'btn-sol-text' }, hasSolution(ds.id, q) ? 'Solution' : 'Add solution');
  const solToggle = h('button', {
    type: 'button',
    class: 'btn-sol-toggle' + (hasSolution(ds.id, q) ? ' has-sol' : '') + (isOpen ? ' active' : ''),
    'aria-expanded': String(isOpen),
    title: 'Toggle solution',
    onclick: () => {
      isOpen = !isOpen;
      solWrap.hidden = !isOpen;
      solToggle.classList.toggle('active', isOpen);
      solToggle.setAttribute('aria-expanded', String(isOpen));
      if (isOpen && !hasSolution(ds.id, q) && !isEditing) {
        startEditing();
      }
    },
  }, h('span', { class: 'icon', 'aria-hidden': 'true' }, '📚'), solToggleText);

  const headActions = h('div', { class: 'qhead-actions' }, btnFav, solToggle, solvedLabel);
  head.append(meta, headActions);

  // badges row
  const badges = h('div', { class: 'qbadges' },
    h('span', { class: 'badge type', dataset: { type: q.type } }, prettyType(q.type)));

  if (isFav) badges.prepend(favBadge);

  if (SHOW_REVIEW_FLAGS && q.needs_review) {
    badges.append(q.review_note
      ? h('details', { class: 'review' }, h('summary', { class: 'badge warn' }, '⚠ unverified'), h('p', { class: 'review-note' }, q.review_note))
      : h('span', { class: 'badge warn' }, '⚠ unverified'));
  }
  if (ctx.showLectures) {
    for (const n of q.lectures) {
      const lec = ds.lectureByNo.get(String(n));
      badges.append(h('a', { class: 'badge lecture', href: hashUrl(['s', ds.id, 'l', n]), title: lec ? lec.title : '' }, `Lecture ${n}`));
    }
    if (!q.lectures.length) badges.append(h('span', { class: 'badge muted', title: 'None of this question\'s keywords belongs to a lecture' }, 'No lecture'));
  }

  // body
  const body = h('div', { class: 'qtext md', html: renderMarkdown(q.text) });

  const figs = q.figures.length ? h('div', { class: 'qfigs' }, q.figures.map((f) => {
    const img = h('img', { src: f.src, alt: f.alt || '', loading: 'lazy', decoding: 'async' });
    img.addEventListener('error', () => {
      btn.replaceWith(h('p', { class: 'fig-missing' }, `Figure not found: ${f.src}`));
    });
    const btn = h('button', { type: 'button', class: 'fig-btn', 'aria-label': `Zoom figure${f.alt ? ': ' + f.alt : ''}`, onclick: () => zoom(f) }, img);
    return h('figure', { class: 'qfig' }, btn);
  })) : null;

  // ---- Solution Section ----------------------------------------------------
  const solWrap = h('section', { class: 'qsolution-wrap', 'aria-label': 'Question solution' });
  solWrap.hidden = !isOpen;

  const solBox = h('div', { class: 'qsolution-box' });
  solWrap.append(solBox);

  const solBody = h('div', { class: 'qsolution-content' });
  const solEditor = h('div', { class: 'qsolution-editor' });
  solEditor.hidden = true;

  const btnEdit = h('button', {
    type: 'button', class: 'btn btn-sm',
    onclick: () => startEditing(),
  }, '✏️ Edit');

  const btnCopy = h('button', {
    type: 'button', class: 'btn btn-sm',
    onclick: async () => {
      const text = getSolution(ds.id, q);
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
        btnCopy.textContent = '✓ Copied!';
        setTimeout(() => { btnCopy.textContent = '📋 Copy'; }, 1800);
      } catch (e) {
        prompt('Copy solution:', text);
      }
    },
  }, '📋 Copy');

  const btnDelete = h('button', {
    type: 'button', class: 'btn btn-sm ghost btn-del',
    title: 'Delete custom solution',
    onclick: () => {
      if (confirm('Delete this solution?')) {
        deleteSolution(ds.id, q.id);
        refreshView();
        if (ctx.onSolutionChange) ctx.onSolutionChange(q, '');
      }
    },
  }, '🗑️');

  const solHeaderTitle = h('span', { class: 'qsolution-title' }, '📚 Solution');
  const solHeaderActions = h('div', { class: 'qsolution-actions' });
  const solHeader = h('div', { class: 'qsolution-header' }, solHeaderTitle, solHeaderActions);

  // Editor components
  const textarea = h('textarea', {
    class: 'sol-textarea',
    rows: 6,
    placeholder: 'Write solution here using Markdown and LaTeX math ($...$, $$...$)...',
    spellcheck: 'false',
  });

  const previewBox = h('div', { class: 'sol-preview md' });
  previewBox.hidden = true;

  const tabWrite = h('button', {
    type: 'button', class: 'tab-btn active',
    onclick: () => showTab('write'),
  }, 'Write');

  const tabPreview = h('button', {
    type: 'button', class: 'tab-btn',
    onclick: () => showTab('preview'),
  }, 'Preview');

  const editorTabs = h('div', { class: 'editor-tabs' }, tabWrite, tabPreview);

  function showTab(tab) {
    if (tab === 'preview') {
      tabPreview.classList.add('active');
      tabWrite.classList.remove('active');
      textarea.hidden = true;
      previewBox.hidden = false;
      previewBox.innerHTML = renderMarkdown(textarea.value.trim() || '*No content to preview*');
    } else {
      tabWrite.classList.add('active');
      tabPreview.classList.remove('active');
      textarea.hidden = false;
      previewBox.hidden = true;
      textarea.focus();
    }
  }

  const btnSave = h('button', {
    type: 'button', class: 'btn primary btn-sm',
    onclick: () => {
      const val = textarea.value.trim();
      setSolution(ds.id, q.id, val);
      stopEditing();
      refreshView();
      if (ctx.onSolutionChange) ctx.onSolutionChange(q, val);
    },
  }, 'Save Solution');

  const btnCancel = h('button', {
    type: 'button', class: 'btn ghost btn-sm',
    onclick: () => stopEditing(),
  }, 'Cancel');

  const editorHelp = h('p', { class: 'editor-help muted' },
    'Supports Markdown (tables, lists, **bold**) and KaTeX math: ',
    h('code', null, '$inline$'), ' and ', h('code', null, '$$display$$'), '.');

  const editorButtons = h('div', { class: 'editor-actions' }, btnSave, btnCancel);
  solEditor.append(editorTabs, textarea, previewBox, editorHelp, editorButtons);

  function startEditing() {
    isEditing = true;
    textarea.value = getSolution(ds.id, q);
    showTab('write');
    solBody.hidden = true;
    solEditor.hidden = false;
    solHeaderActions.hidden = true;
  }

  function stopEditing() {
    isEditing = false;
    solBody.hidden = false;
    solEditor.hidden = true;
    solHeaderActions.hidden = false;
  }

  function refreshView() {
    const text = getSolution(ds.id, q);
    const hasSol = !!text;
    solHeaderActions.replaceChildren();
    if (hasSol) {
      solHeaderActions.append(btnEdit, btnCopy, btnDelete);
      solBody.replaceChildren(h('div', { class: 'md', html: renderMarkdown(text) }));
      solToggle.classList.add('has-sol');
      solToggleText.textContent = 'Solution';
    } else {
      solHeaderActions.append(btnEdit);
      const btnAddSol = h('button', {
        type: 'button', class: 'btn primary btn-sm',
        onclick: () => startEditing(),
      }, '+ Add solution');
      solBody.replaceChildren(
        h('div', { class: 'sol-empty' },
          h('p', null, 'No solution has been added for this question yet.'),
          btnAddSol));
      solToggle.classList.remove('has-sol');
      solToggleText.textContent = 'Add solution';
    }
  }

  refreshView();
  solBox.append(solHeader, solBody, solEditor);

  // footer
  const chips = h('div', { class: 'chips', 'aria-label': 'Keywords' }, q.kw.map((info) =>
    h('button', {
      type: 'button',
      class: 'chip' + (info.known ? '' : ' unknown'),
      title: info.known ? info.name : 'Keyword not in the topics file',
      onclick: () => ctx.onKeyword && ctx.onKeyword(info),
    }, info.keyword)));
  const repeat = q.repeat
    ? h('p', { class: 'repeat' }, `Asked ${q.repeat.count} times (${q.repeat.years.join(', ')})`)
    : null;

  const card = h('article', { class: 'qcard' + (solved.checked ? ' is-solved' : '') + (isFav ? ' is-fav' : ''), id: `q-${q.id}`, dataset: { qid: q.id } },
    head, badges, body, figs, solWrap, repeat, chips.childNodes.length ? chips : null);
  return card;
}

// ---- progressive list ------------------------------------------------------

/**
 * Renders `questions` into `container` in batches; more load on button click or when scrolled near the end.
 * Returns a function that stops observing (call before re-rendering).
 */
export function mountCardList(container, questions, ctx) {
  container.replaceChildren();
  let shown = 0;
  let observer = null;
  const more = h('button', { type: 'button', class: 'btn more' }, 'Show more');
  const sentinel = h('div', { class: 'sentinel', 'aria-hidden': 'true' });

  function renderBatch() {
    const frag = document.createDocumentFragment();
    const end = Math.min(shown + PAGE_SIZE, questions.length);
    for (; shown < end; shown++) frag.append(renderCard(questions[shown], ctx));
    container.insertBefore(frag, sentinel);
    if (shown >= questions.length) { more.remove(); sentinel.remove(); if (observer) observer.disconnect(); }
    else more.textContent = `Show more (${questions.length - shown} left)`;
  }

  more.addEventListener('click', renderBatch);
  container.append(sentinel);
  if (questions.length > PAGE_SIZE) container.append(more);
  renderBatch();
  if (shown < questions.length && 'IntersectionObserver' in window) {
    observer = new IntersectionObserver((entries) => { if (entries.some((e) => e.isIntersecting)) renderBatch(); }, { rootMargin: '600px' });
    observer.observe(sentinel);
  }
  return () => observer && observer.disconnect();
}
