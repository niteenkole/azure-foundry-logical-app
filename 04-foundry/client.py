"""Azure AI Foundry model integration used by the backend API."""

import os
import logging

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

logger = logging.getLogger("policy-assistant.foundry")


class FoundryConfigurationError(RuntimeError):
    """Raised when the backend cannot build a configured Foundry client."""


class FoundryRequestError(RuntimeError):
    """Raised when the model provider rejects or cannot complete a request."""


def complete_chat(question: str) -> str:
    """Send one governed question to the configured Foundry deployment.

    The saved PolicyDesk agent owns the instructions and knowledge source. The
    local connector sends the question through the agent-bound Responses client
    rather than calling the base model.
    """
    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    agent_name = os.environ.get("AZURE_AI_AGENT_NAME")
    if not endpoint or not agent_name:
        raise FoundryConfigurationError("Azure AI project endpoint or agent name is not configured")

    try:
        # DefaultAzureCredential uses Azure CLI locally and managed identity when hosted.
        with DefaultAzureCredential() as credential, AIProjectClient(
            endpoint=endpoint,
            credential=credential,
            allow_preview=True,
        ) as project_client:
            # This client is bound to the saved agent and its knowledge source.
            # The installed SDK supports direct agent invocation; session state
            # is optional and is not required for this single-question demo.
            openai_client = project_client.get_openai_client(agent_name=agent_name)
            response = openai_client.responses.create(input=question)
    except FoundryConfigurationError:
        raise
    except Exception as error:
        # Keep the browser message generic, but preserve the provider error in
        # the backend terminal so configuration failures can be diagnosed.
        logger.exception("Foundry request failed: %s", type(error).__name__)
        raise FoundryRequestError("Azure AI Foundry request failed") from error

    answer = response.output_text
    if not answer:
        raise FoundryRequestError("The model returned an empty response")
    return answer
