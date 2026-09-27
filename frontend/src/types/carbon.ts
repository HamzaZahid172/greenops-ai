export type CarbonIntensityPoint = {
  from_time: string;
  to_time: string;

  forecast: number;
  actual: number | null;

  index: string;
};


export type CarbonCurrentResponse = {
  provider: string;
  region: string;
  unit: string;

  intensity: CarbonIntensityPoint;
};


export type CarbonForecastResponse = {
  provider: string;
  region: string;
  unit: string;

  points: CarbonIntensityPoint[];
};