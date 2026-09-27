import type {
  WorkloadType,
} from "./workload";


export type AgentWorkloadContext = {
  name: string;

  cpu_usage: number;

  memory_usage: number;

  replicas: number;

  runtime_hours: number;

  requests_per_day: number;

  workload_type: WorkloadType;
};


export type AgentQueryRequest = {
  question: string;

  workload?:
    AgentWorkloadContext;

  runtime_minutes?: number;

  max_delay_hours?: number;
};


export type AgentToolTrace = {
  tool: string;

  output:
    Record<string, unknown>;
};


export type AgentQueryResponse = {
  answer: string;

  tools_used: string[];

  trace: AgentToolTrace[];

  provider: string;
};