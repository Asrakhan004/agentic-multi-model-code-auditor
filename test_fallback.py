from router import router

print("Testing Gemini fallback...")

# Temporarily replace the primary deployment's model
# with an invalid model name in this test process.
for deployment in router.model_list:
    if deployment["model_name"] == "code-auditor":
        deployment["litellm_params"]["model"] = "groq/invalid-test-model"

try:
    response = router.completion(
        model="code-auditor",
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Fallback successful"
            }
        ],
    )

    print("\nResponse:")
    print(response.choices[0].message.content)
    print("\nReported model:")
    print(response.model)

except Exception as e:
    print("\nFallback test failed:")
    print(repr(e))

