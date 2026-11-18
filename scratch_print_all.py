import json

dump = json.load(open("scratch_l1_l2_dump.json", encoding="utf-8"))
for item in dump:
    q = item["q"]
    print("=" * 80)
    print(f"ID: {q['id']} | Year: {q['id'].split('-')[1]} | Marks: {q.get('marks')} | Type: {q.get('type')}")
    print(f"Keywords: {q.get('keywords')}")
    print(f"Lectures: {item['lectures']}")
    if q.get('figures'):
        print(f"Figures: {json.dumps(q.get('figures'))}")
    print("-" * 80)
    print(q.get('text'))
    print()
