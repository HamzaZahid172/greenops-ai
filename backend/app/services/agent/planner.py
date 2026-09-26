import json

from app.schemas.agent import (
    AgentQueryRequest,
)

from app.services.ai.base import (
    AIProvider,
)


ALLOWED_TOOLS = {
    "analyze_workload",
    "get_current_carbon",
    "find_low_carbon_window",
    "search_documentation",
}


def fallback_plan(
    request: AgentQueryRequest,
) -> list[str]:

    question = (
        request.question.lower()
    )

    tools: list[str] = []


    if request.workload is not None:
        tools.append(
            "analyze_workload"
        )


    carbon_keywords = (
        "carbon",
        "emission",
        "green",
        "electricity",
    )

    if any(
        keyword in question
        for keyword
        in carbon_keywords
    ):
        tools.append(
            "get_current_carbon"
        )


    schedule_keywords = (
        "when",
        "schedule",
        "wait",
        "run now",
        "best time",
    )

    if any(
        keyword in question
        for keyword
        in schedule_keywords
    ):
        if (
            request.runtime_minutes
            is not None
            and
            request.max_delay_hours
            is not None
        ):
            tools.append(
                "find_low_carbon_window"
            )


    return list(
        dict.fromkeys(tools)
    )


def extract_json(
    text: str,
) -> dict:

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace(
            "```json",
            "",
        )

        cleaned = cleaned.replace(
            "```",
            "",
        )

        cleaned = cleaned.strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "No JSON object found."
        )

    return json.loads(
        cleaned[start:end + 1]
    )


async def plan_tools(
    request: AgentQueryRequest,
    provider: AIProvider,
) -> list[str]:

    prompt = f"""
You are the planning component
of GreenOps AI.

Choose which tools are required
to answer the user's question.

AVAILABLE TOOLS

analyze_workload
Use this when workload efficiency,
CPU, memory, replicas or infrastructure
optimization needs to be analyzed.

get_current_carbon
Use this when the user needs current
electricity carbon-intensity information.

find_low_carbon_window
Use this when the user asks when a
flexible workload should run.

USER QUESTION

{request.question}

CONTEXT

Workload supplied:
{request.workload is not None}

Runtime minutes:
{request.runtime_minutes}

Maximum delay hours:
{request.max_delay_hours}

Return ONLY valid JSON.

Example:

{{
  "tools": [
    "analyze_workload",
    "get_current_carbon"
  ]
}}

Do not return explanations.
""".strip()


    try:
        raw_response = (
            await provider.generate(
                prompt
            )
        )

        data = extract_json(
            raw_response
        )

        requested_tools = (
            data.get("tools", [])
        )

        valid_tools = [
            tool
            for tool
            in requested_tools
            if tool in ALLOWED_TOOLS
        ]

        if valid_tools:
            return list(
                dict.fromkeys(
                    valid_tools
                )
            )

    except (
        ValueError,
        TypeError,
        json.JSONDecodeError,
    ):
        pass


    return fallback_plan(
        request
    )