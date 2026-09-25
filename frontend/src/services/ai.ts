import {
  API_BASE_URL,
} from "../config/api";

import type {
  AIExplanationResponse,
  AIWorkloadExplanationRequest,
} from "../types/ai";


export async function explainWorkload(
  request: AIWorkloadExplanationRequest,
): Promise<AIExplanationResponse> {

  const response = await fetch(
    `${API_BASE_URL}/ai/explain-workload`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify(
        request,
      ),
    },
  );


  if (!response.ok) {
    throw new Error(
      "Unable to generate AI explanation."
    );
  }


  return response.json();
}