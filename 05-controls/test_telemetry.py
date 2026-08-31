import logging
import unittest
from unittest.mock import patch

from telemetry import record_call, record_failure, start_trace


class TelemetryTests(unittest.TestCase):
    # Every request needs a correlation ID and a timer so an operator can find
    # one request in the logs and measure how long the model call took.
    def test_start_trace_returns_id_and_timer(self):
        trace_id, started_at = start_trace()
        self.assertTrue(trace_id)
        self.assertIsInstance(started_at, float)

    # A successful event may include useful operational metadata, but it must
    # not include the user's question or any credential.
    @patch("telemetry.logger")
    def test_success_metadata_excludes_prompt(self, logger):
        record_call("trace-1", "policy-model", 0.0)
        metadata = logger.info.call_args.kwargs["extra"]
        self.assertEqual(metadata["trace_id"], "trace-1")
        self.assertNotIn("question", metadata)
        self.assertNotIn("api_key", metadata)

    # Failure events follow the same privacy rule. Debugging a failed call must
    # not turn the log into a copy of sensitive user input or secrets.
    @patch("telemetry.logger")
    def test_failure_metadata_excludes_prompt(self, logger):
        record_failure("trace-2", "policy-model", 0.0)
        metadata = logger.warning.call_args.kwargs["extra"]
        self.assertEqual(metadata["trace_id"], "trace-2")
        self.assertNotIn("question", metadata)
        self.assertNotIn("api_key", metadata)


if __name__ == "__main__":
    unittest.main()
