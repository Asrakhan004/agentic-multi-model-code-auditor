
from router import router


def bug_audit(code: str) -> str:
    prompt = f"""
You are a Python code correctness auditor.


Analyze the code for concrete programming errors, including:
- Variables that are clearly undefined in the supplied code
- Incorrect conditions or logic
- Runtime exceptions that follow from the code and established input types
- Incorrect API or function usage that can be demonstrated from the snippet
- Edge cases that demonstrably produce incorrect behavior

Important constraints:
- Do not assume argument types when they are not specified.
- Do not report a possible TypeError merely because an operation could receive an incompatible type.
- Do not treat a function's name as proof of its intended return type.
- Do not report speculative return-value mismatches.
- Do not recommend converting values to strings just to avoid a hypothetical TypeError.
- When behavior depends on unknown input types or surrounding code, omit the finding unless the condition is important and clearly stated.
- Do not report security vulnerabilities; the security auditor handles those.


Do not focus on security vulnerabilities; a separate security auditor handles those.

Only report issues supported by the provided code.
Do not invent problems or assume behavior that cannot be established.
Do not claim that you executed or tested the code.

For each finding, provide:
- Issue type
- Severity: LOW, MEDIUM, HIGH, or CRITICAL
- Explanation
- Suggested fix
- Do not report a TypeError based only on the possibility that a variable might have an unexpected type. Report it only when the supplied code establishes the incompatible types.
- Do not report SQL syntax errors based only on hypothetical input values. The relevant input and database behavior must support the conclusion.
- Do not duplicate security vulnerabilities as correctness bugs. The security auditor handles unsafe SQL construction.
- Never recommend `str()` conversion, f-strings, manual quoting, or string concatenation as a fix for SQL injection.
- When the only concern is unsafe SQL query construction, leave it to the security auditor rather than creating separate speculative bug findings.

If no correctness issues are identified, say so clearly.

Python code:
```python
{code}
```
"""

    response = router.completion(
        model="code-auditor",
        messages=[{"role": "user", "content": prompt}],
    )

    result = response.choices[0].message.content

    if not result:
        raise ValueError("Bug auditor returned an empty response.")

    return result.strip()
