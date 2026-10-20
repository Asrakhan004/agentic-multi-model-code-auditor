import litellm

import os
from dotenv import load_dotenv
from litellm import Router

load_dotenv()

router = Router(
    model_list=[
        {
            "model_name":"code-auditor",
            "litellm_params": {
                "model":"groq/openai/gpt-oss-20b",
                "api_key":os.getenv("GROQ_API_KEY")
            },
        }
    ]
)
response = router.completion(
    model="code-auditor",
    messages=[
        {
            "role": "user",
            "content": "Explain in one sentence what a SQL injection is."
        }
    ],
)

print(response.choices[0].message.content)