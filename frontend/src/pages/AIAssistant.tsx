import { useState } from "react";

import {
  explainWorkload,
} from "../services/ai";

import type {
  AIExplanationResponse,
  AIWorkloadExplanationRequest,
} from "../types/ai";

import type {
  WorkloadType,
} from "../types/workload";


const initialForm:
  AIWorkloadExplanationRequest = {

  workload_name: "",

  cpu_usage: 50,

  memory_usage: 50,

  replicas: 1,

  runtime_hours: 8,

  requests_per_day: 1000,

  workload_type: "realtime",
};


function AIAssistant() {

  const [form, setForm] =
    useState(initialForm);


  const [result, setResult] =
    useState<AIExplanationResponse | null>(
      null,
    );


  const [loading, setLoading] =
    useState(false);


  const [error, setError] =
    useState<string | null>(null);


  async function handleSubmit(
    event:
      React.FormEvent<HTMLFormElement>,
  ) {

    event.preventDefault();

    setLoading(true);
    setError(null);


    try {

      const response =
        await explainWorkload(
          form,
        );

      setResult(response);

    } catch {

      setError(
        "AI explanation is "
        + "currently unavailable.",
      );

    } finally {

      setLoading(false);

    }
  }


  return (
    <main>

      <h1>
        GreenOps AI Assistant
      </h1>

      <p>
        Get an AI explanation of
        GreenOps workload analysis.
      </p>


      <form
        className="workload-form"
        onSubmit={handleSubmit}
      >

        <label>
          Workload Name

          <input
            required
            value={
              form.workload_name
            }
            onChange={(event) =>
              setForm({
                ...form,
                workload_name:
                  event.target.value,
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
                  Number(
                    event.target.value,
                  ),
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
            value={
              form.memory_usage
            }
            onChange={(event) =>
              setForm({
                ...form,
                memory_usage:
                  Number(
                    event.target.value,
                  ),
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
                  Number(
                    event.target.value,
                  ),
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
            value={
              form.runtime_hours
            }
            onChange={(event) =>
              setForm({
                ...form,
                runtime_hours:
                  Number(
                    event.target.value,
                  ),
              })
            }
          />
        </label>


        <label>
          Requests Per Day

          <input
            type="number"
            min="0"
            value={
              form.requests_per_day
            }
            onChange={(event) =>
              setForm({
                ...form,
                requests_per_day:
                  Number(
                    event.target.value,
                  ),
              })
            }
          />
        </label>


        <label>
          Workload Type

          <select
            value={
              form.workload_type
            }
            onChange={(event) =>
              setForm({
                ...form,
                workload_type:
                  event.target
                    .value as WorkloadType,
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
            ? "Thinking..."
            : "Explain with AI"}

        </button>

      </form>


      {error && (
        <p>{error}</p>
      )}


      {result && (
        <section
          className="analysis-result"
        >

          <h2>
            AI Explanation
          </h2>


          <p>
            Workload:{" "}
            <strong>
              {
                result
                  .workload_name
              }
            </strong>
          </p>


          <p>
            GreenOps Score:{" "}
            <strong>
              {
                result
                  .efficiency_score
              }
              /100
            </strong>
          </p>


          <p>
            Status:{" "}
            <strong>
              {result.status}
            </strong>
          </p>


          <div className="ai-response">
            {
              result.explanation
            }
          </div>


          <small>
            AI Provider:{" "}
            {result.provider}
          </small>

        </section>
      )}

    </main>
  );
}


export default AIAssistant;