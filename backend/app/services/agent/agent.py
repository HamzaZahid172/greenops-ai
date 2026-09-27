import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.agent import (
    AgentQueryRequest,
    AgentQueryResponse,
    AgentToolTrace,
)

from app.services.agent.planner import (
    plan_tools,
)

from app.services.agent.tools import (
    execute_tool,
)

from app.services.ai.ollama_provider import (
    OllamaProvider,
)


provider = OllamaProvider()


def build_final_prompt(
    request: AgentQueryRequest,
    trace: list[AgentToolTrace],
) -> str:

    tool_data = [
        {
            "tool": item.tool,
            "output": item.output,
        }
        for item in trace
    ]


    return f"""
You are GreenOps AI.

Answer the user's question using
ONLY the GreenOps tool results below.

USER QUESTION

{request.question}


TOOL RESULTS

{json.dumps(
    tool_data,
    indent=2,
)}


RULES

1. Do not invent numerical values.
2. Do not change tool results.
3. Clearly state when data is missing.
4. Do not claim cost savings unless
   the tool results contain them.
5. Do not claim carbon reductions
   unless the scheduler calculated them.
6. Keep infrastructure recommendations
   cautious and explain their basis.
7. Never claim an optimization has
   already been applied.
8. The system only recommends actions.

Provide a concise engineering answer.
""".strip()


async def run_agent(
    request: AgentQueryRequest,
    db: AsyncSession,
) -> AgentQueryResponse:

    planned_tools = (
        await plan_tools(
            request,
            provider,
        )
    )


    trace: list[
        AgentToolTrace
    ] = []


    for tool_name in planned_tools[
        :4
    ]:

        output = await execute_tool(
            tool_name,
            request,
            db,
        )

        trace.append(
            AgentToolTrace(
                tool=tool_name,
                output=output,
            )
        )


    final_prompt = build_final_prompt(
        request,
        trace,
    )


    answer = await provider.generate(
        final_prompt
    )


    return AgentQueryResponse(
        answer=answer,
        tools_used=[
            item.tool
            for item in trace
        ],
        trace=trace,
        provider="ollama",
    )