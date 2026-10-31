
import { useEffect, useState } from "react";
import { ArrowLeft, BookOpen, Lightbulb, Tag } from "lucide-react";
import api from "../services/api";

function PracticeWorkspace({ problemId }) {
  const [problem, setProblem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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

      <div className="panel">
        <h3>
          <BookOpen size={18} /> Problem Description
        </h3>

        <div className="problem-description">
          {problem.description
            ?.split("\n")
            .map((line, index) => (
              <p key={index}>{line || "\u00A0"}</p>
            ))}
        </div>
      </div>

      {problem.examples && (
        <div className="panel">
          <h3>Example Test Cases</h3>
          <pre className="problem-examples">
            {problem.examples}
          </pre>
        </div>
      )}

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
    </div>
  );
}

export default PracticeWorkspace;
