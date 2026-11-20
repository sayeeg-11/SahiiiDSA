
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "evaluation" / "datasets" / "retrieval_test.csv"

# Each query will be evaluated against manually verified relevant problem IDs.
tests = [
    # Dynamic Programming
    ("Find problems involving one-dimensional dynamic programming", "dp_1d"),
    ("Find problems using the house robber pattern", "dp_1d"),
    ("Find problems involving optimization with dynamic programming", "dp_1d"),

    # Two Pointers
    ("Find problems that can be solved using two pointers", "two_pointers"),
    ("Find problems involving pairs in a sorted array", "two_pointers"),

    # Hashing
    ("Find problems involving hash maps and frequency counting", "hashing"),
    ("Find problems involving duplicate detection using hashing", "hashing"),

    # Sliding Window
    ("Find problems involving fixed-size sliding windows", "sliding_window"),
    ("Find problems involving variable-size sliding windows", "sliding_window"),

    # Binary Search
    ("Find problems that use binary search", "binary_search"),
    ("Find problems involving searching in a sorted array", "binary_search"),

    # Greedy
    ("Find problems that can be solved using a greedy strategy", "greedy"),
    ("Find problems involving locally optimal choices", "greedy"),

    # Graphs
    ("Find problems involving depth first search in graphs", "dfs"),
    ("Find problems involving breadth first search", "bfs"),

    # Backtracking
    ("Find problems involving recursive backtracking", "backtracking"),

    # Prefix Sum
    ("Find problems involving prefix sums and range calculations", "prefix_sum"),

    # Strings
    ("Find problems involving string matching", "string_matching"),
    ("Find problems involving character frequency in strings", "hashing"),

    # Other patterns
    ("Find problems involving bit manipulation", "bit_manipulation"),
    ("Find problems involving linked lists", "linked_list"),
    ("Find problems involving mathematical calculations", "math"),
    ("Find problems involving simulation", "simulation"),
    ("Find problems involving divide and conquer", "divide_and_conquer"),

    # Unfiltered natural-language queries
    ("I want to practice array problems involving counting and frequency", ""),
    ("Show me problems where I need to find an optimal subarray", ""),
    ("I want problems involving graph traversal", ""),
    ("Find problems involving recursion and exploring possible choices", ""),
    ("Show me problems involving searching and sorting", ""),
    ("Find problems that involve optimizing an array operation", ""),
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "query",
            "filter_tags",
            "filter_patterns",
            "relevant_problem_ids",
        ],
    )
    writer.writeheader()

    for query, pattern in tests:
        writer.writerow({
            "query": query,
            "filter_tags": "",
            "filter_patterns": pattern,
            "relevant_problem_ids": "",
        })

print(f"Created {len(tests)} retrieval test queries.")
print(f"Saved to: {OUTPUT}")
print("Relevant problem IDs must now be manually labelled.")
