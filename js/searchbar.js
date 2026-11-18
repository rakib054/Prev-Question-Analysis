// Search bar shown on the subject, lecture and search pages.
//  * live mode (search page): results update while typing (debounced) via opts.onLive
//  * navigate mode (other pages): Enter / button opens the search page; while typing, matching keywords
//    are suggested in a dropdown (debounced).
import { SEARCH_DEBOUNCE_MS } from './config.js';
import { h, debounce, hashUrl, plural } from './util.js';
import { matchingKeywords } from './search.js';

let uid = 0;

export function searchUrl(ds, q, k) {
  return hashUrl(['s', ds.id, 'search'], { q, k });
}

export function renderSearchBar(ds, opts = {}) {
  const id = `sb-${++uid}`;
  const input = h('input', {
    id, class: 'search-input', type: 'search', name: 'q', value: opts.value || '',
    placeholder: opts.placeholder || 'Search e.g. cfg, #DFA, pumping',
    autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false', enterkeyhint: 'search',
    'aria-label': 'Search questions',
  });
  const list = h('ul', { class: 'suggest', role: 'listbox', hidden: true, 'aria-label': 'Matching keywords' });
  const go = h('button', { class: 'btn primary', type: 'submit' }, 'Search');
  const form = h('form', { class: 'searchbar', role: 'search' }, h('div', { class: 'search-field' }, input, list), go);

  const hideSuggest = () => { list.hidden = true; list.replaceChildren(); };

  const showSuggest = debounce(() => {
    const q = input.value.trim();
    if (!q) return hideSuggest();
    const items = matchingKeywords(ds, q).filter((i) => i.questions.length).slice(0, 6);
    list.replaceChildren(...items.map((info) =>
      h('li', { role: 'option' },
        h('a', { href: searchUrl(ds, info.keyword, info.keyword), class: 'suggest-item' },
          h('span', { class: 'suggest-name' }, info.name),
          h('span', { class: 'suggest-kw' }, info.keyword),
          h('span', { class: 'count' }, plural(info.questions.length, 'question'))))));
    list.hidden = items.length === 0;
  }, SEARCH_DEBOUNCE_MS);

  const live = opts.onLive ? debounce(() => opts.onLive(input.value), SEARCH_DEBOUNCE_MS) : null;

  input.addEventListener('input', () => { if (live) live(); else showSuggest(); });
  input.addEventListener('keydown', (e) => { if (e.key === 'Escape') hideSuggest(); });
  form.addEventListener('focusout', () => setTimeout(() => { if (!form.contains(document.activeElement)) hideSuggest(); }, 150));
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (live) live.cancel();
    showSuggest.cancel();
    hideSuggest();
    if (opts.onLive) opts.onLive(input.value);
    else location.hash = searchUrl(ds, input.value.trim());
  });

  form.input = input;
  return form;
}
