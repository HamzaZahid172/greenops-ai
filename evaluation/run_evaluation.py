import asyncio
import json
import time

from pathlib import Path

import httpx

from evaluation.metrics import (
    forbidden_term_hits,
    required_term_coverage,
    source_hit,
    tool_exact_match,
    tool_precision,
    tool_recall,
)


ROOT = Path(__file__).parent

SCENARIOS_FILE = (
    ROOT / "scenarios.json"
)

FIXTURE_FILE = (
    ROOT
    / "fixtures"
    / "payment-runbook.md"
)

RESULTS_DIR = (
    ROOT / "results"
)

API_BASE_URL = (
    "http://127.0.0.1:8000/api/v1"
)


async def upload_fixture(
    client: httpx.AsyncClient,
) -> int:

    content = FIXTURE_FILE.read_bytes()

    response = await client.post(
        f"{API_BASE_URL}/rag/documents",
        files={
            "file": (
                FIXTURE_FILE.name,
                content,
                "text/markdown",
            )
        },
    )

    response.raise_for_status()

    return response.json()["id"]


async def delete_fixture(
    client: httpx.AsyncClient,
    document_id: int,
) -> None:

    response = await client.delete(
        (
            f"{API_BASE_URL}"
            f"/rag/documents/{document_id}"
        )
    )

    if response.status_code not in {
        204,
        404,
    }:
        response.raise_for_status()


async def evaluate_agent(
    client: httpx.AsyncClient,
    scenario: dict,
) -> dict:

    started = time.perf_counter()

    response = await client.post(
        f"{API_BASE_URL}/agent/query",
        json=scenario["request"],
    )

    latency_ms = (
        time.perf_counter()
        - started
    ) * 1000

    response.raise_for_status()

    data = response.json()

    answer = data["answer"]

    tools_used = data.get(
        "tools_used",
        [],
    )

    expected_tools = scenario.get(
        "expected_tools",
        [],
    )

    sources = []

    for trace in data.get(
        "trace",
        [],
    ):
        if (
            trace.get("tool")
            == "search_documentation"
        ):
            results = (
                trace.get(
                    "output",
                    {}
                )
                .get(
                    "results",
                    []
                )
            )

            sources.extend(
                result.get(
                    "filename",
                    ""
                )
                for result
                in results
            )

    return {
    "id": scenario["id"],
    "type": "agent",
    "latency_ms": round(
        latency_ms,
        2,
    ),
    "tools_used": tools_used,
    "tool_exact_match":
        tool_exact_match(
            expected_tools,
            tools_used,
        ),
    "tool_precision":
        round(
            tool_precision(
                expected_tools,
                tools_used,
            ),
            3,
        ),
    "tool_recall":
        round(
            tool_recall(
                expected_tools,
                tools_used,
            ),
            3,
        ),
    "required_term_coverage":
        round(
            required_term_coverage(
                answer,
                scenario.get(
                    "required_terms",
                    [],
                ),
            ),
            3,
        ),
    "forbidden_hits":
        forbidden_term_hits(
            answer,
            scenario.get(
                "forbidden_terms",
                [],
            ),
        ),
    "source_hit":
        source_hit(
            scenario.get(
                "expected_sources",
                [],
            ),
            sources,
        ),
    "answer": answer,
    }


async def evaluate_rag(
    client: httpx.AsyncClient,
    scenario: dict,
) -> dict:

    started = time.perf_counter()

    response = await client.post(
        f"{API_BASE_URL}/rag/ask",
        json=scenario["request"],
    )

    latency_ms = (
        time.perf_counter()
        - started
    ) * 1000

    response.raise_for_status()

    data = response.json()

    answer = data["answer"]

    sources = [
        source["filename"]
        for source
        in data.get(
            "sources",
            []
        )
    ]

    return {
        "id": scenario["id"],
        "type": "rag",
        "latency_ms": round(
            latency_ms,
            2,
        ),
        "required_term_coverage":
            round(
                required_term_coverage(
                    answer,
                    scenario.get(
                        "required_terms",
                        [],
                    ),
                ),
                3,
            ),
        "forbidden_hits":
            forbidden_term_hits(
                answer,
                scenario.get(
                    "forbidden_terms",
                    [],
                ),
            ),
        "source_hit":
            source_hit(
                scenario.get(
                    "expected_sources",
                    [],
                ),
                sources,
            ),
        "sources": sources,
        "answer": answer,
    }


def scenario_passed(
    result: dict,
) -> bool:

    if (
        result.get(
            "required_term_coverage",
            1.0,
        )
        < 0.5
    ):
        return False

    if result.get(
        "forbidden_hits"
    ):
        return False

    if (
        result.get(
            "source_hit"
        )
        is False
    ):
        return False

    if (
        "tool_exact_match"
        in result
        and not result[
            "tool_exact_match"
        ]
    ):
        return False

    return True


def failure_reasons(
    result: dict,
) -> list[str]:

    reasons: list[str] = []

    if (
        result.get(
            "required_term_coverage",
            1.0,
        )
        < 0.5
    ):
        reasons.append(
            "required term coverage below 50%"
        )

    forbidden_hits = result.get(
        "forbidden_hits",
        [],
    )

    if forbidden_hits:
        reasons.append(
            "forbidden terms found: "
            + ", ".join(
                forbidden_hits
            )
        )

    if (
        result.get("source_hit")
        is False
    ):
        reasons.append(
            "expected source was not retrieved"
        )

    if (
        "tool_exact_match"
        in result
        and not result[
            "tool_exact_match"
        ]
    ):
        reasons.append(
            "agent selected unexpected tools"
        )

    return reasons


async def main() -> None:

    scenarios = json.loads(
        SCENARIOS_FILE.read_text()
    )

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    async with httpx.AsyncClient(
        timeout=180.0,
    ) as client:

        fixture_id = (
            await upload_fixture(
                client
            )
        )

        try:
            results = []

            for scenario in scenarios:

                if (
                    scenario["type"]
                    == "agent"
                ):
                    result = (
                        await evaluate_agent(
                            client,
                            scenario,
                        )
                    )

                elif (
                    scenario["type"]
                    == "rag"
                ):
                    result = (
                        await evaluate_rag(
                            client,
                            scenario,
                        )
                    )

                else:
                    raise ValueError(
                        "Unknown scenario type: "
                        f"{scenario['type']}"
                    )

                result["passed"] = (
                    scenario_passed(
                        result
                    )
                )

                results.append(
                    result
                )

        finally:
            await delete_fixture(
                client,
                fixture_id,
            )


    passed = sum(
        1
        for result in results
        if result["passed"]
    )

    total = len(results)

    report = {
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(
                passed / total,
                3,
            )
            if total
            else 0.0,
        },
        "results": results,
    }


    output_path = (
        RESULTS_DIR
        / "latest.json"
    )

    output_path.write_text(
        json.dumps(
            report,
            indent=2,
        )
    )


    print()
    print("GreenOps AI Evaluation")
    print("======================")
    print(
        f"Passed: {passed}/{total}"
    )
    print(
        "Pass rate: "
        f"{report['summary']['pass_rate'] * 100:.1f}%"
    )

    for result in results:

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"{status}: "
            f"{result['id']} "
            f"({result['latency_ms']} ms)"
        )

        if not result["passed"]:

            reasons = failure_reasons(
                result
            )

            for reason in reasons:
                print(
                    f"      -> {reason}"
                )

            if "tools_used" in result:
                print(
                    "      -> tools used: "
                    f"{result['tools_used']}"
                )

    print()
    print(
        f"Report: {output_path}"
    )


if __name__ == "__main__":
    asyncio.run(main())