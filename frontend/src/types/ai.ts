import type {
  WorkloadType,
} from "./workload";


export type AIWorkloadExplanationRequest = {
  workload_name: string;

  cpu_usage: number;

  memory_usage: number;

  replicas: number;

  runtime_hours: number;

  requests_per_day: number;

  workload_type: WorkloadType;
};


export type AIExplanationResponse = {
  workload_name: string;

  efficiency_score: number;

  status: string;

  explanation: string;

  provider: string;
};