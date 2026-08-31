# Step 4: Azure AI Foundry Integration

This folder owns the saved-agent integration. The backend passes a validated question into `complete_chat()`. The saved agent owns the AI instructions and knowledge grounding; the local connector sends the request through the agent-bound Responses API.

## Agent-Bound Request Path

```text
AIProjectClient -> configured agent -> instructions + knowledge -> grounded response
```

The agent is the reusable Azure AI configuration that keeps the policy-only behavior and knowledge
source attached to the application request.

## What This Module Does

1. Reads the Foundry project endpoint, agent name, and version from the backend environment.
2. Creates an `AIProjectClient` with `DefaultAzureCredential`.
3. Gets an agent-bound `OpenAI` client from the project client.
4. Sends the validated question through the Responses API.
4. Extracts the model's answer text.
5. Converts configuration and provider failures into explicit exceptions for the API route.

The frontend does not know the deployment name and never receives the API key.

## Model Choice

Create an agent in your Foundry project and connect it to a model deployment available in your
region. The connector targets the agent, not the model deployment directly, so the agent
instructions and attached knowledge source are applied.

Model availability and pricing vary by region, deployment type, quota, and date. Review the Azure
AI Foundry Model Catalog for current availability and pricing before choosing a deployment.

Suggested starting values:

```text
Agent name: <your-agent-name>
Agent version: latest
Underlying model: gpt-5-mini
Purpose: short grounded enterprise-policy answers
Output cap: 800 completion tokens for GPT-5
Usage: small development workload
```

Keep the deployment name separate from the model name. The application sends the deployment name; Azure maps that deployment to the selected model.

## Create the Model Deployment in Foundry

1. Open the Azure AI Foundry project.
2. Create the new agent and open its details.
3. Confirm the agent's model deployment is `gpt-5-mini`.
4. Confirm that the model is available in the selected region.
5. Review the displayed pricing, quota, supported features, and terms.
6. Choose the deployment option.
7. Record the agent name and active version shown in Foundry.
8. Use the smallest practical capacity for the manual demo.
9. Create the deployment and wait until its status is ready.
10. Open the deployment details and copy the endpoint, deployment name, and selected API version.

Do not paste credentials into the video recording. This connector follows the Foundry-generated Entra ID sample, so it uses `DefaultAzureCredential` rather than an API key.

## Configure the Local Connector

Set the values in the backend environment, not in source code:

```env
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
AZURE_AI_AGENT_NAME=<your-agent-name>
```

The project endpoint and agent name must match the saved agent. Never commit `.env` or print
credentials in a terminal.

## Test the Deployment Before the Chatbot

1. Start the backend.
2. Call the health endpoint to confirm the local connector is alive.
3. Submit one short question from the chatbot.
4. Confirm the backend status changes from `BACKEND NOT CONNECTED` to a successful Azure response.
5. If the request fails, check the deployment name, endpoint, API version, key, region availability, quota, and backend logs without exposing secrets.

## Configuration

```env
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project-name>
AZURE_AI_AGENT_NAME=<your-agent-name>
```

## Live Check

Start the backend from the backend folder:

```bash
cd ai-demo/azure-foundry-logical-app/02-backend-api
uvicorn main:app --reload --port 8000
```

Then submit a question in the frontend. The request path is:

```text
Browser
  -> POST /ask
FastAPI + guardrails
  -> complete_chat()
AIProjectClient
  -> Azure AI Foundry agent
  -> answer text
Browser
```

No credentials are stored in `client.py`; `.env` and shell environment values stay outside source code.
