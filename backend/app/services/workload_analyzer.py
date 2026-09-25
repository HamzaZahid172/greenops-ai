from app.schemas.workload import (
    Recommendation,
    WorkloadAnalysisResponse,
    WorkloadRequest,
    WorkloadType,
)


def analyze_workload(
    workload: WorkloadRequest,
) -> WorkloadAnalysisResponse:

    score = 100
    recommendations: list[Recommendation] = []

    # CPU analysis
    if workload.cpu_usage < 20:
        score -= 25

        recommendations.append(
            Recommendation(
                code="LOW_CPU_UTILIZATION",
                title="Very low CPU utilization",
                message=(
                    "CPU utilization is below 20%. "
                    "The workload may be over-provisioned."
                ),
                severity="high",
                estimated_saving_percent=25,
            )
        )

    elif workload.cpu_usage < 40:
        score -= 10

        recommendations.append(
            Recommendation(
                code="MODERATE_CPU_UNDERUTILIZATION",
                title="Low CPU utilization",
                message=(
                    "CPU utilization is below 40%. "
                    "Consider reviewing allocated resources."
                ),
                severity="medium",
                estimated_saving_percent=10,
            )
        )

    elif workload.cpu_usage > 90:
        score -= 20

        recommendations.append(
            Recommendation(
                code="HIGH_CPU_UTILIZATION",
                title="High CPU utilization",
                message=(
                    "CPU utilization is above 90%. "
                    "The workload may require additional capacity."
                ),
                severity="high",
            )
        )

    # Memory analysis
    if workload.memory_usage < 20:
        score -= 10

        recommendations.append(
            Recommendation(
                code="LOW_MEMORY_UTILIZATION",
                title="Low memory utilization",
                message=(
                    "Memory usage is below 20%. "
                    "Consider reducing allocated memory."
                ),
                severity="medium",
                estimated_saving_percent=10,
            )
        )

    elif workload.memory_usage > 90:
        score -= 15

        recommendations.append(
            Recommendation(
                code="HIGH_MEMORY_UTILIZATION",
                title="High memory utilization",
                message=(
                    "Memory usage is above 90%. "
                    "Review memory limits to reduce failure risk."
                ),
                severity="high",
            )
        )

    # Replica analysis
    if (
        workload.replicas >= 4
        and workload.cpu_usage < 40
    ):
        score -= 15

        recommendations.append(
            Recommendation(
                code="POSSIBLE_EXCESS_REPLICAS",
                title="Possible excess replicas",
                message=(
                    "Multiple replicas are running while CPU "
                    "utilization remains low. Consider testing "
                    "whether fewer replicas can handle the workload."
                ),
                severity="medium",
                estimated_saving_percent=15,
            )
        )

    # Workload scheduling opportunity
    if workload.workload_type in {
        WorkloadType.batch,
        WorkloadType.flexible,
    }:
        recommendations.append(
            Recommendation(
                code="SCHEDULING_OPPORTUNITY",
                title="Scheduling optimization available",
                message=(
                    "This workload may be suitable for "
                    "carbon-aware scheduling in a future phase."
                ),
                severity="info",
            )
        )

    score = max(0, min(score, 100))

    if score >= 80:
        status = "Efficient"
    elif score >= 60:
        status = "Review Recommended"
    else:
        status = "Needs Optimization"

    return WorkloadAnalysisResponse(
        workload_name=workload.name,
        efficiency_score=score,
        status=status,
        recommendations=recommendations,
    )