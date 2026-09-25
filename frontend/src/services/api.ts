import type { HealthResponse } from "../types/api";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Failed to connect to GreenOps API");
  }

  return response.json();
}