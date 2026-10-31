import { useEffect, useState } from "react";
import {
  Search,
  BookOpen,
  ArrowUpRight,
  LoaderCircle,
  AlertCircle,
} from "lucide-react";
import api from "../services/api";

export default function ProblemLibrary({ onSelectProblem }) {
  const [questions, setQuestions] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await api.get("/api/questions/");
        setQuestions(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail || "Unable to load questions."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  const filteredQuestions = questions.filter((question) =>
    question.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="welcome-section">
        <div>
          <p className="eyebrow">BUILD YOUR FUNDAMENTALS</p>
          <h2>Problem Library</h2>
          <p className="welcome-description">
            Explore structured problems and strengthen your DSA skills.
          </p>
        </div>

        <div className="coming-label">
          {questions.length} available problems
        </div>
      </div>

      <div className="panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">QUESTION BANK</p>
            <h3>Available problems</h3>
          </div>
        </div>

        <div className="library-search">
          <Search size={17} />
          <input
            type="text"
            placeholder="Search problems..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {loading ? (
          <div className="library-message">
            <LoaderCircle className="spin" size={22} />
            <p>Loading questions...</p>
          </div>
        ) : error ? (
          <div className="library-message error-message">
            <AlertCircle size={22} />
            <p>{error}</p>
          </div>
        ) : filteredQuestions.length === 0 ? (
          <div className="library-message">
            <BookOpen size={25} />
            <p>No matching questions found.</p>
          </div>
        ) : (
          <div className="question-list">
            {filteredQuestions.map((question) => (
              <div className="question-card" key={question.id}>
                <div className="question-icon">
                  <BookOpen size={20} />
                </div>

                <div className="question-info">
                  <h4>{question.title}</h4>
                  <span>Method: {question.method}</span>
                </div>

                <button
                  className="primary-button"
                  onClick={() => onSelectProblem(question.id)}
                >
                  Practice <ArrowUpRight size={15} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}