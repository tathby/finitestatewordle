import unittest

from wordle import Wordle


class TestWordle(unittest.TestCase):
    def test_is_winner_true(self):
        game = Wordle("crane", input_func=lambda _: "", output_func=lambda _: None)
        game._current_guess = "crane"
        self.assertTrue(game.IsWinner())

    def test_score_updates_attempts_and_count(self):
        game = Wordle("crane", input_func=lambda _: "", output_func=lambda _: None)
        game._current_guess = "slate"
        game.Score()
        self.assertEqual(1, game.attempt_count)
        self.assertEqual(["slate"], game.attempts)

    def test_evaluate_guess_handles_duplicates(self):
        game = Wordle("eerie", input_func=lambda _: "", output_func=lambda _: None)
        self.assertEqual(
            ["present", "correct", "absent", "present", "absent"],
            game._evaluate_guess("refer"),
        )

    def test_playround_wins(self):
        entries = iter([
            "crane",  # word entry
            "y",      # confirm
            "",       # display pause
        ])
        outputs = []

        game = Wordle("crane", input_func=lambda _: next(entries), output_func=outputs.append)
        game.PlayRound()

        self.assertTrue(game.has_won)
        self.assertEqual(1, game.attempt_count)
        self.assertIn("You Won.", outputs)
        self.assertTrue(any("C[✓]" in message for message in outputs))

    def test_review_shows_feedback_for_previous_guesses(self):
        entries = iter([
            "slate", "y", "",
            "crane", "y", "",
        ])
        outputs = []

        game = Wordle("crane", input_func=lambda _: next(entries), output_func=outputs.append)
        game.PlayRound()

        slate_rows = [message for message in outputs if "S[x] L[x] A[✓] T[x] E[✓]" in message]
        crane_rows = [message for message in outputs if "C[✓] R[✓] A[✓] N[✓] E[✓]" in message]
        self.assertTrue(slate_rows, "expected first guess feedback in review output")
        self.assertTrue(crane_rows, "expected winning guess feedback in display output")

    def test_playround_loses_after_six_attempts(self):
        entries = iter([
            "slate", "y", "",
            "pride", "y", "",
            "ghost", "y", "",
            "flint", "y", "",
            "mound", "y", "",
            "vibes", "y", "",
            "",  # display pause
        ])
        outputs = []

        game = Wordle("crane", input_func=lambda _: next(entries), output_func=outputs.append)
        game.PlayRound()

        self.assertFalse(game.has_won)
        self.assertEqual(6, game.attempt_count)
        self.assertIn("You Lost.", outputs)


if __name__ == "__main__":
    unittest.main()
