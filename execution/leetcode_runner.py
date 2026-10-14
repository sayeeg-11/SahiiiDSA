"""Local LeetCode-style test harnesses for configured problems.

Development use only. Submitted code is NOT sandboxed.
"""

from execution.question_bank import QUESTION_TESTS
from execution.runner import run_code


def _normalise_output(output):
    """Compare comma-separated integer results independent of ordering."""
    text = output.strip()
    if not text:
        return ""

    try:
        values = [int(part.strip()) for part in text.split(",")]
        return ",".join(str(value) for value in sorted(values))
    except ValueError:
        return text



def _build_python(source, case):
    nums = repr(case["nums"])
    target = case["target"]

    harness = f"""

_nums = {nums}
_target = {target}

try:
    _result = Solution().twoSum(_nums, _target)
    if _result is None:
        print("ERROR: Solution.twoSum returned None")
    elif not isinstance(_result, (list, tuple)):
        print("ERROR: Solution.twoSum must return a list of indices")
    else:
        print(",".join(str(x) for x in sorted(_result)))
except Exception as exc:
    print(f"ERROR: {{type(exc).__name__}}: {{exc}}")
"""
    return "from typing import List\n" + source + harness


def _build_cpp(source, case):
    nums = ", ".join(str(x) for x in case["nums"])
    target = case["target"]

    harness = f"""

int main() {{
    vector<int> nums = {{{nums}}};
    int target = {target};
    Solution solution;
    vector<int> result = solution.twoSum(nums, target);
    sort(result.begin(), result.end());

    for (size_t i = 0; i < result.size(); ++i) {{
        if (i) cout << ",";
        cout << result[i];
    }}
    cout << endl;
    return 0;
}}
"""
    return "#include <bits/stdc++.h>\nusing namespace std;\n" + source + harness


def _build_c(source, case):
    nums = ", ".join(str(x) for x in case["nums"])
    nums_size = len(case["nums"])
    target = case["target"]

    harness = f"""

int main(void) {{
    int nums[] = {{{nums}}};
    int returnSize = 0;
    int* result = twoSum(nums, {nums_size}, {target}, &returnSize);

    if (result == NULL || returnSize <= 0) {{
        free(result);
        return 2;
    }}

    for (int i = 0; i < returnSize; ++i) {{
        for (int j = i + 1; j < returnSize; ++j) {{
            if (result[j] < result[i]) {{
                int temp = result[i];
                result[i] = result[j];
                result[j] = temp;
            }}
        }}
    }}

    for (int i = 0; i < returnSize; ++i) {{
        if (i) printf(",");
        printf("%d", result[i]);
    }}
    printf("\\n");
    free(result);
    return 0;
}}
"""
    return "#include <stdio.h>\n#include <stdlib.h>\n" + source + harness


_BUILDERS = {
    "python": _build_python,
    "cpp": _build_cpp,
    "c": _build_c,
}


def run_question_tests(slug, language, source_code, mode="samples"):
    """Run configured tests and return per-case results."""
    language = language.strip().lower()
    mode = mode.strip().lower()

    if language not in _BUILDERS:
        return {
            "status": "error",
            "message": f"Unsupported language: {language}",
            "results": [],
        }

    question = QUESTION_TESTS.get(slug)
    if not question:
        return {
            "status": "unsupported",
            "message": "Automated tests are not configured for this problem yet.",
            "results": [],
        }

    if mode not in ("samples", "submit"):
        return {
            "status": "error",
            "message": "Unknown test mode.",
            "results": [],
        }

    if not source_code.strip():
        return {
            "status": "error",
            "message": "Please enter your solution first.",
            "results": [],
        }

    cases = question[mode]
    results = []

    for index, case in enumerate(cases, start=1):
        full_source = _BUILDERS[language](source_code, case)
        execution = run_code(language, full_source)

        item = {
            "case": index,
            "status": execution["status"],
            "passed": False,
            "expected": ",".join(map(str, case["expected"])),
            "actual": execution["stdout"].strip(),
            "stderr": execution["stderr"],
            "duration_ms": execution["duration_ms"],
        }

        if execution["status"] == "success":
            item["passed"] = (
                _normalise_output(execution["stdout"])
                == _normalise_output(item["expected"])
            )
            item["status"] = "passed" if item["passed"] else "wrong_answer"

        results.append(item)

        # Stop after a compilation/runtime failure.
        if execution["status"] != "success":
            break

    all_passed = len(results) == len(cases) and all(
        item["passed"] for item in results
    )

    return {
        "status": "accepted" if all_passed else "not_accepted",
        "message": f"{sum(item['passed'] for item in results)}/{len(cases)} tests passed.",
        "results": results,
    }