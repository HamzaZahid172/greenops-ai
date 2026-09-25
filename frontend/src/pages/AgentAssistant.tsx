import { useState } from "react";

import {
  askAgent,
} from "../services/agent";

import type {
  AgentQueryResponse,
} from "../types/agent";


function AgentAssistant() {

  const [question, setQuestion] =
    useState(
      "Should I run this batch workload now "
      + "or wait for a greener time?"
    );


  const [result, setResult] =
    useState<AgentQueryResponse | null>(
      null
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

      const response = await askAgent({
        question,

        workload: {
          name: "Embedding Worker",

          cpu_usage: 15,

          memory_usage: 50,

          replicas: 5,

          runtime_hours: 2,

          requests_per_day: 1000,

          workload_type: "batch",
        },

        runtime_minutes: 120,

        max_delay_hours: 6,
      });


      setResult(response);

    } catch {

      setError(
        "GreenOps Agent is "
        + "currently unavailable."
      );

    } finally {

      setLoading(false);

    }
  }


  return (
    <main>

      <h1>
        GreenOps Agent
      </h1>

      <p>
        Ask GreenOps questions that may
        require multiple engineering tools.
      </p>


      <form
        className="workload-form"
        onSubmit={handleSubmit}
      >

        <label>
          Question

          <textarea
            rows={5}
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
          />
        </label>


        <button disabled={loading}>

          {loading
            ? "Agent working..."
            : "Ask GreenOps Agent"}

        </button>

      </form>


      {error && (
        <p>{error}</p>
      )}


      {result && (
        <section
          className="analysis-result"
        >

          <h2>Agent Answer</h2>

          <div className="ai-response">
            {result.answer}
          </div>


          <h3>Tools Used</h3>

          <p>
            {result.tools_used.join(", ")}
          </p>


          <details>

            <summary>
              Agent Trace
            </summary>

            <pre>
              {JSON.stringify(
                result.trace,
                null,
                2,
              )}
            </pre>

          </details>

        </section>
      )}

    </main>
  );
}


export default AgentAssistant;