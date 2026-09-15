import json
from pathlib import Path

from app.document import extract_text
from app.foundry import analyze_document


TEST_CASES_PATH = Path("evaluation/test_cases.json")


def normalize_text(value: str) -> str:
    return str(value).strip().lower()


def normalize_currency(currency: str) -> str:
    currency = normalize_text(currency)

    currency_map = {
        "$": "usd",
        "usd": "usd",
        "us dollar": "usd",
        "us dollars": "usd",

        "€": "eur",
        "eur": "eur",
        "euro": "eur",
        "euros": "eur",

        "£": "gbp",
        "gbp": "gbp",
        "pound": "gbp",
        "pounds": "gbp",
    }

    return currency_map.get(currency, currency)


def parse_expected_financial_value(value: str):
    value = value.strip()

    currency = None

    if value.startswith("$"):
        currency = "usd"
        amount_text = value[1:]
    elif value.startswith("€"):
        currency = "eur"
        amount_text = value[1:]
    elif value.startswith("£"):
        currency = "gbp"
        amount_text = value[1:]
    else:
        parts = value.split()

        if len(parts) == 2:
            currency = normalize_currency(parts[0])
            amount_text = parts[1]
        else:
            raise ValueError(
                f"Unsupported financial value format: {value}"
            )

    amount = float(
        amount_text.replace(",", "").strip()
    )

    return amount, currency


def financial_value_matches(actual, expected: str) -> bool:

    expected_amount, expected_currency = (
        parse_expected_financial_value(expected)
    )

    actual_amount = float(actual.amount)
    actual_currency = normalize_currency(actual.currency)

    return (
        actual_amount == expected_amount
        and actual_currency == expected_currency
    )


def evaluate_document(result, expected):

    total = 0
    passed = 0

    metrics = {
        "document_type": {
            "passed": 0,
            "total": 0,
        },
        "entities": {
            "passed": 0,
            "total": 0,
        },
        "financial_values": {
            "passed": 0,
            "total": 0,
        },
    }

    # Document Type

    if "document_type" in expected:
        total += 1
        metrics["document_type"]["total"] += 1

        actual_type = normalize_text(
            result.document_type
        )

        expected_type = normalize_text(
            expected["document_type"]
        )

        if actual_type == expected_type:
            passed += 1
            metrics["document_type"]["passed"] += 1

    # Entities

    expected_entities = expected.get(
        "entities",
        [],
    )

    actual_entities = [
        normalize_text(entity.name)
        for entity in result.entities
    ]

    for expected_entity in expected_entities:
        total += 1
        metrics["entities"]["total"] += 1

        expected_entity = normalize_text(
            expected_entity
        )

        if expected_entity in actual_entities:
            passed += 1
            metrics["entities"]["passed"] += 1

    # Financial Values

    expected_values = expected.get(
        "financial_values",
        [],
    )

    for expected_value in expected_values:
        total += 1
        metrics["financial_values"]["total"] += 1

        matched = False

        for actual_value in result.financial_values:
            if financial_value_matches(
                actual_value,
                expected_value,
            ):
                matched = True
                break

        if matched:
            passed += 1
            metrics["financial_values"]["passed"] += 1

    return passed, total, metrics


def calculate_percentage(passed: int, total: int) -> float:
    if total == 0:
        return 0.0

    return passed / total * 100


def main():

    # Load test cases

    with open(
        TEST_CASES_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        test_cases = json.load(file)

    overall_passed = 0
    overall_total = 0

    metric_totals = {
        "document_type": {
            "passed": 0,
            "total": 0,
        },
        "entities": {
            "passed": 0,
            "total": 0,
        },
        "financial_values": {
            "passed": 0,
            "total": 0,
        },
    }

    # Evaluation

    print()
    print("AI EVALUATION")
    print("=" * 60)

    for case in test_cases:

        file_path = Path(case["file"])

        with open(
            file_path,
            "rb",
        ) as file:
            content = file.read()

        text = extract_text(
            filename=file_path.name,
            content=content,
        )

        result = analyze_document(text)

        passed, total, metrics = evaluate_document(
            result,
            case["expected"],
        )

        overall_passed += passed
        overall_total += total

        # Add metrics to global totals
        for metric_name, values in metrics.items():

            metric_totals[metric_name]["passed"] += (
                values["passed"]
            )

            metric_totals[metric_name]["total"] += (
                values["total"]
            )

        print(
            f"{case['name']}: "
            f"{passed}/{total} checks passed"
        )

    # Overall Results

    overall_accuracy = calculate_percentage(
        overall_passed,
        overall_total,
    )

    print("=" * 60)

    print(
        f"Overall accuracy: "
        f"{overall_passed}/{overall_total} "
        f"({overall_accuracy:.1f}%)"
    )

    # Detailed Metrics

    print()
    print("METRICS")
    print("-" * 60)

    for metric_name, values in metric_totals.items():

        accuracy = calculate_percentage(
            values["passed"],
            values["total"],
        )

        display_name = (
            metric_name
            .replace("_", " ")
            .title()
        )

        print(
            f"{display_name}: "
            f"{values['passed']}/{values['total']} "
            f"({accuracy:.1f}%)"
        )

    # Security Evaluation

    security_cases = [
        case
        for case in test_cases
        if case["name"] == "prompt_injection"
    ]

    if security_cases:

        security_case = security_cases[0]

        with open(
            security_case["file"],
            "rb",
        ) as file:
            content = file.read()

        text = extract_text(
            filename=Path(
                security_case["file"]
            ).name,
            content=content,
        )

        result = analyze_document(text)

        security_passed, security_total, _ = (
            evaluate_document(
                result,
                security_case["expected"],
            )
        )

        security_accuracy = calculate_percentage(
            security_passed,
            security_total,
        )

        print(
            f"Prompt Injection Test: "
            f"{security_passed}/{security_total} "
            f"({security_accuracy:.1f}%)"
        )

    print("=" * 60)
    print()


if __name__ == "__main__":
    main()