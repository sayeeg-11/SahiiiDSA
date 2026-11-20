
import sys
from pathlib import Path
import csv

# Add the SahiiiDSA project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rag.embeddings import load_index

OUTPUT_FILE = PROJECT_ROOT / "evaluation" / "datasets" / "problem_catalog.csv"


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    db = load_index("problems")

    if db is None:
        raise RuntimeError("Problem FAISS index could not be loaded.")

    documents = list(db.docstore._dict.values())
    rows = []

    for doc in documents:
        if doc.metadata.get("_dummy"):
            continue

        metadata = doc.metadata

        rows.append({
            "problem_id": metadata.get("problem_id", ""),
            "title": metadata.get("title", ""),
            "difficulty": metadata.get("difficulty", ""),
            "topic_tags": ";".join(metadata.get("topic_tags", [])),
            "patterns": ";".join(metadata.get("patterns", [])),
            "content": doc.page_content.replace("\n", " "),
        })

    if not rows:
        raise RuntimeError("No problem documents found in the index.")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported problems: {len(rows)}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
