
from execution.runner import run_code

tests = [
    (
        "python",
        'n = int(input())\nprint(n * 2)',
        "21\n",
        "42",
    ),
    (
        "c",
        '#include <stdio.h>\nint main(void) { int n; scanf("%d", &n); printf("%d\\n", n * 2); return 0; }',
        "21\n",
        "42",
    ),
    (
        "cpp",
        '#include <iostream>\nusing namespace std;\nint main() { int n; cin >> n; cout << n * 2 << endl; return 0; }',
        "21\n",
        "42",
    ),
]

for language, code, stdin, expected in tests:
    result = run_code(language, code, stdin)
    passed = (
        result["status"] == "success"
        and result["stdout"].strip() == expected
    )

    print(f"\nLanguage: {language}")
    print(f"Status: {result['status']}")
    print(f"Output: {result['stdout'].strip()!r}")
    print(f"Duration: {result['duration_ms']} ms")
    print("PASS" if passed else f"FAIL: {result['stderr']}")
