
from router import router


def security_audit(code: str) -> str:
    prompt = f"""
You are a Python security auditor.

Analyze the supplied code for genuine security vulnerabilities, including:
- SQL injection
- Command injection
- Hard-coded secrets
- Unsafe input handling
- Insecure authentication or authorization
- Other security weaknesses supported by the code

Only report issues supported by the provided code.
Do not invent vulnerabilities.
Do not claim that you executed or tested the code.

For each finding, provide:
- Issue type
- Severity: LOW, MEDIUM, HIGH, or CRITICAL
- Explanation
- Suggested fix

If no security vulnerabilities are identified, say so clearly.

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
        raise ValueError("Security auditor returned an empty response.")

    return result.strip()
