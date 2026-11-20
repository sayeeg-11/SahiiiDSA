
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

catalog_path = ROOT / "evaluation/datasets/problem_catalog.csv"
test_path = ROOT / "evaluation/datasets/retrieval_test.csv"
output_path = ROOT / "evaluation/datasets/relevance_candidates.csv"

catalog = pd.read_csv(catalog_path).fillna("")
tests = pd.read_csv(test_path).fillna("")

rows = []

for _, test in tests.iterrows():
    pattern = test["filter_patterns"].strip()
    query = test["query"]

    if pattern:
        candidates = catalog[
            catalog["patterns"].apply(
                lambda value: pattern in [
                    p.strip() for p in value.split(";")
                ]
            )
        ]
    else:
        candidates = catalog.iloc[0:0]

    for _, problem in candidates.iterrows():
        rows.append({
            "query": query,
            "problem_id": problem["problem_id"],
            "title": problem["title"],
            "difficulty": problem["difficulty"],
            "patterns": problem["patterns"],
            "relevant": ""
        })

result = pd.DataFrame(rows)
result.to_csv(output_path, index=False, encoding="utf-8-sig")

print("Candidate rows:", len(result))
print("Saved:", output_path)
print("Fill relevant with 1 (relevant) or 0 (not relevant).")
