import { useEffect, useState } from "react";

import MetricCard from "../components/MetricCard";
import { getHealth } from "../services/api";
import type { HealthResponse } from "../types/api";


function Dashboard() {
  const [health, setHealth] =
    useState<HealthResponse | null>(null);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() => {
        setError("Backend unavailable");
      });
  }, []);


  return (
    <main>
      <h1>GreenOps AI Dashboard</h1>

      <p>
        Monitor and optimize cloud and AI workloads.
      </p>

      <p>
        API Status:{" "}
        {health
          ? health.status
          : error
            ? error
            : "Connecting..."}
      </p>

      <section className="metrics">
        <MetricCard
          title="Efficiency Score"
          value="--"
        />

        <MetricCard
          title="Carbon Intensity"
          value="--"
        />

        <MetricCard
          title="Potential Savings"
          value="--"
        />

        <MetricCard
          title="Active Workloads"
          value="0"
        />
      </section>
    </main>
  );
}

export default Dashboard;