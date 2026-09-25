import { useState } from "react";

import CarbonIntelligence from "./pages/CarbonIntelligence";
import Dashboard from "./pages/Dashboard";
import WorkloadAnalyzer from "./pages/WorkloadAnalyzer";
import CarbonScheduler from "./pages/CarbonScheduler";

type View = "overview" | "workloads" | "carbon" | "scheduler";

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
        </nav>
      </header>

      {view === "overview" && <Dashboard />}

      {view === "workloads" && <WorkloadAnalyzer />}

      {view === "carbon" && <CarbonIntelligence />}
      
      {view === "scheduler" && <CarbonScheduler />}
    </>
  );
}

export default App;
