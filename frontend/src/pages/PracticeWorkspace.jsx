
import { useEffect, useState } from "react";
import {
  BookOpen,
  Lightbulb,
  Tag,
  Play,
  Send,
  Loader2,
  Terminal,
} from "lucide-react";

import api from "../services/api";
import CodeEditor from "../components/CodeEditor";

// Starter code for the supported languages
const starterCode = {
  python: `class Solution:
    def twoSum(self, nums, target):
        # Write your solution here
        pass
`,
  cpp: `#include <vector>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // Write your solution here
        return {};
    }
};
`,
  c: `#include <stdlib.h>

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    // Write your solution here
    *returnSize = 0;
    return NULL;
}
`,
};

const languageOptions = [
  { value: "python", label: "Python" },
  { value: "cpp", label: "C++" },
  { value: "c", label: "C" },
];

function PracticeWorkspace({ problemId }) {
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [language, setLanguage] = useState("python");
  const [code, setCode] = useState(starterCode.python);
  const [stdin, setStdin] = useState("");
  const [executionResult, setExecutionResult] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [executionMode, setExecutionMode] = useState("");

  // Fetch selected problem
  useEffect(() => {
    const fetchProblem = async () => {
      try {
        setLoading(true);
        setError("");
        setProblem(null);

        const response = await api.get(`/api/questions/${problemId}`);
        setProblem(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail || "Failed to load problem details."
        );
      } finally {
        setLoading(false);
      }
    };

    if (problemId) {
      fetchProblem();
    } else {
      setLoading(false);
    }
  }, [problemId]);

  // Change language and starter code
  const handleLanguageChange = (event) => {
    const selectedLanguage = event.target.value;

    setLanguage(selectedLanguage);
    setCode(starterCode[selectedLanguage]);
    setExecutionResult(null);
  };

  // Run code with custom input
  const handleRun = async () => {
    try {
      setExecuting(true);
      setExecutionMode("run");
      setExecutionResult(null);

      const response = await api.post("/api/execute/run", {
        language,
        source_code: code,
        stdin,
      });

      setExecutionResult(response.data);
    } catch (err) {
      setExecutionResult({
        status: "error",
        message:
          err.response?.data?.detail || "Code execution failed.",
      });
    } finally {
      setExecuting(false);
      setExecutionMode("");
    }
  };

  // Submit code against configured problem test cases
  const handleSubmit = async () => {
    try {
      setExecuting(true);
      setExecutionMode("submit");
      setExecutionResult(null);

      const response = await api.post("/api/execute/submit", {
        problem_id: problemId,
        language,
        source_code: code,
        mode: "samples",
      });

      setExecutionResult(response.data);
    } catch (err) {
      setExecutionResult({
        status: "error",
        message:
          err.response?.data?.detail || "Code submission failed.",
      });
    } finally {
      setExecuting(false);
      setExecutionMode("");
    }
  };

  if (loading) {
    return <div className="panel">Loading LeetCode problem...</div>;
  }

  if (error) {
    return <div className="panel library-message">{error}</div>;
  }

  if (!problem) {
    return <div className="panel">No problem selected.</div>;
  }

  return (
    <div className="practice-workspace">
      {/* Problem Information */}
      <div className="panel">
        <p className="eyebrow">PRACTICE WORKSPACE</p>

        <h2>
          {problem.number !== "?" ? `#${problem.number} ` : ""}
          {problem.title}
        </h2>

        <p>
          <strong>{problem.difficulty}</strong>
          {" · "}
          Source: {problem.source}
        </p>

        {problem.tags?.length > 0 && (
          <div className="problem-tags">
            {problem.tags.map((tag, index) => (
              <span className="problem-tag" key={index}>
                <Tag size={13} />
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Problem Description */}
      <div className="panel">
        <h3>
          <BookOpen size={18} /> Problem Description
        </h3>

        <div className="problem-description">
          {problem.description?.split("\n").map((line, index) => (
            <p key={index}>{line || "\u00A0"}</p>
          ))}
        </div>
      </div>

      {/* Examples */}
      {problem.examples && (
        <div className="panel">
          <h3>Example Test Cases</h3>
          <pre className="problem-examples">{problem.examples}</pre>
        </div>
      )}

      {/* LeetCode Hints */}
      {problem.hints?.length > 0 && (
        <div className="panel">
          <h3>
            <Lightbulb size={18} /> LeetCode Hints
          </h3>

          {problem.hints.map((hint, index) => (
            <p key={index}>
              <strong>Hint {index + 1}:</strong> {hint}
            </p>
          ))}
        </div>
      )}

      {/* Code Editor */}
      <div className="panel editor-panel">
        <div className="editor-toolbar">
          <h3>Code Editor</h3>

          <select
            value={language}
            onChange={handleLanguageChange}
            disabled={executing}
            aria-label="Select programming language"
          >
            {languageOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <CodeEditor
          language={language}
          value={code}
          onChange={(value) => setCode(value || "")}
        />

        <div className="editor-actions">
          <button
            type="button"
            onClick={handleRun}
            disabled={executing}
          >
            {executing && executionMode === "run" ? (
              <Loader2 size={16} className="spin" />
            ) : (
              <Play size={16} />
            )}
            Run
          </button>

          <button
            type="button"
            onClick={handleSubmit}
            disabled={executing}
          >
            {executing && executionMode === "submit" ? (
              <Loader2 size={16} className="spin" />
            ) : (
              <Send size={16} />
            )}
            Submit
          </button>
        </div>
      </div>

      {/* Custom Input */}
      <div className="panel">
        <h3>Custom Input</h3>

        <textarea
          className="custom-input"
          value={stdin}
          onChange={(event) => setStdin(event.target.value)}
          placeholder="Enter input for your program..."
          rows={4}
        />
      </div>

      {/* Execution Output */}
      <div className="panel output-panel">
        <h3>
          <Terminal size={18} /> Execution Output
        </h3>

        {executing && (
          <p>
            <Loader2 size={16} className="spin" /> Executing your code...
          </p>
        )}

        {!executing && !executionResult && (
          <p>Run or submit your code to see the results here.</p>
        )}

        {executionResult && (
          <>
            <p>
              <strong>Status:</strong>{" "}
              {executionResult.status || "Unknown"}
            </p>

            {executionResult.stdout && (
              <>
                <strong>Output</strong>
                <pre>{executionResult.stdout}</pre>
              </>
            )}

            {executionResult.stderr && (
              <>
                <strong>Errors</strong>
                <pre>{executionResult.stderr}</pre>
              </>
            )}

            {executionResult.message && (
              <p>{executionResult.message}</p>
            )}

            {executionResult.results && (
              <>
                <strong>Test Case Results</strong>
                <pre>
                  {JSON.stringify(executionResult.results, null, 2)}
                </pre>
              </>
            )}

            {!executionResult.stdout &&
              !executionResult.stderr &&
              !executionResult.message &&
              !executionResult.results && (
                <pre>
                  {JSON.stringify(executionResult, null, 2)}
                </pre>
              )}
          </>
        )}
      </div>
    </div>
  );
}

export default PracticeWorkspace;
