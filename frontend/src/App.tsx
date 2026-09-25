import { useState } from "react";

import CarbonIntelligence from "./pages/CarbonIntelligence";
import Dashboard from "./pages/Dashboard";
import WorkloadAnalyzer from "./pages/WorkloadAnalyzer";
import CarbonScheduler from "./pages/CarbonScheduler";
import AIAssistant from "./pages/AIAssistant";
import AgentAssistant from "./pages/AgentAssistant";

type View = "overview" | "workloads" | "carbon" | "scheduler" | "ai" | "agent";

function App() {
  const [view, setView] = useState<View>("overview");

  return (
    <>
      <header className="app-header">
        <strong>🌱 GreenOps AI</strong>

        <nav>
          <button onClick={() => setView("overview")}>Overview</button>

          <button onClick={() => setView("workloads")}>Workloads</button>

          <button onClick={() => setView("carbon")}>Carbon Intelligence</button>

          <button onClick={() => setView("scheduler")}>Carbon Scheduler</button>

          <button onClick={() => setView("ai")}>AI Assistant</button>

          <button onClick={() => setView("agent")}>AI Agent</button>
        </nav>
      </header>

      {view === "overview" && <Dashboard />}

      {view === "workloads" && <WorkloadAnalyzer />}

      {view === "carbon" && <CarbonIntelligence />}

      {view === "scheduler" && <CarbonScheduler />}

      {view === "ai" && <AIAssistant />}

      {view === "agent" && <AgentAssistant />}
    </>
  );
}

export default App;
