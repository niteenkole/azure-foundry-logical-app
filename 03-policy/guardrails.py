"""Application policy enforced before requests reach Azure AI Foundry.

This module is the small request checkpoint between the browser and Azure AI
Foundry. It handles only deterministic HTTP safeguards. AI behavior and system
instructions are configured in Azure AI Foundry, not hardcoded here.
"""

# The application rejects unusually large questions before they consume model
# tokens or create an unexpectedly expensive request.
MAX_QUESTION_LENGTH = 2000

def validate_question(question: str) -> str:
    """Normalize and check one question before it reaches the model.

    The backend passes the browser's question into this function. A valid value
    is returned to the route, which sends it to the Azure AI Foundry agent or
    model configured for the demo. A rejected value raises ValueError, allowing
    the API route to return a clear client error without making an AI call.
    """

    # Remove accidental spaces and line breaks so equivalent questions are
    # handled consistently and the model receives clean input.
    normalized = question.strip()
    if not normalized:
        # This is a deterministic application decision, not a model decision.
        raise ValueError("Question required")
    if len(normalized) > MAX_QUESTION_LENGTH:
        # Keeping the limit here protects cost, latency, and the model context.
        raise ValueError("Question too long")

    # Future HTTP-level checks belong here. AI behavior changes belong in the
    # Azure AI Foundry agent instructions and should be tested there.
    return normalized
