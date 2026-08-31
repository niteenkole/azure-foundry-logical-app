import unittest

from guardrails import MAX_QUESTION_LENGTH, validate_question


class GuardrailsTests(unittest.TestCase):
    def test_strips_surrounding_whitespace(self):
        self.assertEqual(validate_question("  What needs approval?  "), "What needs approval?")

    def test_rejects_blank_question(self):
        with self.assertRaisesRegex(ValueError, "Question required"):
            validate_question("   ")

    def test_rejects_question_that_is_too_long(self):
        with self.assertRaisesRegex(ValueError, "Question too long"):
            validate_question("x" * (MAX_QUESTION_LENGTH + 1))


if __name__ == "__main__":
    unittest.main()
