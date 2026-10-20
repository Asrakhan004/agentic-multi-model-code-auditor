
from router import router


def performance_audit(code: str) -> str:
    prompt = f"""
You are a Python performance auditor.

Analyze the code for meaningful performance problems, including:
- Inefficient algorithms or excessive time complexity
- Unnecessary nested loops
- Repeated expensive computations
- Unnecessary memory usage
- Inefficient data processing

Do not focus on security vulnerabilities or general correctness issues;
separate auditors handle those.

Only report performance issues supported by the provided code.
Avoid speculative optimizations without a clear reason.
Do not claim that you executed or benchmarked the code.

For each finding, provide:
- Issue type
- Severity: LOW, MEDIUM, HIGH, or CRITICAL
- Explanation
- Suggested fix

If no meaningful performance issues are identified, say so clearly.

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
        raise ValueError("Performance auditor returned an empty response.")

    return result.strip()
