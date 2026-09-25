from app.schemas.workload import (
    WorkloadAnalysisResponse,
    WorkloadRequest,
)


def build_workload_explanation_prompt(
    workload: WorkloadRequest,
    analysis: WorkloadAnalysisResponse,
) -> str:

    recommendations = "\n".join(
        (
            f"- {item.title}: "
            f"{item.message}"
        )
        for item
        in analysis.recommendations
    )

    if not recommendations:
        recommendations = (
            "- No optimization problems detected."
        )


    return f"""
You are GreenOps AI, an assistant that explains
cloud workload optimization results.

IMPORTANT RULES:

1. Use only the facts provided below.
2. Do not invent numerical values.
3. Do not calculate new percentages.
4. Do not claim cost savings unless provided.
5. Do not claim carbon savings unless provided.
6. Clearly distinguish recommendations from facts.
7. Keep the explanation concise and technical.
8. Do not recommend shutting down critical services.

WORKLOAD DATA

Name:
{workload.name}

CPU usage:
{workload.cpu_usage}%

Memory usage:
{workload.memory_usage}%

Replicas:
{workload.replicas}

Runtime:
{workload.runtime_hours} hours

Requests per day:
{workload.requests_per_day}

Workload type:
{workload.workload_type.value}


GREENOPS ANALYSIS

Efficiency score:
{analysis.efficiency_score}/100

Status:
{analysis.status}

Recommendations:

{recommendations}


TASK

Explain the GreenOps analysis in plain English.

Structure the response as:

Summary

Why GreenOps reached this conclusion

Recommended next action

Risk / limitation
""".strip()