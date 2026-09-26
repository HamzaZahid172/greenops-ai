from typing import Any

from app.schemas.agent import (
    AgentQueryRequest,
)

from app.schemas.workload import (
    WorkloadRequest,
)

from app.services.carbon.gb_provider import (
    GBCarbonIntensityProvider,
)

from app.services.carbon.scheduler import (
    find_best_carbon_window,
)

from app.services.workload_analyzer import (
    analyze_workload,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.rag.retriever import (
    search_knowledge_base,
)


carbon_provider = (
    GBCarbonIntensityProvider()
)


async def analyze_workload_tool(
    request: AgentQueryRequest,
) -> dict[str, Any]:

    if request.workload is None:
        return {
            "error":
                "Workload context is required."
        }

    workload = WorkloadRequest(
        **request.workload.model_dump()
    )

    result = analyze_workload(
        workload
    )

    return result.model_dump(
        mode="json"
    )


async def current_carbon_tool(
    request: AgentQueryRequest,
) -> dict[str, Any]:

    result = (
        await carbon_provider
        .get_current()
    )

    return result.model_dump(
        mode="json"
    )


async def schedule_tool(
    request: AgentQueryRequest,
) -> dict[str, Any]:

    if request.runtime_minutes is None:
        return {
            "error":
                "runtime_minutes is required "
                "for carbon scheduling."
        }

    if request.max_delay_hours is None:
        return {
            "error":
                "max_delay_hours is required "
                "for carbon scheduling."
        }

    forecast = (
        await carbon_provider
        .get_forecast()
    )

    workload_name = (
        request.workload.name
        if request.workload
        else "Unnamed workload"
    )

    result = find_best_carbon_window(
        workload_name=workload_name,
        forecast_points=(
            forecast.points
        ),
        runtime_minutes=(
            request.runtime_minutes
        ),
        max_delay_hours=(
            request.max_delay_hours
        ),
    )

    return result.model_dump(
        mode="json"
    )


async def execute_tool(
    tool_name: str,
    request: AgentQueryRequest,
    db: AsyncSession,
) -> dict[str, Any]:

    if tool_name == "analyze_workload":
        return await analyze_workload_tool(
            request
        )

    if tool_name == "get_current_carbon":
        return await current_carbon_tool(
            request
        )

    if tool_name == "search_documentation":
        return await search_documentation_tool(
            request,
            db,
        )

    if (
        tool_name
        == "find_low_carbon_window"
    ):
        return await schedule_tool(
            request
        )

    return {
        "error":
            f"Unknown tool: {tool_name}"
    }

async def search_documentation_tool(
    request: AgentQueryRequest,
    db: AsyncSession,
) -> dict[str, object]:

    results = await search_knowledge_base(
        session=db,
        query=request.question,
        top_k=5,
    )

    return {
        "results": [
            result.model_dump(
                mode="json"
            )
            for result in results
        ]
    }