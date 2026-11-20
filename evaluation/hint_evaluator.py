
import sys
import time
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from prompts.hints import get_hint_prompt
from utils.llm import invoke_llm, get_llm_name


DATASET = ROOT / "evaluation" / "datasets" / "hint_test.csv"
RESULTS = ROOT / "evaluation" / "results"

TEMPERATURE = 0.3


def generate_hints(provider, model):
    RESULTS.mkdir(parents=True, exist_ok=True)

    tests = pd.read_csv(DATASET)
    records = []

    for _, test in tests.iterrows():
        print(f"\nTesting: {test['problem_title']}")

        problem = (
            f"Problem: {test['problem_title']}\n"
            f"Difficulty: {test['difficulty']}\n"
            f"Description: {test['description']}"
        )

        for tier in range(1, 6):
            print(f"  Generating Tier {tier}...")

            prompt = get_hint_prompt(
                tier=tier,
                problem=problem,
                user_message=test["user_message"]
            )

            start = time.perf_counter()

            try:
                response = invoke_llm(
                    prompt,
                    temperature=TEMPERATURE,
                    provider=provider,
                    model=model
                )

                elapsed = time.perf_counter() - start

                records.append({
                    "problem_id": test["problem_id"],
                    "problem_title": test["problem_title"],
                    "difficulty": test["difficulty"],
                    "hint_tier": tier,
                    "hint_type": [
                        "Pattern Nudge",
                        "Approach Direction",
                        "Detailed Strategy",
                        "Implementation Guide",
                        "Full Solution Walkthrough"
                    ][tier - 1],
                    "generated_hint": response,
                    "response_time_seconds": round(elapsed, 3),
                    "provider": provider,
                    "model": model,
                    "temperature": TEMPERATURE,
                })

                print(f"  Completed in {elapsed:.2f}s")

            except Exception as error:
                print(f"  Failed: {error}")

                records.append({
                    "problem_id": test["problem_id"],
                    "problem_title": test["problem_title"],
                    "difficulty": test["difficulty"],
                    "hint_tier": tier,
                    "hint_type": f"Tier {tier}",
                    "generated_hint": "",
                    "response_time_seconds": None,
                    "provider": provider,
                    "model": model,
                    "temperature": TEMPERATURE,
                    "error": str(error)
                })

    output = pd.DataFrame(records)

    output.to_csv(
        RESULTS / "hint_evaluation.csv",
        index=False
    )

    # Separate human evaluation sheet
    scores = output[[
        "problem_id",
        "problem_title",
        "difficulty",
        "hint_tier",
        "hint_type",
        "generated_hint"
    ]].copy()

    criteria = [
        "relevance",
        "correctness",
        "progressiveness",
        "disclosure_control",
        "clarity",
        "non_repetition"
    ]

    for criterion in criteria:
        scores[criterion] = ""

    scores["total_score"] = ""
    scores["reviewer_comments"] = ""

    scores.to_csv(
        RESULTS / "hint_scores.csv",
        index=False
    )

    print("\nEvaluation generation completed.")
    print(f"Generated responses: {len(records)}")
    print(f"Results saved in: {RESULTS}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--provider",
        default="ollama",
        choices=["ollama", "gemini"]
    )

    parser.add_argument("--model", default=None)

    args = parser.parse_args()

    print("Provider:", args.provider)
    print("Model:", get_llm_name(args.provider, args.model))

    generate_hints(args.provider, args.model)


if __name__ == "__main__":
    main()
