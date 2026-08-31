# Step 5: Controls and Telemetry

This folder adds operational visibility around the model call without writing secrets or full prompts to ordinary application logs.

## What It Does

- Creates a trace ID for each request.
- Measures model-call latency.
- Records the selected deployment name.
- Records successful and failed model calls.
- Excludes the user's question and API key from telemetry metadata.

## Explanation

"The final layer makes the application operable. We need to know which request completed, which deployment handled it, and how long it took. We deliberately do not log the prompt or credential because prompts may contain sensitive business data and credentials must never enter logs."

## Run The Tests

```bash
cd ai-demo/azure-foundry-logical-app/05-controls
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_telemetry.py
```

## Request Flow

```text
POST /ask
    -> start_trace()
    -> Azure AI Foundry call
    -> record_call() on success
    -> record_failure() on configuration/provider failure
```
