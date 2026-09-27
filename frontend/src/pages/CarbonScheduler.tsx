import { useState } from "react";

import { scheduleWorkload } from "../services/scheduler";

import type {
  CarbonScheduleRequest,
  CarbonScheduleResponse,
} from "../types/scheduler";


const initialForm: CarbonScheduleRequest = {
  workload_name: "",
  runtime_minutes: 60,
  max_delay_hours: 6,
};


function CarbonScheduler() {
  const [form, setForm] =
    useState(initialForm);

  const [result, setResult] =
    useState<CarbonScheduleResponse | null>(
      null,
    );

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
      const response =
        await scheduleWorkload(form);

      setResult(response);

    } catch {
      setError(
        "Unable to calculate the carbon-aware schedule.",
      );

    } finally {
      setLoading(false);
    }
  }


  return (
    <main>

      <h1>
        Carbon-Aware Scheduler
      </h1>

      <p>
        Find a lower-carbon execution
        window for flexible workloads.
      </p>


      <form
        className="workload-form"
        onSubmit={handleSubmit}
      >

        <label>
          Workload Name

          <input
            required
            value={form.workload_name}
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
          Runtime Minutes

          <input
            type="number"
            min="30"
            max="1440"
            value={form.runtime_minutes}
            onChange={(event) =>
              setForm({
                ...form,
                runtime_minutes:
                  Number(
                    event.target.value,
                  ),
              })
            }
          />
        </label>


        <label>
          Maximum Delay (hours)

          <input
            type="number"
            min="1"
            max="24"
            value={form.max_delay_hours}
            onChange={(event) =>
              setForm({
                ...form,
                max_delay_hours:
                  Number(
                    event.target.value,
                  ),
              })
            }
          />
        </label>


        <button disabled={loading}>
          {loading
            ? "Optimizing..."
            : "Find Best Window"}
        </button>

      </form>


      {error && (
        <p>{error}</p>
      )}


      {result && (
        <section className="analysis-result">

          <h2>
            Scheduling Recommendation
          </h2>

          <h3>
            {result.workload_name}
          </h3>


          <div className="schedule-comparison">

            <div>
              <h3>Run Now</h3>

              <p>
                {
                  new Date(
                    result
                      .current_window
                      .start_time,
                  ).toLocaleString()
                }
              </p>

              <strong>
                {
                  result
                    .current_window
                    .average_intensity
                }{" "}
                gCO₂/kWh
              </strong>
            </div>


            <div>
              <h3>
                Recommended
              </h3>

              <p>
                {
                  new Date(
                    result
                      .recommended_window
                      .start_time,
                  ).toLocaleString()
                }
              </p>

              <strong>
                {
                  result
                    .recommended_window
                    .average_intensity
                }{" "}
                gCO₂/kWh
              </strong>
            </div>

          </div>


          <h2>
            Potential Reduction
          </h2>

          <div className="carbon-value">
            {result.reduction_percent}%
          </div>


          <p>
            {result.message}
          </p>

        </section>
      )}

    </main>
  );
}


export default CarbonScheduler;