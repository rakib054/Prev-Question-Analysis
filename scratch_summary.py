import json
from pathlib import Path

dump = json.load(open("scratch_l1_l2_dump.json", encoding="utf-8"))
by_year = {}
for item in dump:
    q = item["q"]
    y = q["id"].split("-")[1]
    by_year.setdefault(y, []).append((q, item["lectures"]))

for y in sorted(by_year.keys(), reverse=True):
    print(f"\n=== YEAR {y} ({len(by_year[y])} questions) ===")
    for q, lects in by_year[y]:
        print(f"[{q['id']}] (Lects: {lects}, Marks: {q.get('marks')}, Type: {q.get('type')})")
        print(f"  Keywords: {q.get('keywords')}")
        print(f"  Figures: {[f.get('src') for f in q.get('figures', [])]}")
        text_preview = q.get('text', '').replace('\n', ' ')[:120]
        print(f"  Text: {text_preview}...")
