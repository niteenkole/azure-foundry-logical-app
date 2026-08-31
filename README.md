# Azure AI Foundry Enterprise Policy Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A reference implementation of an enterprise policy assistant built with Azure AI Foundry and a
small FastAPI connector. Clone it to explore an agent that answers only from approved, grounded
policy documents while keeping Azure credentials out of browser code.

The application-specific AI behavior belongs in Azure AI Foundry: model deployment, agent
instructions, knowledge grounding, and refusal behavior. Python provides the local API boundary
between the browser and Foundry.

## Quick Start

### Prerequisites

- Python 3.10 or later.
- Azure CLI, signed in with an identity that can access your Azure AI Foundry project.
- An Azure AI Foundry project, an agent, and a deployed model.

### Run locally

```bash
git clone https://github.com/niteenkole/azure-foundry-logical-app.git
cd azure-foundry-logical-app/02-backend-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
az login
uvicorn main:app --reload --port 8000
```

Before starting the server, update `.env` with your own Foundry project endpoint and agent name:

```env
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project-name>
AZURE_AI_AGENT_NAME=<your-agent-name>
```

Open `01-frontend/index.html` in a browser and submit a policy question. The backend health check
is available at `http://127.0.0.1:8000/health`.

Never commit `.env`. It contains environment-specific configuration and is excluded by
`.gitignore`.

## Flow

```text
Browser frontend -> Backend API -> Application policy -> Azure AI Foundry -> Chat model
```

The current demo uses a reachable Foundry endpoint so the application can be built and tested without private networking. The backend owns the credential, validates requests, applies policy, and calls the model.

Production hardening is presented as a later phase:

```text
Private application/backend -> Private Endpoint -> Azure AI Foundry
```

The root [index.html](index.html) and [build_guide.html](build_guide.html) files are optional
architecture visualizations. They are not required to run the application.

## Build Pages

- `01-frontend/index.html` - chatbot frontend
- `02-backend-api/index.html` - trusted API boundary and server-side credential
- `03-policy/index.html` - input validation, instructions, and response contract
- `04-foundry/index.html` - Azure AI Foundry model deployment call
- `05-controls/index.html` - telemetry, safety handling, and cost controls
- `06-policy-knowledge-base/index.html` - Azure storage, search, and Foundry grounding
- `06-policy-knowledge-base/` - synthetic policy source data for upload into Azure

The policy files are synthetic source content for upload into Azure AI Foundry. We will not build a local Python document-search engine or add Azure API Management. The local API stays simple; the AI workflow belongs inside Foundry.

Each numbered page is a visual drawing board with the implementation flow on the left and the
related code or artifact on the right.
