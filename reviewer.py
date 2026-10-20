
from router import router


def review_findings(code: str, findings: dict) -> str:
    """
    Consolidate findings from specialized code auditors
    into one final report.
    """

    prompt = f"""
You are a careful senior Python code reviewer validating findings
from specialized security, correctness, and performance auditors.

ORIGINAL PYTHON CODE:
```python
{code}

AUDITOR FINDINGS:
{findings}

Review rules:

1. Verify every proposed finding against the original code. Report only issues supported by the supplied snippet.
2. Do not invent bugs based on function names, coding style, or assumptions about what callers expect.
3. Do not report a return-value mismatch merely because a function returns a cursor, result object, or other valid API result. Report it only when the code establishes that the returned value is incorrect.
4. Distinguish confirmed defects from conditional risks. If a concern depends on missing context, explain the condition or omit it if it adds no actionable value.
5. Do not claim that code was executed, tested, or benchmarked.
6. Use only these severity levels: LOW, MEDIUM, HIGH, CRITICAL. Choose severity according to realistic impact, not worst-case speculation.
7. Do not exaggerate severity. An undefined variable is generally a correctness bug, not automatically CRITICAL.
8. Do not assume input types, database configuration, caller expectations, or runtime behavior unless the snippet establishes them.
9. For SQL injection risks, recommend parameterized queries using the syntax supported by the database driver. Never recommend manual string escaping or string concatenation as the security fix.
10. When a variable is not defined in the supplied snippet, state that it is not defined in the snippet. Acknowledge that it may exist in an enclosing or global scope if relevant.
11. Do not claim that string concatenation necessarily causes a TypeError or invalid SQL unless the specific types and database behavior support that conclusion.
12. Do not duplicate the same underlying issue across multiple findings.
13. Give practical fixes that address confirmed issues without introducing unrelated changes.
14. If no issues are adequately supported, return a table row stating "No confirmed issues found" and explain briefly why.

Return a Markdown table with exactly these columns:
Issue | Type | Severity | Explanation | Suggested Fix

After the table, include a concise overall summary.

Return only the final report.
"""

    response = router.completion(
        model="code-auditor",
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("Reviewer returned an empty response.")

    return result.strip()

  