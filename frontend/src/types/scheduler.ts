export type CarbonScheduleRequest = {
  workload_name: string;
  runtime_minutes: number;
  max_delay_hours: number;
};


export type ScheduleWindow = {
  start_time: string;
  end_time: string;
  average_intensity: number;
};


export type CarbonScheduleResponse = {
  workload_name: string;

  current_window: ScheduleWindow;

  recommended_window: ScheduleWindow;

  reduction_percent: number;

  optimization_available: boolean;

  message: string;
};