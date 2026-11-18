// Small helpers shared by all modules.

/** Create an element: h('div', {class:'x', onclick: fn}, 'text', childNode, ...) */
export function h(tag, attrs, ...children) {
  const node = document.createElement(tag);
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v === null || v === undefined || v === false) continue;
      if (k === 'class') node.className = v;
      else if (k === 'dataset') Object.assign(node.dataset, v);
      else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
      else if (k === 'html') node.innerHTML = v;
      else if (v === true) node.setAttribute(k, '');
      else node.setAttribute(k, v);
    }
  }
  appendChildren(node, children);
  return node;
}

function appendChildren(node, children) {
  for (const c of children) {
    if (c === null || c === undefined || c === false) continue;
    if (Array.isArray(c)) appendChildren(node, c);
    else node.append(c.nodeType ? c : document.createTextNode(String(c)));
  }
}

export function clear(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
  return node;
}

export function debounce(fn, ms) {
  let t;
  const wrapped = (...args) => {
    clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
  wrapped.cancel = () => clearTimeout(t);
  return wrapped;
}

export function plural(n, one, many) {
  return `${n} ${n === 1 ? one : (many || one + 's')}`;
}

/** "short-note" -> "Short note" */
export function prettyType(t) {
  const s = String(t || 'other').replace(/[-_]+/g, ' ').trim();
  return s.charAt(0).toUpperCase() + s.slice(1);
}

/** Natural comparison for question numbers / parts that may be numbers or strings. */
export function cmpNatural(a, b) {
  const na = Number(a), nb = Number(b);
  if (a !== null && b !== null && a !== '' && b !== '' && !Number.isNaN(na) && !Number.isNaN(nb)) return na - nb;
  return String(a ?? '').localeCompare(String(b ?? ''), undefined, { numeric: true });
}

/** Default question order: newest year first, then question number, then part. */
export function cmpQuestions(a, b) {
  return (b.year - a.year) || cmpNatural(a.qno, b.qno) || cmpNatural(a.part, b.part) || a._order - b._order;
}

export function cmpQuestionsOldestFirst(a, b) {
  return (a.year - b.year) || cmpNatural(a.qno, b.qno) || cmpNatural(a.part, b.part) || a._order - b._order;
}

/** Keywords are compared case-insensitively and always with a leading '#'. */
export function kwKey(kw) {
  return String(kw ?? '').trim().replace(/^#+/, '').toLowerCase();
}

export function withHash(kw) {
  const s = String(kw ?? '').trim();
  return s.startsWith('#') ? s : '#' + s;
}

/** Build a hash URL like "#/s/toc/l/5?k=%23DFA". Params with empty values are dropped. */
export function hashUrl(pathParts, params) {
  const path = '#/' + pathParts.map(encodeURIComponent).join('/');
  const usp = new URLSearchParams();
  for (const [k, v] of Object.entries(params || {})) {
    if (v !== null && v !== undefined && v !== '' && v !== false) usp.set(k, v === true ? '1' : v);
  }
  const qs = usp.toString();
  return qs ? `${path}?${qs}` : path;
}

/** Change the URL without triggering the router (used for filter state). */
export function replaceHash(url) {
  history.replaceState(null, '', url);
}

export function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'auto' });
}
