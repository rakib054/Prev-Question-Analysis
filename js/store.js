// "Solved", "Favorites" and "Solution" state, stored per subject in localStorage. Fails quietly if storage is blocked.
import { STORAGE_PREFIX } from './config.js';

const memory = new Map(); // fallback when localStorage is unavailable
const listeners = new Set();

const favMemory = new Map();
const favListeners = new Set();

const solMemory = new Map();
const solListeners = new Set();

function key(subjectId) {
  return `${STORAGE_PREFIX}solved:${subjectId}`;
}

function favKey(subjectId) {
  return `${STORAGE_PREFIX}favorites:${subjectId}`;
}

function solKey(subjectId) {
  return `${STORAGE_PREFIX}solutions:${subjectId}`;
}

function load(subjectId) {
  if (memory.has(subjectId)) return memory.get(subjectId);
  let set = new Set();
  try {
    const raw = localStorage.getItem(key(subjectId));
    if (raw) set = new Set(JSON.parse(raw));
  } catch (e) { /* storage blocked or corrupt: start empty */ }
  memory.set(subjectId, set);
  return set;
}

export function isSolved(subjectId, qid) {
  return load(subjectId).has(qid);
}

export function solvedCount(subjectId, ids) {
  const s = load(subjectId);
  let n = 0;
  for (const id of ids) if (s.has(id)) n++;
  return n;
}

export function setSolved(subjectId, qid, value) {
  const set = load(subjectId);
  if (value) set.add(qid); else set.delete(qid);
  try {
    localStorage.setItem(key(subjectId), JSON.stringify([...set]));
  } catch (e) { /* ignore */ }
  listeners.forEach((fn) => fn(subjectId, qid, value));
}

export function onSolvedChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

// ---- Solutions -------------------------------------------------------------

function loadSolutions(subjectId) {
  if (solMemory.has(subjectId)) return solMemory.get(subjectId);
  let dict = {};
  try {
    const raw = localStorage.getItem(solKey(subjectId));
    if (raw) dict = JSON.parse(raw) || {};
  } catch (e) { /* ignore */ }
  solMemory.set(subjectId, dict);
  return dict;
}

export function getSolution(subjectId, q) {
  const dict = loadSolutions(subjectId);
  const qid = typeof q === 'string' ? q : (q?.id || '');
  if (qid && qid in dict) return dict[qid];
  if (typeof q === 'object' && q?.solution) return q.solution;
  return '';
}

export function hasSolution(subjectId, q) {
  const sol = getSolution(subjectId, q);
  return !!(sol && String(sol).trim().length > 0);
}

export function setSolution(subjectId, qid, text) {
  const dict = loadSolutions(subjectId);
  const val = String(text ?? '').trim();
  if (val) {
    dict[qid] = String(text);
  } else {
    delete dict[qid];
  }
  try {
    localStorage.setItem(solKey(subjectId), JSON.stringify(dict));
  } catch (e) { /* ignore */ }
  solListeners.forEach((fn) => fn(subjectId, qid, val));
}

export function deleteSolution(subjectId, qid) {
  setSolution(subjectId, qid, '');
}

export function onSolutionChange(fn) {
  solListeners.add(fn);
  return () => solListeners.delete(fn);
}

export function solutionCount(subjectId, questions) {
  let count = 0;
  for (const q of questions) {
    if (hasSolution(subjectId, q)) count++;
  }
  return count;
}

// ---- Favorites / Saved Questions -------------------------------------------

function loadFavorites(subjectId) {
  if (favMemory.has(subjectId)) return favMemory.get(subjectId);
  let set = new Set();
  try {
    const raw = localStorage.getItem(favKey(subjectId));
    if (raw) set = new Set(JSON.parse(raw));
  } catch (e) { /* ignore */ }
  favMemory.set(subjectId, set);
  return set;
}

export function isFavorite(subjectId, qid) {
  return loadFavorites(subjectId).has(qid);
}

export function setFavorite(subjectId, qid, value) {
  const set = loadFavorites(subjectId);
  if (value) set.add(qid); else set.delete(qid);
  try {
    localStorage.setItem(favKey(subjectId), JSON.stringify([...set]));
  } catch (e) { /* ignore */ }
  favListeners.forEach((fn) => fn(subjectId, qid, value));
}

export function toggleFavorite(subjectId, qid) {
  const current = isFavorite(subjectId, qid);
  setFavorite(subjectId, qid, !current);
  return !current;
}

export function favoriteCount(subjectId, questionsOrIds) {
  const set = loadFavorites(subjectId);
  if (!questionsOrIds) return set.size;
  let count = 0;
  for (const item of questionsOrIds) {
    const id = typeof item === 'string' ? item : item.id;
    if (set.has(id)) count++;
  }
  return count;
}

export function onFavoriteChange(fn) {
  favListeners.add(fn);
  return () => favListeners.delete(fn);
}

export function getFavoriteIds(subjectId) {
  return [...loadFavorites(subjectId)];
}


