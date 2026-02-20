# finitestatewordle

A console-based Wordle simulator in Python where each round is controlled by a Finite State Machine (FSM).

## Requirements
- Python 3.10+

## How to run
From the project root:

```bash
python wordle.py
```

## How to play
1. Start the app and choose:
   - `1` to play a round
   - `2` to leave
2. During a round, enter a 5-letter guess.
3. At the guess prompt, you can also type:
   - `history` to show previous guesses with per-letter feedback
   - `quit` to end the current round early
4. Confirm each guess with `y` or `n`.
5. After each scored, non-winning guess, the game shows:
   - all previous guesses
   - per-letter indicators:
     - `[✓]` letter is in the correct position
     - `[?]` letter is in the word but wrong position
     - `[x]` letter is not in the word
6. Between guesses, choose:
   - `n` for next guess
   - `h` for history
   - `q` to quit the round
7. A round ends when you:
   - guess the secret word,
   - use all 6 attempts, or
   - quit early.

## Running tests
From the project root:

```bash
python -m unittest -v
```

## What is tested in `TestWordle`
The test class covers:
- Word bank quality:
  - `test_word_bank_is_long_and_five_letter` (bank length and valid 5-letter words)
- Secret-word selection:
  - `test_choose_secret_word_uses_chooser` (random chooser integration)
- Core Wordle behavior:
  - `test_is_winner_true`
  - `test_score_updates_attempts_and_count`
  - `test_evaluate_guess_handles_duplicates`
- FSM round flows:
  - `test_playround_wins`
  - `test_playround_loses_after_six_attempts`
  - `test_review_shows_feedback_for_previous_guesses`
  - `test_quit_from_word_entry`
  - `test_quit_after_review`
