from prometheus_client import (
    Counter,
    Histogram,
)


HTTP_REQUESTS_TOTAL = Counter(
    "greenops_http_requests_total",
    "Total number of HTTP requests.",
    [
        "method",
        "route",
        "status",
    ],
)


HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "greenops_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    [
        "method",
        "route",
    ],
)


AI_GENERATION_DURATION_SECONDS = Histogram(
    "greenops_ai_generation_duration_seconds",
    "LLM generation duration in seconds.",
    [
        "provider",
        "model",
    ],
)


AI_ERRORS_TOTAL = Counter(
    "greenops_ai_errors_total",
    "Total AI provider errors.",
    [
        "provider",
        "operation",
    ],
)


EMBEDDING_DURATION_SECONDS = Histogram(
    "greenops_embedding_duration_seconds",
    "Embedding generation duration.",
    [
        "provider",
        "model",
    ],
)


RAG_RETRIEVAL_DURATION_SECONDS = Histogram(
    "greenops_rag_retrieval_duration_seconds",
    "RAG retrieval duration in seconds.",
)


AGENT_TOOL_DURATION_SECONDS = Histogram(
    "greenops_agent_tool_duration_seconds",
    "Agent tool execution duration.",
    [
        "tool",
    ],
)


AGENT_TOOL_CALLS_TOTAL = Counter(
    "greenops_agent_tool_calls_total",
    "Total number of agent tool calls.",
    [
        "tool",
        "outcome",
    ],
)