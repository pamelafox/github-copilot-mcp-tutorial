import unittest
from unittest.mock import patch

from src.quiz import run_quiz


class QuizTests(unittest.TestCase):
    @patch("builtins.input", side_effect=["a", "c", "a", "b", "b"])
    def test_lowercase_answers_are_accepted(self, mock_input):
        with patch("builtins.print") as mock_print:
            run_quiz()

        output = "\n".join(call.args[0] for call in mock_print.call_args_list if call.args)
        self.assertIn("Quiz complete! Your score: 5/5", output)


if __name__ == "__main__":
    unittest.main()
