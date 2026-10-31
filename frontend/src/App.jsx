import { useState, useEffect } from "react";
import api from "./services/api";
import PracticeWorkspace from "./pages/PracticeWorkspace";
import ProblemLibrary from "./pages/ProblemLibrary";
import {
  LayoutDashboard,
  BookOpen,
  Code2,
  MessageSquareText,
  ChartNoAxesCombined,
  RefreshCw,
  Settings,
  Search,
  Bell,
  ChevronDown,
  ArrowUpRight,
  Clock3,
  Target,
  Flame,
  PanelLeftClose,
} from "lucide-react";

const navigation = [
  {
    label: "LEARNING",
    items: [
      { name: "Overview", icon: LayoutDashboard },
      { name: "Problem Library", icon: BookOpen },
      { name: "Practice Workspace", icon: Code2 },
      { name: "Mentor", icon: MessageSquareText },
    ],
  },
  {
    label: "YOUR PROGRESS",
    items: [
      { name: "Learning Progress", icon: ChartNoAxesCombined },
      { name: "LeetCode Sync", icon: RefreshCw },
    ],
  },
];

function Sidebar({ activePage, setActivePage }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">S</div>
        <div>
          <h1>SahiiiDSA</h1>
          <span>Learn. Think. Solve.</span>
        </div>
        <button className="icon-button sidebar-toggle" aria-label="Toggle sidebar">
          <PanelLeftClose size={17} />
        </button>
      </div>

      <div className="profile-card">
        <div className="avatar">SG</div>
        <div className="profile-details">
          <strong>Welcome back</strong>
          <span>Your learning space</span>
        </div>
        <ChevronDown size={15} className="muted-icon" />
      </div>

      <nav className="navigation">
        {navigation.map((group) => (
          <div className="nav-group" key={group.label}>
            <p className="nav-heading">{group.label}</p>
            {group.items.map(({ name, icon: Icon }) => (
              <button
                key={name}
                onClick={() => setActivePage(name)}
                className={`nav-item ${activePage === name ? "active" : ""}`}
              >
                <Icon size={18} strokeWidth={1.8} />
                <span>{name}</span>
              </button>
            ))}
          </div>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <button className="nav-item">
          <Settings size={18} strokeWidth={1.8} />
          <span>Settings</span>
        </button>
        <div className="sidebar-footer">
          <span>SAHIIIDSA</span>
          <span>Version 1.0</span>
        </div>
      </div>
    </aside>
  );
}

function StatCard({ label, value, note, icon: Icon }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <span>{label}</span>
        <Icon size={18} strokeWidth={1.7} />
      </div>
      <div className="stat-value">{value}</div>
      <div className="stat-note">{note}</div>
    </div>
  );
}

function Overview({ setActivePage }) {
  return (
    <>
      <section className="welcome-section">
        <div>
          <p className="eyebrow">YOUR LEARNING OVERVIEW</p>
          <h2>Build understanding, one problem at a time.</h2>
          <p className="welcome-description">
            Keep practising, explore new patterns and strengthen your
            problem-solving approach.
          </p>
        </div>
        <button
  className="primary-button"
  onClick={() => setActivePage("Problem Library")}
>
  Explore Problems
</button>
      </section>

      <section className="stats-grid">
        <StatCard
          label="Problems solved"
          value="--"
          note="Your recorded practice"
          icon={Target}
        />
        <StatCard
          label="Current streak"
          value="--"
          note="Consecutive practice days"
          icon={Flame}
        />
        <StatCard
          label="Time invested"
          value="--"
          note="Total learning time"
          icon={Clock3}
        />
        <StatCard
          label="Patterns explored"
          value="--"
          note="Across DSA topics"
          icon={ChartNoAxesCombined}
        />
      </section>

      <section className="content-grid">
        <div className="panel main-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">PICK UP WHERE YOU LEFT OFF</p>
              <h3>Continue learning</h3>
            </div>
            <button className="text-button">
              View all <ArrowUpRight size={15} />
            </button>
          </div>

          <div className="empty-state">
            <div className="empty-icon">
              <BookOpen size={23} strokeWidth={1.6} />
            </div>
            <h4>Your next problem starts here.</h4>
            <p>
              Select a problem from your question bank and work through
              it at your own pace.
            </p>
            <button className="secondary-button" onClick={() => setActivePage("Problem Library")}>
              Browse problem library
            </button>
          </div>
        </div>

        <div className="panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">YOUR PRACTICE</p>
              <h3>Learning activity</h3>
            </div>
          </div>

          <div className="activity-placeholder">
            <ChartNoAxesCombined size={25} strokeWidth={1.5} />
            <p>Activity insights will appear here.</p>
            <span>
              Your practice history will populate this section once
              connected to your existing learning data.
            </span>
          </div>
        </div>
      </section>

      <section className="panel patterns-panel">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">KNOW YOUR FUNDAMENTALS</p>
            <h3>DSA pattern progress</h3>
          </div>
          <span className="coming-label">Learning insights</span>
        </div>
        <p className="patterns-description">
          Track your understanding of topics such as arrays, linked lists,
          trees, graphs and dynamic programming.
        </p>
      </section>
    </>
  );
}

function PlaceholderPage({ title }) {
  return (
    <div className="panel page-placeholder">
      <p className="eyebrow">SAHIIIDSA WORKSPACE</p>
      <h2>{title}</h2>
      <p>
        This section will be connected to the existing Python
        functionality during the feature-by-feature migration.
      </p>
    </div>
  );
}

export default function App() {
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [activePage, setActivePage] = useState("Overview");
useEffect(() => {
  const checkBackend = async () => {
    try {
      const response = await api.get("/api/health");
      console.log("Backend connected:", response.data);
    } catch (error) {
      console.error("Backend connection failed:", error.message);
    }
  };

  checkBackend();
}, []);
  return (
    <div className="app-shell">
      <Sidebar activePage={activePage} setActivePage={setActivePage} />

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> {activePage}
          </div>
          <div className="topbar-actions">
            <div className="search-box">
              <Search size={16} />
              <span>Search your workspace</span>
              <kbd>⌘ K</kbd>
            </div>
            <button className="icon-button" aria-label="Notifications">
              <Bell size={18} />
            </button>
            <div className="topbar-avatar">SG</div>
          </div>
        </header>

        <div className="page-content">
 {activePage === "Overview" && (
  <Overview setActivePage={setActivePage} />
)}
  {activePage === "Problem Library" && (
    <ProblemLibrary
      onSelectProblem={(problemId) => {
        setSelectedProblem(problemId);
        setActivePage("Practice Workspace");
      }}
    />
  )}

  {activePage === "Practice Workspace" && (
  <PracticeWorkspace problemId={selectedProblem} />
)}

  {!["Overview", "Problem Library", "Practice Workspace"].includes(
    activePage
  ) && <PlaceholderPage title={activePage} />}
</div>

        <footer className="app-footer">
          <span>SahiiiDSA · Learn. Think. Solve.</span>
          <span>Designed for independent problem solving.</span>
        </footer>
      </main>
    </div>
  );
}
