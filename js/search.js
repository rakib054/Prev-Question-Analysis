// Search over the loaded dataset. The index is derived from the data at load time (see data.js).
//
// Rules
//  * case-insensitive; a leading '#' is ignored; several words must ALL match (somewhere)
//  * a word matches keywords (substring), topic names, question text (LaTeX stripped) and figure alt text
//  * ranking: keyword match > topic-name match > text match > figure alt match
//  * if the query is exactly one keyword and no other keyword contains it (e.g. #CFGtoPDA), only questions
//    tagged with that keyword are returned; otherwise (e.g. "cfg") every keyword containing it matches
//    and the "Matching keywords" chips let the user narrow to one.
//  * `exactKw` (set by clicking a chip) always restricts to that keyword.
import { cmpQuestions, kwKey } from './util.js';

export function tokenize(query) {
  return String(query ?? '').toLowerCase().split(/\s+/).map((t) => t.replace(/^#+/, '')).filter(Boolean);
}

/** Keyword infos whose keyword or topic name contains every token. */
export function matchingKeywords(ds, query) {
  const tokens = tokenize(query);
  if (!tokens.length) return [];
  const out = [];
  for (const info of ds.kwInfo.values()) {
    const name = info.name.toLowerCase();
    if (tokens.every((t) => info.key.includes(t) || name.includes(t))) out.push(info);
  }
  out.sort((a, b) => {
    const ea = tokens.length === 1 && a.key === tokens[0] ? 0 : 1;
    const eb = tokens.length === 1 && b.key === tokens[0] ? 0 : 1;
    return ea - eb || b.questions.length - a.questions.length || a.key.localeCompare(b.key);
  });
  return out;
}

/** The single keyword a query refers to unambiguously, or null. */
export function exactKeyword(ds, query) {
  const tokens = tokenize(query);
  if (tokens.length !== 1) return null;
  const t = tokens[0];
  const info = ds.kwInfo.get(t);
  if (!info) return null;
  for (const other of ds.kwInfo.values()) {
    if (other !== info && other.key.includes(t)) return null;
  }
  return info;
}

/**
 * @returns {{results: object[], keywords: object[], exact: object|null, tokens: string[]}}
 */
export function search(ds, query, { exactKw = null } = {}) {
  const tokens = tokenize(query);
  const keywords = matchingKeywords(ds, query);
  const forced = exactKw ? ds.kwInfo.get(kwKey(exactKw)) || null : null;
  const exact = forced || exactKeyword(ds, query);

  if (!tokens.length && !forced) return { results: [], keywords, exact: null, tokens };

  const scored = [];
  for (const q of ds.questions) {
    if (exact && !q.kw.includes(exact)) continue;
    let score = 0;
    let ok = true;
    for (const t of tokens) {
      const s = q._search;
      const kwHit = s.kw.some((k) => k.includes(t));
      const exactHit = s.kw.some((k) => k === t);
      const topicHit = s.topic.some((n) => n.includes(t));
      const textHit = s.text.includes(t);
      const altHit = s.alt.includes(t);
      if (!(kwHit || topicHit || textHit || altHit)) { ok = false; break; }
      score += (kwHit ? 100 : 0) + (exactHit ? 50 : 0) + (topicHit ? 60 : 0) + (textHit ? 30 : 0) + (altHit ? 15 : 0);
    }
    if (ok) scored.push({ q, score });
  }
  scored.sort((a, b) => b.score - a.score || cmpQuestions(a.q, b.q));
  return { results: scored.map((x) => x.q), keywords, exact, tokens };
}

/** Keywords by number of questions, for "try searching…" hints. */
export function popularKeywords(ds, n = 10) {
  return [...ds.kwInfo.values()].filter((i) => i.questions.length).sort((a, b) => b.questions.length - a.questions.length || a.key.localeCompare(b.key)).slice(0, n);
}
