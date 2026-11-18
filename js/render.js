// Markdown + KaTeX rendering with HTML sanitising, and LaTeX stripping for search.
//
// Pipeline: protect code -> pull out $...$ / $$...$$ -> marked -> sanitise -> put KaTeX output back.
// Math is pulled out first so Markdown never mangles underscores, asterisks or pipes inside formulas.

const PH = 'KTXPH';           // placeholder prefix (letters/digits only, safe for Markdown)
const PH_RE = /KTXPH(\d+)KTX/g;

const cache = new Map();

export function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// ---- math extraction -------------------------------------------------------

const CODE_SPLIT = /(```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`)/g;
const DISPLAY_RE = /\$\$([\s\S]+?)\$\$/g;
// Inline: $x$ where the opening $ is followed by non-space and the closing $ is not followed by a digit,
// so prices like "$5 and $6" are left alone.
const INLINE_RE = /(^|[^\\$])\$(?!\s)((?:\\.|[^$\\\n])+?)\$(?!\d)/g;

function renderMath(tex, display) {
  if (!window.katex) return `<code>${escapeHtml(display ? `$$${tex}$$` : `$${tex}$`)}</code>`;
  try {
    return window.katex.renderToString(tex, {
      displayMode: display,
      throwOnError: false,
      strict: 'ignore',
      trust: false,
      output: 'htmlAndMathml',
    });
  } catch (e) {
    return `<code>${escapeHtml(tex)}</code>`;
  }
}

function extractMath(src) {
  const store = [];
  const put = (tex, display) => {
    store.push(renderMath(tex.trim(), display));
    return `${PH}${store.length - 1}KTX`;
  };
  const parts = src.split(CODE_SPLIT);
  const out = parts.map((part, i) => {
    if (i % 2 === 1) return part; // code: leave untouched
    return part
      .replace(DISPLAY_RE, (_, tex) => put(tex, true))
      .replace(INLINE_RE, (m, pre, tex) => (/\s$/.test(tex) ? m : pre + put(tex, false)));
  });
  return { text: out.join(''), store };
}

// ---- sanitiser -------------------------------------------------------------

const ALLOWED = new Set([
  'P', 'BR', 'STRONG', 'EM', 'B', 'I', 'U', 'S', 'DEL', 'INS', 'MARK', 'SMALL', 'CODE', 'PRE', 'KBD', 'BLOCKQUOTE',
  'UL', 'OL', 'LI', 'DL', 'DT', 'DD', 'TABLE', 'THEAD', 'TBODY', 'TFOOT', 'TR', 'TH', 'TD', 'CAPTION',
  'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'HR', 'A', 'SPAN', 'DIV', 'SUB', 'SUP', 'INPUT',
]);
const DROP_WITH_CONTENT = new Set(['SCRIPT', 'STYLE', 'IFRAME', 'OBJECT', 'EMBED', 'NOSCRIPT', 'TEMPLATE', 'LINK', 'META', 'SVG', 'MATH', 'FORM', 'TEXTAREA', 'SELECT', 'BUTTON']);
const ALLOWED_ATTRS = { A: ['href', 'title'], TH: ['align', 'colspan', 'rowspan'], TD: ['align', 'colspan', 'rowspan'], CODE: ['class'], OL: ['start'], INPUT: ['type', 'checked', 'disabled'] };

function safeHref(v) {
  const s = v.trim();
  return /^(https?:|mailto:|#|\/|\.\/|\.\.\/|[^:]*$)/i.test(s) && !/^\s*javascript:/i.test(s);
}

function sanitizeNode(node) {
  for (const child of [...node.childNodes]) {
    if (child.nodeType === Node.TEXT_NODE) continue;
    if (child.nodeType !== Node.ELEMENT_NODE) { child.remove(); continue; }
    const tag = child.tagName;
    if (DROP_WITH_CONTENT.has(tag)) { child.remove(); continue; }
    sanitizeNode(child);
    if (!ALLOWED.has(tag)) { child.replaceWith(...child.childNodes); continue; }
    const keep = ALLOWED_ATTRS[tag] || [];
    for (const attr of [...child.attributes]) {
      const name = attr.name.toLowerCase();
      if (!keep.includes(name) || attr.value.includes(PH)) { child.removeAttribute(attr.name); continue; }
      if (name === 'href' && !safeHref(attr.value)) child.removeAttribute(attr.name);
      if (name === 'class' && !/^language-[\w-]+$/.test(attr.value)) child.removeAttribute(attr.name);
    }
    if (tag === 'INPUT' && child.getAttribute('type') !== 'checkbox') { child.remove(); continue; }
    if (tag === 'INPUT') child.setAttribute('disabled', '');
    if (tag === 'A' && child.getAttribute('href')) {
      child.setAttribute('rel', 'noopener noreferrer');
      if (/^https?:/i.test(child.getAttribute('href'))) child.setAttribute('target', '_blank');
    }
  }
}

export function sanitizeHtml(html) {
  const doc = new DOMParser().parseFromString(`<body>${html}`, 'text/html'); // inert: scripts never run
  sanitizeNode(doc.body);
  return doc.body.innerHTML;
}

// ---- public API ------------------------------------------------------------

/** Markdown (+ KaTeX math) -> sanitised HTML string. Cached by input text. */
export function renderMarkdown(text) {
  const src = String(text ?? '');
  if (cache.has(src)) return cache.get(src);
  const { text: withPh, store } = extractMath(src);
  let html;
  if (window.marked && typeof window.marked.parse === 'function') {
    try {
      html = window.marked.parse(withPh, { gfm: true, breaks: true });
    } catch (e) {
      console.error('Markdown rendering failed', e);
      html = `<p>${escapeHtml(withPh)}</p>`;
    }
  } else {
    html = `<p style="white-space:pre-wrap">${escapeHtml(withPh)}</p>`; // library failed to load
  }
  html = sanitizeHtml(html).replace(PH_RE, (_, i) => store[Number(i)] ?? '');
  cache.set(src, html);
  return html;
}

const GREEK = 'alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|lambda|mu|nu|xi|pi|rho|sigma|tau|phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Sigma|Phi|Psi|Omega';
const GREEK_RE = new RegExp(`\\\\(${GREEK})(?![a-zA-Z])`, 'g');

/** Plain lowercase text for matching: LaTeX/Markdown markup removed, spaces collapsed. */
export function stripMarkup(text) {
  return String(text ?? '')
    .replace(GREEK_RE, ' $1 ')                 // keep \epsilon / \Sigma etc. searchable by name
    .replace(/\$+/g, ' ')                        // math delimiters
    .replace(/\\[a-zA-Z]+\*?/g, ' ')            // other LaTeX commands (\frac, \mathbb, \to ...)
    .replace(/\\./g, ' ')                        // \{ \} \, \; ...
    .replace(/[{}^_~*`|>#\\\[\]()=<+\-:;,.!?"']/g, ' ') // markdown / punctuation noise
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}
