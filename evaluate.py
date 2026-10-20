
import csv
import json
from pathlib import Path

from orchestrator import run_audits

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "evaluation_cases.json"
RESULTS_PATH = BASE_DIR / "evaluation_results.csv"


# Simple keyword rules for this starter evaluation.
ISSUE_KEYWORDS = {
    "sql_injection": [
        "sql injection",
        "sql-injection",
        "sql injection vulnerability",
    ],
    "undefined_variable": [
        "undefined variable",
        "undefined name",
        "nameerror",
        "not defined",
        "undefined in the snippet",
    ],
    "hardcoded_secret": [
        "hardcoded password",
        "hardcoded secret",
        "hard-coded password",
        "hard-coded secret",
        "hard‑coded password",
        "hard‑coded secret",
        "plaintext password",
    ],
    "division_by_zero": [
        "division by zero",
        "divide by zero",
        "zero division",
        "zerodivisionerror",
    ],
}


def expected_issue_detected(report, expected_issue):
    text = report.lower()

    if expected_issue == "none":
        return False

    # Avoid counting negative mentions as detected issues.
    if "no confirmed issues found" in text:
        return False

    keywords = ISSUE_KEYWORDS.get(expected_issue, [])

    return any(keyword in text for keyword in keywords)


def main():
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        cases = json.load(file)

    results = []

    for index, case in enumerate(cases, start=1):
        print(f"\nEvaluating {index}/{len(cases)}: {case['id']}")

        try:
            report = run_audits(case["code"])
            error = ""
        except Exception as exc:
            report = ""
            error = str(exc)

        if error:
            outcome = "ERROR"
            detected = False

        elif case["expected_issue"] == "none":
            # Check the issue that this clean test is intended to avoid.
            related_issue = case.get("check_for_issue")

            if not related_issue:
                related_issue = (
                    "sql_injection"
                    if case["category"] == "security"
                    else "undefined_variable"
                )

            detected = expected_issue_detected(report, related_issue)
            outcome = (
                "FALSE POSITIVE" if detected else "TRUE NEGATIVE"
            )

        else:
            # Check whether the expected issue was detected.
            detected = expected_issue_detected(
                report, case["expected_issue"]
            )
            outcome = (
                "TRUE POSITIVE" if detected else "FALSE NEGATIVE"
            )

        print(f"Expected issue: {case['expected_issue']}")
        print(f"Keyword match: {detected}")
        print(f"Result: {outcome}")

        results.append({
            "id": case["id"],
            "category": case["category"],
            "expected_issue": case["expected_issue"],
            "detected_by_keyword_rule": detected,
            "outcome": outcome,
            "error": error,
            "report": report,
        })

    if results:
        with open(
            RESULTS_PATH, "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file, fieldnames=results[0].keys()
            )
            writer.writeheader()
            writer.writerows(results)

    successful = [
        row for row in results if row["outcome"] != "ERROR"
    ]

    print("\n--- Evaluation Summary ---")
    print(f"Total cases: {len(results)}")
    print(f"Completed without errors: {len(successful)}")
    print(
        f"True positives: "
        f"{sum(r['outcome'] == 'TRUE POSITIVE' for r in results)}"
    )
    print(
        f"False negatives: "
        f"{sum(r['outcome'] == 'FALSE NEGATIVE' for r in results)}"
    )
    print(
        f"False positives: "
        f"{sum(r['outcome'] == 'FALSE POSITIVE' for r in results)}"
    )
    print(
        f"True negatives: "
        f"{sum(r['outcome'] == 'TRUE NEGATIVE' for r in results)}"
    )
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
