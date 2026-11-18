import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_QUESTIONS = ROOT / "data" / "questions"

def update_year_solutions(year, solutions_dict):
    """
    solutions_dict: { qid: solution_markdown_string }
    Updates data/questions/toc-{year}.json with solutions.
    """
    file_path = DATA_QUESTIONS / f"toc-{year}.json"
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    updated_count = 0
    for q in data.get("questions", []):
        qid = q.get("id")
        if qid in solutions_dict:
            q["solution"] = solutions_dict[qid]
            updated_count += 1
            print(f"  [+] Added solution for {qid}")
    
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    
    print(f"Successfully updated {updated_count}/{len(solutions_dict)} solutions in toc-{year}.json")

if __name__ == "__main__":
    print("Helper module for applying solutions.")
