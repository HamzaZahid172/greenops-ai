import { API_BASE_URL } from "../config/api";

import type {
  CarbonScheduleRequest,
  CarbonScheduleResponse,
} from "../types/scheduler";


export async function scheduleWorkload(
  request: CarbonScheduleRequest,
): Promise<CarbonScheduleResponse> {

  const response = await fetch(
    `${API_BASE_URL}/carbon/schedule`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(request),
    },
  );


  if (!response.ok) {
    throw new Error(
      "Unable to calculate carbon schedule.",
    );
  }


  return response.json();
}