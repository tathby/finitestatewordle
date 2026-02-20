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
