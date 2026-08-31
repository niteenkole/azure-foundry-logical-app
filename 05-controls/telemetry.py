"""Safe operational telemetry for the PolicyDesk backend."""

import logging
import time
import uuid

logger = logging.getLogger("policy-assistant")


def start_trace() -> tuple[str, float]:
    """Create a request ID and start a latency timer.

    The ID lets an operator follow one request across logs without recording the
    user's question, which may contain sensitive business information.
    """
    return str(uuid.uuid4()), time.perf_counter()


def record_call(trace_id: str, model: str, started_at: float) -> None:
    """Record safe metadata after a successful model call."""
    logger.info(
        "model_call_complete",
        extra={
            "trace_id": trace_id,
            "model": model,
            "latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
        },
    )


def record_failure(trace_id: str, model: str, started_at: float) -> None:
    """Record a provider failure without logging the prompt or exception details."""
    logger.warning(
        "model_call_failed",
        extra={
            "trace_id": trace_id,
            "model": model,
            "latency_ms": round((time.perf_counter() - started_at) * 1000, 2),
        },
    )
