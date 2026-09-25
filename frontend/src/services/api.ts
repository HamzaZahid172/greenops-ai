import type { HealthResponse } from "../types/api";
import { API_BASE_URL } from "../config/api";

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Failed to connect to GreenOps API");
  }

  return response.json();
}