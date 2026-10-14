from execution.leetcode_runner import run_question_tests

solutions = {
    "python": """
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, value in enumerate(nums):
            complement = target - value
            if complement in seen:
                return [seen[complement], i]
            seen[value] = i
        return []
""",
    "cpp": """
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;
        for (int i = 0; i < (int)nums.size(); ++i) {
            int complement = target - nums[i];
            if (seen.count(complement)) {
                return {seen[complement], i};
            }
            seen[nums[i]] = i;
        }
        return {};
    }
};
""",
    "c": """
int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    int* result = malloc(2 * sizeof(int));

    for (int i = 0; i < numsSize; ++i) {
        for (int j = i + 1; j < numsSize; ++j) {
            if (nums[i] + nums[j] == target) {
                result[0] = i;
                result[1] = j;
                *returnSize = 2;
                return result;
            }
        }
    }

    free(result);
    *returnSize = 0;
    return NULL;
}
""",
}

failed = False

for language, source in solutions.items():
    for mode in ("samples", "submit"):
        result = run_question_tests("two-sum", language, source, mode)
        passed = result["status"] == "accepted"

        print(f"\n{language.upper()} | {mode.upper()}")
        print(result["message"])
        print("PASS" if passed else "FAIL")

        if not passed:
            failed = True
            for item in result["results"]:
                if not item["passed"]:
                    print(item)

if failed:
    raise SystemExit(1)

print("\nAll language and test-mode checks passed.")