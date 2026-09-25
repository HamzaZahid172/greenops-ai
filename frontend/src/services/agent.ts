import {
  API_BASE_URL,
} from "../config/api";

import type {
  AgentQueryRequest,
  AgentQueryResponse,
} from "../types/agent";


export async function askAgent(
  request: AgentQueryRequest,
): Promise<AgentQueryResponse> {

  const response = await fetch(
    `${API_BASE_URL}/agent/query`,
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
      "GreenOps Agent unavailable."
    );
  }


  return response.json();
}