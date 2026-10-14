"""Structured test cases for supported LeetCode-style problems."""

QUESTION_TESTS = {
    "two-sum": {
        "title": "Two Sum",
        "method": "twoSum",
        "samples": [
            {"nums": [2, 7, 11, 15], "target": 9, "expected": [0, 1]},
            {"nums": [3, 2, 4], "target": 6, "expected": [1, 2]},
            {"nums": [3, 3], "target": 6, "expected": [0, 1]},
        ],
        "submit": [
            {"nums": [1, 5, 3, 7], "target": 8, "expected": [1, 2]},
            {"nums": [-3, 4, 3, 90], "target": 0, "expected": [0, 2]},
            {"nums": [0, 4, 3, 0], "target": 0, "expected": [0, 3]},
        ],
        "starter_code": {
            "python": (
                "from typing import List\n\n"
                "class Solution:\n"
                "    def twoSum(self, nums: List[int], target: int) -> List[int]:\n"
                "        # Write your solution here\n"
                "        pass\n"
            ),
            "cpp": (
                "#include <bits/stdc++.h>\n"
                "using namespace std;\n\n"
                "class Solution {\n"
                "public:\n"
                "    vector<int> twoSum(vector<int>& nums, int target) {\n"
                "        // Write your solution here\n"
                "        return {};\n"
                "    }\n"
                "};\n"
            ),
            "c": (
                "#include <stdlib.h>\n\n"
                "int* twoSum(int* nums, int numsSize, int target, int* returnSize) {\n"
                "    // Write your solution here\n"
                "    *returnSize = 0;\n"
                "    return NULL;\n"
                "}\n"
            ),
        },
    },
}