import { useState } from "react";

import { analyzeWorkload } from "../services/workloads";

import type {
  WorkloadAnalysis,
  WorkloadRequest,
  WorkloadType,
} from "../types/workload";


const initialForm: WorkloadRequest = {
  name: "",
  cpu_usage: 50,
  memory_usage: 50,
  replicas: 1,
  runtime_hours: 8,
  requests_per_day: 1000,
  workload_type: "realtime",
};


function WorkloadAnalyzer() {
  const [form, setForm] =
    useState<WorkloadRequest>(initialForm);

  const [analysis, setAnalysis] =
    useState<WorkloadAnalysis | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);


  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setLoading(true);
    setError(null);

    try {
      const result =
        await analyzeWorkload(form);

      setAnalysis(result);

    } catch {
      setError(
        "Unable to analyze workload.",
      );

    } finally {
      setLoading(false);
    }
  }


  return (
    <main>
      <h1>Workload Analyzer</h1>

      <p>
        Analyze infrastructure utilization
        and identify optimization opportunities.
      </p>

      <form
        className="workload-form"
        onSubmit={handleSubmit}
      >
        <label>
          Workload Name

          <input
            required
            value={form.name}
            onChange={(event) =>
              setForm({
                ...form,
                name: event.target.value,
              })
            }
          />
        </label>


        <label>
          CPU Usage (%)

          <input
            type="number"
            min="0"
            max="100"
            value={form.cpu_usage}
            onChange={(event) =>
              setForm({
                ...form,
                cpu_usage:
                  Number(event.target.value),
              })
            }
          />
        </label>


        <label>
          Memory Usage (%)

          <input
            type="number"
            min="0"
            max="100"
            value={form.memory_usage}
            onChange={(event) =>
              setForm({
                ...form,
                memory_usage:
                  Number(event.target.value),
              })
            }
          />
        </label>


        <label>
          Replicas

          <input
            type="number"
            min="1"
            value={form.replicas}
            onChange={(event) =>
              setForm({
                ...form,
                replicas:
                  Number(event.target.value),
              })
            }
          />
        </label>


        <label>
          Runtime Hours

          <input
            type="number"
            min="1"
            max="24"
            value={form.runtime_hours}
            onChange={(event) =>
              setForm({
                ...form,
                runtime_hours:
                  Number(event.target.value),
              })
            }
          />
        </label>


        <label>
          Requests Per Day

          <input
            type="number"
            min="0"
            value={form.requests_per_day}
            onChange={(event) =>
              setForm({
                ...form,
                requests_per_day:
                  Number(event.target.value),
              })
            }
          />
        </label>


        <label>
          Workload Type

          <select
            value={form.workload_type}
            onChange={(event) =>
              setForm({
                ...form,
                workload_type:
                  event.target.value as WorkloadType,
              })
            }
          >
            <option value="realtime">
              Real-time
            </option>

            <option value="batch">
              Batch
            </option>

            <option value="flexible">
              Flexible
            </option>

            <option value="critical">
              Critical
            </option>

            <option value="non-critical">
              Non-critical
            </option>
          </select>
        </label>


        <button disabled={loading}>
          {loading
            ? "Analyzing..."
            : "Analyze Workload"}
        </button>
      </form>


      {error && (
        <p>{error}</p>
      )}


      {analysis && (
        <section className="analysis-result">

          <h2>
            Analysis Result
          </h2>

          <h3>
            {analysis.workload_name}
          </h3>

          <p>
            Efficiency Score:{" "}
            <strong>
              {analysis.efficiency_score}/100
            </strong>
          </p>

          <p>
            Status:{" "}
            <strong>
              {analysis.status}
            </strong>
          </p>


          <h3>Recommendations</h3>

          {analysis.recommendations.length === 0 ? (
            <p>
              No optimization issues detected.
            </p>
          ) : (
            analysis.recommendations.map(
              (recommendation) => (
                <div
                  key={recommendation.code}
                  className="recommendation"
                >
                  <strong>
                    {recommendation.title}
                  </strong>

                  <p>
                    {recommendation.message}
                  </p>

                  {recommendation.estimated_saving_percent !== null && (
                    <p>
                      Potential saving:{" "}
                      {
                        recommendation.estimated_saving_percent
                      }
                      %
                    </p>
                  )}
                </div>
              ),
            )
          )}

        </section>
      )}

    </main>
  );
}


export default WorkloadAnalyzer;