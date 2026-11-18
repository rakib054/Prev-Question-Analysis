// Loads subjects/topics/questions and derives everything else (lectures per question, counts, years,
// repeat groups, search text). Nothing here knows about specific questions, years or keywords.
import { SUBJECTS_URL } from './config.js';
import { cmpQuestions, kwKey, withHash } from './util.js';
import { stripMarkup } from './render.js';

let subjectsPromise = null;
const datasets = new Map();

async function fetchJson(url) {
  const res = await fetch(url, { cache: 'no-cache' }); // always revalidate so edits show up on refresh
  if (!res.ok) throw new Error(`${url}: HTTP ${res.status}`);
  try {
    return await res.json();
  } catch (e) {
    throw new Error(`${url}: not valid JSON (${e.message})`);
  }
}

export function loadSubjects() {
  if (!subjectsPromise) subjectsPromise = fetchJson(SUBJECTS_URL);
  return subjectsPromise;
}

export function loadSubject(id) {
  if (!datasets.has(id)) datasets.set(id, build(id));
  return datasets.get(id);
}

async function build(id) {
  const subjects = await loadSubjects();
  const subject = subjects.find((s) => s.id === id);
  if (!subject) throw new Error(`Unknown subject "${id}"`);

  const [topicsData, qData] = await Promise.all([fetchJson(subject.topics_file), fetchJson(subject.questions_file)]);

  // ---- lectures & keywords -------------------------------------------------
  const lectures = (topicsData.lectures || [])
    .map((l) => ({
      lecture: l.lecture,
      title: l.title,
      topics: (l.topics || []).map((t) => ({ keyword: withHash(t.keyword), name: t.name || t.keyword })),
      questions: [],
    }))
    .sort((a, b) => a.lecture - b.lecture);
  const lectureByNo = new Map(lectures.map((l) => [String(l.lecture), l]));

  /** key -> { keyword, name, lectures:[numbers], known:true, questions:[] } */
  const kwInfo = new Map();
  for (const lec of lectures) {
    for (const t of lec.topics) {
      const k = kwKey(t.keyword);
      let info = kwInfo.get(k);
      if (!info) {
        info = { key: k, keyword: t.keyword, name: t.name, lectures: [], known: true, questions: [] };
        kwInfo.set(k, info);
      }
      if (!info.lectures.includes(lec.lecture)) info.lectures.push(lec.lecture);
    }
  }

  // ---- exams & questions ---------------------------------------------------
  const exams = new Map((qData.exams || []).map((e) => [e.id, e]));
  const questions = [];
  const unknown = new Map(); // keyword -> [question ids]

  (qData.questions || []).forEach((raw, i) => {
    const exam = exams.get(raw.exam_id) || {};
    if (!exams.has(raw.exam_id)) console.warn(`Question "${raw.id}" refers to unknown exam_id "${raw.exam_id}"`);
    const q = {
      ...raw,
      _order: i,
      exam,
      year: Number(exam.year) || 0,
      part: String(raw.part ?? '').replace(/[()]/g, '').trim() || null,
      figures: Array.isArray(raw.figures) ? raw.figures : [],
      type: raw.type || 'other',
      repeat_group: raw.repeat_group || null,
      needs_review: !!raw.needs_review,
      solution: typeof raw.solution === 'string' ? raw.solution : '',
    };

    // keywords: canonicalise against the topics file, keep unknown ones visible
    q.kw = [];
    const seen = new Set();
    for (const rawKw of raw.keywords || []) {
      const k = kwKey(rawKw);
      if (!k || seen.has(k)) continue;
      seen.add(k);
      let info = kwInfo.get(k);
      if (!info) {
        info = { key: k, keyword: withHash(rawKw), name: withHash(rawKw), lectures: [], known: false, questions: [] };
        kwInfo.set(k, info);
        unknown.set(info.keyword, []);
      }
      if (!info.known) unknown.get(info.keyword).push(q.id);
      info.questions.push(q);
      q.kw.push(info);
    }

    // lectures this question belongs to = union over its keywords
    q.lectures = [...new Set(q.kw.flatMap((info) => info.lectures))].sort((a, b) => a - b);
    for (const n of q.lectures) lectureByNo.get(String(n)).questions.push(q);

    // search fields (built once from the data)
    q._search = {
      kw: q.kw.map((info) => info.key),
      topic: q.kw.filter((info) => info.known).map((info) => info.name.toLowerCase()),
      text: stripMarkup(q.text),
      alt: q.figures.map((f) => String(f.alt || '').toLowerCase()).join(' '),
    };
    questions.push(q);
  });

  for (const [kw, ids] of unknown) {
    console.warn(`Keyword ${kw} is not in ${subject.topics_file} (used by ${ids.join(', ')}). It is still shown on the questions.`);
  }

  // ---- repeat groups -------------------------------------------------------
  const groups = new Map();
  for (const q of questions) {
    if (!q.repeat_group) continue;
    if (!groups.has(q.repeat_group)) groups.set(q.repeat_group, []);
    groups.get(q.repeat_group).push(q);
  }
  for (const q of questions) {
    const g = q.repeat_group ? groups.get(q.repeat_group) : null;
    q.repeat = g && g.length > 1 ? { count: g.length, years: [...new Set(g.map((x) => x.year))].sort((a, b) => a - b) } : null;
  }

  questions.sort(cmpQuestions);
  for (const l of lectures) l.questions.sort(cmpQuestions);
  const years = [...new Set(questions.map((q) => q.year))].sort((a, b) => b - a);

  return {
    subject,
    id: subject.id,
    exams,
    lectures,
    lectureByNo,
    kwInfo,
    questions,
    years,
    yearRange: years.length ? [years[years.length - 1], years[0]] : null,
    unknownKeywords: [...unknown.keys()],
  };
}
