
import json
from pydantic import BaseModel
from router import router


class AuditPlan(BaseModel):
    security: bool
    bugs: bool
    performance: bool


def plan_audit(code: str) -> AuditPlan:
    prompt = f"""
You are a code-audit planner.

Decide which types of analysis are needed for this Python code:

- security
- bugs
- performance

Select true for relevant audit types and false for unnecessary ones.
When uncertain, select true rather than skipping a potentially useful audit.

Return ONLY valid JSON in this format:
{{
    "security": true,
    "bugs": true,
    "performance": false
}}

Python code:
```python
{code}
```
"""

    response = router.completion(
        model="code-auditor",
        messages=[{"role": "user", "content": prompt}],
    )

    raw_result = response.choices[0].message.content

    if not raw_result:
        raise ValueError("Planner returned an empty response.")

    raw_result = raw_result.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw_result)

    return AuditPlan(**result)

