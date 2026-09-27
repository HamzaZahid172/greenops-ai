from collections.abc import Iterable


def normalize(
    value: str,
) -> str:
    return value.lower().strip()


def tool_exact_match(
    expected: list[str],
    actual: list[str],
) -> bool:

    return set(expected) == set(actual)


def tool_precision(
    expected: list[str],
    actual: list[str],
) -> float:

    actual_set = set(actual)

    if not actual_set:
        return 1.0 if not expected else 0.0

    expected_set = set(expected)

    correct = len(
        actual_set & expected_set
    )

    return correct / len(actual_set)


def tool_recall(
    expected: list[str],
    actual: list[str],
) -> float:

    expected_set = set(expected)

    if not expected_set:
        return 1.0

    actual_set = set(actual)

    correct = len(
        actual_set & expected_set
    )

    return correct / len(expected_set)


def required_term_coverage(
    answer: str,
    required_terms: Iterable[str],
) -> float:

    terms = list(required_terms)

    if not terms:
        return 1.0

    normalized_answer = normalize(
        answer
    )

    matched = sum(
        1
        for term in terms
        if normalize(term)
        in normalized_answer
    )

    return matched / len(terms)


def forbidden_term_hits(
    answer: str,
    forbidden_terms: Iterable[str],
) -> list[str]:

    normalized_answer = normalize(
        answer
    )

    return [
        term
        for term in forbidden_terms
        if normalize(term)
        in normalized_answer
    ]


def source_hit(
    expected_sources: list[str],
    actual_sources: list[str],
) -> bool:

    if not expected_sources:
        return True

    actual_set = set(
        actual_sources
    )

    return all(
        source in actual_set
        for source
        in expected_sources
    )