import json
from pathlib import Path
from collections import defaultdict

root = Path(r"c:\Users\User\MR.RAKIB\Big Projects\Prev Years Question Analysis")
topics = json.load(open(root / "data/topics/toc.json", encoding="utf-8"))
kw_to_lectures = defaultdict(set)
for lec in topics["lectures"]:
    lno = lec["lecture"]
    for t in lec.get("topics", []):
        kw_to_lectures[t["keyword"].lower()].add(lno)

data = json.load(open(root / "data/questions/toc.json", encoding="utf-8"))
questions = data["questions"]

l1_l2_questions = []

for q in questions:
    lects = set()
    for kw in q.get("keywords") or []:
        k = kw.strip()
        if not k.startswith("#"):
            k = "#" + k
        if k.lower() in kw_to_lectures:
            lects |= kw_to_lectures[k.lower()]
    if 1 in lects or 2 in lects:
        l1_l2_questions.append((q, sorted(lects)))

print(f"Total count: {len(l1_l2_questions)}")
with open(root / "scratch_l1_l2_dump.json", "w", encoding="utf-8") as f:
    json.dump([{"q": q, "lectures": lects} for q, lects in l1_l2_questions], f, indent=2, ensure_ascii=False)
print("Dumped to scratch_l1_l2_dump.json")
