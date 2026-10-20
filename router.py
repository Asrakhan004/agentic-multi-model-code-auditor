
import os
from dotenv import load_dotenv
from litellm import Router

load_dotenv()

router = Router(
    model_list=[
        {
            "model_name": "code-auditor",
            "litellm_params": {
                "model": "groq/openai/gpt-oss-20b",
                "api_key": os.getenv("GROQ_API_KEY"),
            },
        },
          {
            "model_name": "gemini-backup",
            "litellm_params": {
                "model": "gemini/gemini-3.5-flash-lite",
                "api_key": os.getenv("GEMINI_API_KEY"),
                "order": 2,
            },
        },
    ],
    fallbacks=[
        {"code-auditor": ["gemini-backup"]}
    ],
    num_retries=1,
)
