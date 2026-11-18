// Site-wide settings. Nothing about questions, years, lectures or keywords lives here.

/** Show the small "⚠ unverified" badge on questions with needs_review: true. */
export const SHOW_REVIEW_FLAGS = true;

/** Delay (ms) before live search runs / suggestions appear while typing. */
export const SEARCH_DEBOUNCE_MS = 200;

/** Path of the subject list, relative to index.html. */
export const SUBJECTS_URL = 'data/subjects.json';

/** localStorage key prefix. */
export const STORAGE_PREFIX = 'qbank:';

/** Question cards rendered per batch (the rest load on "Show more" / scroll). */
export const PAGE_SIZE = 20;
