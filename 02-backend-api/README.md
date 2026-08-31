# Backend API

This service receives browser questions and calls the Azure AI Foundry model deployment. The browser never receives the Azure credential. Python is the implementation language for this API; the demo focus is the Azure AI application and its enterprise controls, not Python itself.

## Demo Routing Decision

The live recording will route requests to the new `policydesk-youtube-demo` agent created during the video, not directly to the base `policydesk-gpt-5-mini` deployment. 
The existing `niteen-test-policydesk` agent is a reference only.

```text
Frontend
	-> FastAPI connector
	-> AIProjectClient
	-> saved PolicyDesk agent
	-> instructions + knowledge source + model
```

Direct model invocation is retained only as a baseline explanation. If the connector calls the base deployment directly, it can behave like a general model and bypass the agent policy.

## Technology Used

### Python

Python is the backend language. It is concise for the demo and has mature libraries for HTTP APIs, validation, and Azure model access.

### FastAPI

FastAPI exposes the backend HTTP endpoints:

- `GET /health` confirms that the backend process is running.
- `POST /ask` receives a policy question and returns the model answer.

FastAPI also uses the type definitions in `main.py` to validate requests and shape responses.

### Uvicorn

Uvicorn is the local web server that runs the FastAPI application. This command starts the backend on port `8000`:

```bash
uvicorn main:app --reload --port 8000
```

The frontend sends requests to `http://127.0.0.1:8000/ask`.

### Pydantic

Pydantic validates the data crossing the API boundary:

- `AskRequest` requires a non-empty question with a maximum length of 2,000 characters.
- `AskResponse` guarantees that the frontend receives an `answer` field.

This keeps malformed input away from the model call and gives the frontend a predictable response shape.

### Azure AI Projects and OpenAI Responses API

The `azure-ai-projects` package creates an agent-bound OpenAI client for the saved PolicyDesk agent. The `openai` package then sends the validated question through the Responses API:

- The saved agent name and version.
- The user's validated question.

The project client creates an OpenAI client bound to the saved agent so the request uses the saved agent instructions and attached knowledge source. The browser never receives the project endpoint or Azure identity token.

### Microsoft Entra ID Authentication

The Foundry-generated Python sample uses `DefaultAzureCredential` and a bearer-token provider. This means the connector authenticates with an Azure identity instead of an API key. During local development, sign in with an identity supported by `DefaultAzureCredential`, such as Azure CLI or VS Code. The signed-in identity must have permission to invoke the model deployment.

The token scope used by the Foundry sample is:

```text
https://ai.azure.com/.default
```

### If the Application Is Hosted Outside Azure

The application does not have to run in Azure, but it still needs two things:

1. An Azure identity that can obtain a Microsoft Entra token.
2. A network route to the Foundry endpoint.

For an external host such as another cloud, an on-premises server, or a developer machine, use an identity method appropriate to that host:

- **Local development:** `az login`, VS Code sign-in, or another `DefaultAzureCredential` source.
- **External cloud with OIDC:** Microsoft Entra workload identity federation, preferred over a stored secret.
- **External server with a service principal:** certificate authentication is preferred; a client secret is a fallback and must be stored in the external platform's secret manager.
- **Private Foundry endpoint:** the external host must have private connectivity into Azure, such as VPN, ExpressRoute, or an approved cross-cloud private link.
- **Public Foundry endpoint:** the host needs outbound HTTPS access, and the Azure resource must permit the request path.

The request path is still:

```text
External application
	-> Entra token for https://ai.azure.com/.default
	-> Foundry OpenAI v1 endpoint
	-> Azure AI Foundry deployment
```

The important point is that hosting outside Azure does not remove Azure authorization. The external application's identity must be granted the appropriate Foundry/model invocation permission, and the endpoint must be reachable from its network.

Do not put an Azure API key in browser code. If an external host cannot use Entra workload identity, keep any fallback credential only in its server-side secret manager and rotate it through the organization's credential process.

### Azure AI Foundry

Azure AI Foundry provides the project and deployed model that generate the answer. The backend connects to it using these environment values:

```env
AZURE_AI_PROJECT_ENDPOINT
AZURE_AI_AGENT_NAME
```

For this hands-on stage, the endpoint is reachable from the local backend. Private networking is not required to run the application demonstration. The model version shown in Foundry is not an API version; the v1 endpoint pattern does not use the old `api-version` setting.

### CORS Middleware

FastAPI's CORS middleware allows the browser frontend to call the local backend during development. The current demo allows all origins for convenience; a production deployment should replace `*` with the exact approved frontend origin.

### Environment Variables and `.env`

The backend reads configuration from the process environment with Python's `os.environ`. For local development, `python-dotenv` loads the backend folder's `.env` when `main.py` starts. The API key is not hardcoded in `main.py`, and `.env` is ignored by Git.

## Explanation

backend sequence:

1. FastAPI creates the HTTP boundary between the browser and the model.
2. Pydantic validates the question and response contract.
3. The Azure AI Projects client creates an OpenAI client bound to the saved PolicyDesk agent.
4. The agent-bound OpenAI client sends the request through the Responses API.
5. Uvicorn runs the API locally so the frontend can call it.

The request path is:

```text
Browser frontend
	-> POST /ask
FastAPI backend
	-> OpenAI Foundry v1 client
Azure AI Foundry deployment
	-> response text
FastAPI backend
	-> JSON answer
Browser frontend
```

## Run

