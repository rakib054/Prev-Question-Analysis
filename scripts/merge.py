#!/usr/bin/env python3
"""Merge per-year question files into the single file the website reads.

Usage:
    python scripts/merge.py            # subject "toc"
    python scripts/merge.py <subject>  # any other subject id from data/subjects.json

What it does (Python standard library only):
  1. Reads data/questions/<id>-<YYYY>.json and writes data/questions/<id>.json
     (exams sorted newest first, all questions). Fails on duplicate ids or a
     missing "exam" block.
  2. For subject "toc": makes sure data/topics/toc.json has Lecture 9
     ("Undecidability & Complexity (not covered in slides)") with its topics.
  3. Checks keywords and figure files, checks that marks add up per question
     number, and prints a summary. Problems that do not break the site are
     reported as warnings; real data errors exit with status 1.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# ---- Lecture 9 (only applied to the "toc" subject) -------------------------
LECTURE9_NUMBER = 9
LECTURE9_TITLE = "Undecidability & Complexity (not covered in slides)"
LECTURE9_TOPICS = [
    ("#HaltingProblem", "Halting Problem"),
    ("#Undecidability", "Undecidability"),
    ("#PCP", "Post's Correspondence Problem"),
    ("#NPHardNPComplete", "NP-Hard & NP-Complete"),
    ("#Reduction", "Reduction"),
    ("#SAT", "Satisfiability (SAT, Clique, Circuit-SAT)"),
    ("#TractableIntractable", "Tractable vs Intractable Problems"),
    ("#RecursiveVsRE", "Recursive vs Recursively Enumerable Languages"),
    ("#UnrestrictedGrammar", "Unrestricted Grammar"),
    ("#TwoWayInfiniteTape", "TM with Two-way Infinite Tape"),
]

# Marks expected per question number (per exam year). Default 35; 2020 uses 30.
DEFAULT_MARKS_PER_QNO = 35
MARKS_PER_QNO_BY_YEAR = {2020: 30}

errors = []
warnings = []


def err(msg):
    errors.append(msg)
    print(f"  ERROR: {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"  warning: {msg}")


def read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        err(f"{path.relative_to(ROOT)}: invalid JSON ({e})")
    except OSError as e:
        err(f"cannot read {path}: {e}")
    return None


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def part_clean(p):
    return (p or "").strip().strip("()").lower()


def ensure_lecture9(topics_path):
    """Add Lecture 9 / its topics to the topics file if missing."""
    topics = read_json(topics_path)
    if topics is None:
        return None
    lectures = topics.setdefault("lectures", [])
    changed = False
    lec = next((l for l in lectures if l.get("lecture") == LECTURE9_NUMBER), None)
    if lec is None:
        lec = {"lecture": LECTURE9_NUMBER, "title": LECTURE9_TITLE, "topics": []}
        lectures.append(lec)
        lectures.sort(key=lambda l: l.get("lecture", 0))
        changed = True
        print(f"  added Lecture {LECTURE9_NUMBER}: {LECTURE9_TITLE}")
    elif lec.get("title") != LECTURE9_TITLE:
        print(f"  note: Lecture 9 already exists with title {lec.get('title')!r}; title left unchanged")
    have = {t["keyword"].lower() for t in lec.setdefault("topics", [])}
    elsewhere = {}
    for l in lectures:
        if l is not lec:
            for t in l.get("topics", []):
                elsewhere[t["keyword"].lower()] = l.get("lecture")
    for kw, name in LECTURE9_TOPICS:
        if kw.lower() in have:
            continue
        lec["topics"].append({"keyword": kw, "name": name})
        changed = True
        print(f"  added topic {kw} to Lecture 9")
        if kw.lower() in elsewhere:
            warn(f"{kw} is also a topic of lecture {elsewhere[kw.lower()]}; questions with it will show in both lectures")
    if changed:
        write_json(topics_path, topics)
    else:
        print("  Lecture 9 already complete")
    return topics


def main():
    subject_id = sys.argv[1] if len(sys.argv) > 1 else "toc"
    qdir = DATA / "questions"

    # Locate topics file (from subjects.json when possible)
    topics_path = DATA / "topics" / f"{subject_id}.json"
    subjects = read_json(DATA / "subjects.json") if (DATA / "subjects.json").exists() else None
    if isinstance(subjects, list):
        entry = next((s for s in subjects if s.get("id") == subject_id), None)
        if entry is None:
            warn(f'subject "{subject_id}" is not listed in data/subjects.json')
        elif entry.get("topics_file"):
            topics_path = ROOT / entry["topics_file"]

    print(f"Merging subject '{subject_id}'")
    pattern = re.compile(rf"^{re.escape(subject_id)}-(\d{{4}})\.json$")
    files = sorted(p for p in qdir.glob(f"{subject_id}-*.json") if pattern.match(p.name))
    if not files:
        err(f"no files named {subject_id}-<year>.json in {qdir.relative_to(ROOT)}")
        return finish()

    exams, questions, seen_ids, seen_exam_ids = [], [], {}, {}
    for path in files:
        rel = path.relative_to(ROOT)
        data = read_json(path)
        if data is None:
            continue
        exam = data.get("exam")
        if not isinstance(exam, dict) or not exam.get("id"):
            err(f'{rel}: missing "exam" block (or it has no "id")')
            continue
        file_year = int(pattern.match(path.name).group(1))
        if exam.get("year") != file_year:
            warn(f'{rel}: exam.year is {exam.get("year")!r} but the file name says {file_year}')
        if exam["id"] in seen_exam_ids:
            err(f'{rel}: exam id "{exam["id"]}" already used in {seen_exam_ids[exam["id"]]}')
            continue
        seen_exam_ids[exam["id"]] = rel
        if data.get("subject") not in (None, subject_id):
            warn(f'{rel}: "subject" is {data.get("subject")!r}, expected "{subject_id}"')
        exams.append(exam)
        for i, q in enumerate(data.get("questions", [])):
            qid = q.get("id")
            if not qid:
                err(f"{rel}: question #{i + 1} has no id")
                continue
            if qid in seen_ids:
                err(f'duplicate question id "{qid}" ({rel} and {seen_ids[qid]})')
                continue
            seen_ids[qid] = rel
            if "exam_id" not in q:
                q["exam_id"] = exam["id"]
            elif q["exam_id"] != exam["id"]:
                err(f'{rel}: question "{qid}" has exam_id "{q["exam_id"]}" but the file\'s exam is "{exam["id"]}"')
                continue
            for field in ("qno", "text"):
                if q.get(field) in (None, ""):
                    warn(f'{rel}: question "{qid}" has no "{field}"')
            questions.append(q)

    if errors:
        return finish()

    exams.sort(key=lambda e: (-int(e.get("year", 0)), str(e.get("id"))))
    year_of = {e["id"]: int(e.get("year", 0)) for e in exams}
    questions = [q for _, q in sorted(enumerate(questions), key=lambda p: (-year_of[p[1]["exam_id"]], p[0]))]

    out_path = qdir / f"{subject_id}.json"
    write_json(out_path, {"subject": subject_id, "exams": exams, "questions": questions})
    print(f"  wrote {out_path.relative_to(ROOT)}: {len(exams)} exams, {len(questions)} questions")

    # ---- topics ----------------------------------------------------------
    topics = None
    if subject_id == "toc":
        print("Topics: checking Lecture 9")
        topics = ensure_lecture9(topics_path)
    elif topics_path.exists():
        topics = read_json(topics_path)
    else:
        warn(f"topics file {topics_path.relative_to(ROOT)} not found; keyword checks skipped")

    # ---- checks ----------------------------------------------------------
    print("Checks")
    kw_to_lectures = defaultdict(set)
    lecture_titles = {}
    if topics:
        for lec in topics.get("lectures", []):
            lecture_titles[lec["lecture"]] = lec.get("title", "")
            for t in lec.get("topics", []):
                kw_to_lectures[t["keyword"].lower()].add(lec["lecture"])

    per_lecture = Counter()
    unassigned = 0
    unknown_kw = defaultdict(list)
    for q in questions:
        lects = set()
        for kw in q.get("keywords") or []:
            k = kw.strip()
            if not k.startswith("#"):
                k = "#" + k
            if topics:
                if k.lower() in kw_to_lectures:
                    lects |= kw_to_lectures[k.lower()]
                else:
                    unknown_kw[kw].append(q["id"])
        for l in lects:
            per_lecture[l] += 1
        if topics and not lects:
            unassigned += 1
        if not (q.get("keywords") or []):
            warn(f'question "{q["id"]}" has no keywords')
        for fig in q.get("figures") or []:
            src = (fig.get("src") or "").lstrip("/")
            if not src or not (ROOT / src).is_file():
                warn(f'question "{q["id"]}": figure file not found: {fig.get("src")!r}')
            if not fig.get("alt"):
                warn(f'question "{q["id"]}": figure {fig.get("src")!r} has no alt text')
    for kw, ids in sorted(unknown_kw.items()):
        warn(f"keyword {kw} is not in the topics file (used by {', '.join(ids[:5])}{'...' if len(ids) > 5 else ''})")

    marks_by_qno = defaultdict(float)
    qno_year = {}
    for q in questions:
        key = (q["exam_id"], q.get("section"), q.get("qno"))
        marks_by_qno[key] += q.get("marks") or 0
        qno_year[key] = year_of[q["exam_id"]]
    for (exam_id, section, qno), total in sorted(marks_by_qno.items(), key=lambda kv: (-qno_year[kv[0]], str(kv[0][1]), str(kv[0][2]))):
        want = MARKS_PER_QNO_BY_YEAR.get(qno_year[(exam_id, section, qno)], DEFAULT_MARKS_PER_QNO)
        if abs(total - want) > 1e-9:
            warn(f"{exam_id} Q{qno}{' (section ' + str(section) + ')' if section else ''}: marks add up to {total:g}, expected {want:g}")

    # ---- summary ---------------------------------------------------------
    print("\nSummary")
    per_year = Counter(year_of[q["exam_id"]] for q in questions)
    print("  Questions per year: " + ", ".join(f"{y}: {per_year[y]}" for y in sorted(per_year, reverse=True)))
    if topics:
        print("  Questions per lecture (a question counts in every lecture it touches):")
        for n in sorted(lecture_titles):
            print(f"    L{n:<2} {per_lecture[n]:>3}  {lecture_titles[n]}")
        if unassigned:
            print(f"    (no lecture) {unassigned} question(s) have no keyword that belongs to a lecture")
    print(f"  Total: {len(questions)} questions in {len(exams)} exams; {len(warnings)} warning(s)")
    return finish()


def finish():
    if errors:
        print(f"\nFAILED with {len(errors)} error(s); nothing was written." if not any("wrote" in e for e in errors) else f"\nFAILED with {len(errors)} error(s).")
        return 1
    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
