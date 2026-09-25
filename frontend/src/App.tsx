import { useState } from "react";

import CarbonIntelligence from "./pages/CarbonIntelligence";
import Dashboard from "./pages/Dashboard";
import WorkloadAnalyzer from "./pages/WorkloadAnalyzer";


type View =
  | "overview"
  | "workloads"
  | "carbon";


function App() {
  const [view, setView] =
    useState<View>("overview");


  return (
    <>
      <header className="app-header">

        <strong>
          🌱 GreenOps AI
        </strong>

        <nav>
          <button
            onClick={() =>
              setView("overview")
            }
          >
            Overview
          </button>

          <button
            onClick={() =>
              setView("workloads")
            }
          >
            Workloads
          </button>

          <button
            onClick={() =>
              setView("carbon")
            }
          >
            Carbon Intelligence
          </button>
        </nav>

      </header>


      {view === "overview" && (
        <Dashboard />
      )}

      {view === "workloads" && (
        <WorkloadAnalyzer />
      )}

      {view === "carbon" && (
        <CarbonIntelligence />
      )}
    </>
  );
}


export default App;