```bash
cd ai-demo/azure-foundry-logical-app/02-backend-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Keep this terminal activated before running Uvicorn. Confirm that Python and Uvicorn come from the backend virtual environment:

```bash
which python
which uvicorn
```

Both paths should contain:

```text
ai-demo/azure-foundry-logical-app/02-backend-api/.venv/
```

Set the values from the Azure AI Foundry model deployment in `02-backend-api/.env`. Restart Uvicorn after changing `.env`; it is loaded when the backend process starts.

Sign in before starting the backend so `DefaultAzureCredential` can obtain a token:

```bash
az login
```

Use this environment configuration:

```env
AZURE_AI_PROJECT_ENDPOINT=https://niteen-test-useast-01.services.ai.azure.com/api/projects/niteen-test-useast-01
AZURE_AI_AGENT_NAME=policydesk-youtube-demo
```

The project endpoint and agent name must match the saved agent's Foundry configuration. The installed SDK binds directly to the active named agent; no API version setting is used.

Do not use the base-model endpoint here:

```text
https://...services.ai.azure.com/openai/v1
```

That endpoint is for direct model deployment calls. The saved-agent project flow requires the project endpoint:

```text
https://...services.ai.azure.com/api/projects/<project-name>
```

If the backend returns `503` with an endpoint or agent configuration error, check the variable name first. It must be `AZURE_AI_PROJECT_ENDPOINT`, not `AZURE_AI_FOUNDRY_ENDPOINT`.

```bash
# Run this only after activating .venv in this same terminal.
uvicorn main:app --reload --port 8000
```

Check `http://127.0.0.1:8000/health`. The frontend should call `POST http://127.0.0.1:8000/ask`.

## Verify Foundry Access Before Testing the Chatbot

Run these checks after `az login` and before debugging the frontend. They verify identity, Azure role scope, token acquisition, endpoint alignment, and the direct Foundry request.

### 1. Confirm the active identity

```bash
az account show --query "{subscription:id, user:user.name, tenant:tenantId}" -o table
```

The signed-in user must be the identity that has access to the Foundry resource or project. Confirm it matches the account you used to create the Foundry project.

### 2. Get the signed-in user's object ID

```bash
USER_ID=$(az ad signed-in-user show --query id -o tsv)
echo "$USER_ID"
```

### 3. Inspect Foundry roles and scopes

```bash
az role assignment list \
	--assignee "$USER_ID" \
	--all \
	--include-inherited \
	--query "[?contains(roleDefinitionName, 'Foundry') || contains(roleDefinitionName, 'AI') || contains(roleDefinitionName, 'Cognitive') || contains(roleDefinitionName, 'OpenAI')].{Role:roleDefinitionName,Scope:scope}" \
	-o table
```

The role scope must match the same Foundry project used by `AZURE_AI_PROJECT_ENDPOINT`. For example, a role on `niteen-test-02` does not automatically grant access to a different project or resource.

### 4. Confirm the Entra token can be obtained

```bash
az account get-access-token \
	--resource https://ai.azure.com \
	--query "{tokenType:tokenType,expiresOn:expiresOn}" \
	-o table
```

Do not print or share the actual token.

### 5. Check the deployment and endpoint values without printing secrets

```bash
grep -E '^(AZURE_AI_PROJECT_ENDPOINT|AZURE_AI_AGENT_NAME)=' .env
```

For this Foundry v1 connection, the endpoint should look like:

```text
https://<resource>.services.ai.azure.com/api/projects/<project>
```

The deployment name must exist under the project/resource represented by that endpoint. The model version shown in Foundry is not an API version, and no `AZURE_OPENAI_API_VERSION` is used for this v1 connection.

### 6. Test the new demo agent directly, without the frontend

Load the non-secret `.env` values into the current shell and obtain a temporary Entra token. Do not echo the token:

```bash
set -a
source .env
set +a

TOKEN=$(az account get-access-token \
	--resource https://ai.azure.com \
	--query accessToken \
	-o tsv)
```

The Python connector uses the saved agent-bound client flow. Use the generated Foundry agent code or the agent-bound `AIProjectClient` path. Do not use a base-model `/responses` request for the live demo, because it bypasses the saved instructions and knowledge source.

```bash
curl -sS \
	-X POST "${AZURE_AI_FOUNDRY_ENDPOINT%/}/responses" \
	-H "Authorization: Bearer $TOKEN" \
	-H "Content-Type: application/json" \
	-d "{\"model\":\"$AZURE_OPENAI_DEPLOYMENT\",\"input\":\"Reply with exactly: Foundry access verified.\"}"
```

Expected result: a successful JSON response containing the model output.

### 6a. Clean up the temporary test environment

After the direct test, remove the token and exported values from the current terminal session:

```bash
unset TOKEN
unset AZURE_AI_PROJECT_ENDPOINT
unset AZURE_AI_AGENT_NAME
```

This does not delete `.env`. It only clears values from the current shell. Restarting the backend will load the saved `.env` values again through `python-dotenv`.

### 7. Test through FastAPI

After the direct Foundry request succeeds, start the connector:

```bash
cd ai-demo/azure-foundry-logical-app/02-backend-api

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

which python
which uvicorn
uvicorn main:app --reload --port 8000
```

Then call the API directly:

```bash
curl -sS \
	-X POST http://127.0.0.1:8000/ask \
	-H "Content-Type: application/json" \
	-d '{"question":"What approvals are needed before using an external AI model?"}'
```

### Interpreting failures

```text
401 = token or credential problem
403 = identity is authenticated but lacks Foundry/model permission
404 = endpoint, project, deployment, or route is wrong
400 API version not supported = old versioned client/path is being used; Foundry v1 does not use the model version as api-version
502 from FastAPI = the connector wrapped an upstream Foundry failure; read the backend traceback
```

The alignment that must be true is:

```text
Signed-in identity
		-> role assignment
		-> same Foundry resource/project
		-> same endpoint
		-> same deployment
		-> direct Foundry request succeeds
		-> FastAPI /ask succeeds
```
