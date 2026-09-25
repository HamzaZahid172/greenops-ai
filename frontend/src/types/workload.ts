export type WorkloadType =
  | "realtime"
  | "batch"
  | "flexible"
  | "critical"
  | "non-critical";


export type WorkloadRequest = {
  name: string;
  cpu_usage: number;
  memory_usage: number;
  replicas: number;
  runtime_hours: number;
  requests_per_day: number;
  workload_type: WorkloadType;
};


export type Recommendation = {
  code: string;
  title: string;
  message: string;
  severity: string;
  estimated_saving_percent: number | null;
};


export type WorkloadAnalysis = {
  workload_name: string;
  efficiency_score: number;
  status: string;
  recommendations: Recommendation[];
};