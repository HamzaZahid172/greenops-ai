import { API_BASE_URL } from "../config/api";

import type {
  CarbonCurrentResponse,
  CarbonForecastResponse,
} from "../types/carbon";


export async function getCurrentCarbon():
  Promise<CarbonCurrentResponse> {

  const response = await fetch(
    `${API_BASE_URL}/carbon/current`,
  );

  if (!response.ok) {
    throw new Error(
      "Unable to retrieve carbon data",
    );
  }

  return response.json();
}


export async function getCarbonForecast():
  Promise<CarbonForecastResponse> {

  const response = await fetch(
    `${API_BASE_URL}/carbon/forecast`,
  );

  if (!response.ok) {
    throw new Error(
      "Unable to retrieve carbon forecast",
    );
  }

  return response.json();
}