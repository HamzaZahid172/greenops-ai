from fastapi import (
    APIRouter,
    HTTPException,
)

from app.schemas.ai import (
    AIExplanationResponse,
    AIWorkloadExplanationRequest,
)

from app.schemas.workload import (
    WorkloadRequest,
)

from app.services.ai.base import (
    AIProviderError,
)

from app.services.ai.ollama_provider import (
    OllamaProvider,
)

from app.services.ai.prompts import (
    build_workload_explanation_prompt,
)

from app.services.workload_analyzer import (
    analyze_workload,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


provider = OllamaProvider()


@router.post(
    "/explain-workload",
    response_model=AIExplanationResponse,
)
async def explain_workload(
    request: AIWorkloadExplanationRequest,
):

    workload = WorkloadRequest(
        name=request.workload_name,
        cpu_usage=request.cpu_usage,
        memory_usage=request.memory_usage,
        replicas=request.replicas,
        runtime_hours=request.runtime_hours,
        requests_per_day=(
            request.requests_per_day
        ),
        workload_type=request.workload_type,
    )


    analysis = analyze_workload(
        workload
    )


    prompt = (
        build_workload_explanation_prompt(
            workload,
            analysis,
        )
    )


    try:
        explanation = (
            await provider.generate(
                prompt,
            )
        )

    except AIProviderError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "AI provider is currently "
                "unavailable."
            ),
        ) from exc


    return AIExplanationResponse(
        workload_name=workload.name,
        efficiency_score=(
            analysis.efficiency_score
        ),
        status=analysis.status,
        explanation=explanation,
        provider="ollama",
    )