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

    question = request.question.lower()

    tools: list[str] = []


    workload_keywords = (
        "workload",
        "cpu",
        "memory",
        "replica",
        "replicas",
        "efficient",
        "efficiency",
        "provisioned",
        "provisioning",
        "utilization",
    )

    if (
        request.workload is not None
        and any(
            keyword in question
            for keyword in workload_keywords
        )
    ):
        tools.append(
            "analyze_workload"
        )


    carbon_keywords = (
        "carbon",
        "emission",
        "emissions",
        "green",
        "greener",
        "electricity",
    )

    if any(
        keyword in question
        for keyword in carbon_keywords
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
        for keyword in schedule_keywords
    ):
        if (
            request.runtime_minutes
            is not None
            and request.max_delay_hours
            is not None
        ):
            tools.append(
                "find_low_carbon_window"
            )


    documentation_keywords = (
        "documentation",
        "document",
        "docs",
        "runbook",
        "architecture",
        "deployment",
        "policy",
        "requirement",
        "requirements",
        "configuration",
        "config",
        "knowledge base",
        "according to",
    )

    if any(
        keyword in question
        for keyword in documentation_keywords
    ):
        tools.append(
            "search_documentation"
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


def tool_is_applicable(
    tool_name: str,
    request: AgentQueryRequest,
) -> bool:
    """
    Validate an LLM-selected tool against
    the context actually available.

    The planner may suggest a valid tool name,
    but that does not mean the tool can be
    executed for this request.
    """

    if tool_name == "analyze_workload":
        return (
            request.workload
            is not None
        )


    if (
        tool_name
        == "find_low_carbon_window"
    ):
        return (
            request.runtime_minutes
            is not None
            and request.max_delay_hours
            is not None
        )


    if tool_name in {
        "get_current_carbon",
        "search_documentation",
    }:
        return True


    return False


async def plan_tools(
    request: AgentQueryRequest,
    provider: AIProvider,
) -> list[str]:

    prompt = f"""
You are the planning component of GreenOps AI.

Select the MINIMUM set of tools required
to answer the user's question.

Do not select tools that are unnecessary.
Do not select a tool when its required
input data is unavailable.

AVAILABLE TOOLS

analyze_workload
Use this ONLY when workload efficiency,
CPU, memory, replicas, provisioning,
or utilization must be analyzed.

IMPORTANT:
This tool requires workload context.
If no workload context is supplied,
DO NOT select analyze_workload.


get_current_carbon
Use this when current electricity
carbon intensity is required.


find_low_carbon_window
Use this when the user asks when a
flexible workload should run.

IMPORTANT:
This tool requires both runtime_minutes
and max_delay_hours.


search_documentation
Use this when the question depends on
uploaded documentation, architecture,
runbooks, deployment configuration,
operational rules, service requirements,
policies, or internal technical knowledge.


EXAMPLES

Question:
"Is this workload efficiently provisioned?"

If workload context is supplied:

{{
  "tools": [
    "analyze_workload"
  ]
}}


Question:
"According to the runbook, can the
payment service use two replicas?"

{{
  "tools": [
    "search_documentation"
  ]
}}


Question:
"What is the current carbon intensity?"

{{
  "tools": [
    "get_current_carbon"
  ]
}}


Question:
"When should this flexible workload run?"

If runtime and delay are supplied:

{{
  "tools": [
    "find_low_carbon_window"
  ]
}}


USER QUESTION

{request.question}


AVAILABLE CONTEXT

Workload supplied:
{request.workload is not None}

Runtime minutes:
{request.runtime_minutes}

Maximum delay hours:
{request.max_delay_hours}


Return ONLY valid JSON.

Format:

{{
  "tools": [
    "tool_name"
  ]
}}
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
            data.get(
                "tools",
                [],
            )
        )


        valid_tools = [
            tool
            for tool in requested_tools
            if (
                tool in ALLOWED_TOOLS
                and tool_is_applicable(
                    tool,
                    request,
                )
            )
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