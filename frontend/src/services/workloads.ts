import type {
  WorkloadAnalysis,
  WorkloadRequest,
} from "../types/workload";


const API_BASE_URL =
  "http://127.0.0.1:8000/api/v1";


export async function analyzeWorkload(
  workload: WorkloadRequest,
): Promise<WorkloadAnalysis> {

  const response = await fetch(
    `${API_BASE_URL}/workloads/analyze`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(workload),
    },
  );

  if (!response.ok) {
    throw new Error(
      "Failed to analyze workload",
    );
  }

  return response.json();
}