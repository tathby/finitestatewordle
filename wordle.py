from __future__ import annotations

from enum import Enum, auto
from typing import Callable


class RoundState(Enum):
    WORD_ENTRY = auto()
    CONFIRM = auto()
    SCORE = auto()
    IS_WINNER = auto()
    REVIEW = auto()
    CONFIRM_AFTER_REVIEW = auto()
    DISPLAY = auto()


class Wordle:
    def __init__(self, secret_word: str, input_func: Callable[[str], str] = input, output_func: Callable[[str], None] = print):
        if len(secret_word) != 5 or not secret_word.isalpha():
            raise ValueError("secret_word must be exactly 5 alphabetic letters")

        self.secret_word = secret_word.lower()
        self.attempt_count = 0
        self.has_won = False
        self.attempts: list[str] = []
        self._current_guess = ""
        self._input = input_func
        self._output = output_func

    def PlayRound(self) -> None:
        state = RoundState.WORD_ENTRY

        while True:
            if state == RoundState.WORD_ENTRY:
                guess = self._input("Enter a 5-letter guess: ").strip().lower()
                if len(guess) != 5 or not guess.isalpha():
                    self._output("Invalid guess. Please enter exactly five letters.")
                    continue

                self._current_guess = guess
                state = RoundState.CONFIRM

            elif state == RoundState.CONFIRM:
                confirm = self._input(f"Use '{self._current_guess}'? (y/n): ").strip().lower()
                if confirm in {"n", "no"}:
                    state = RoundState.WORD_ENTRY
                elif confirm in {"y", "yes"}:
                    state = RoundState.SCORE
                else:
                    self._output("Please answer with y or n.")

            elif state == RoundState.SCORE:
                self.Score()
                state = RoundState.IS_WINNER

            elif state == RoundState.IS_WINNER:
                self.has_won = self.IsWinner()
                if self.has_won:
                    state = RoundState.DISPLAY
                elif self.attempt_count >= 6:
                    state = RoundState.DISPLAY
                else:
                    state = RoundState.REVIEW

            elif state == RoundState.REVIEW:
                present_letters = sorted({ch for ch in self._current_guess if ch in self.secret_word})
                correct_positions = [
                    ch.upper() if self._current_guess[idx] == self.secret_word[idx] else "_"
                    for idx, ch in enumerate(self._current_guess)
                ]

                present = " ".join(letter.upper() for letter in present_letters) if present_letters else "None"
                self._output(f"Letters present in secret word: {present}")
                self._output(f"Correct position pattern: {' '.join(correct_positions)}")
                state = RoundState.CONFIRM_AFTER_REVIEW

            elif state == RoundState.CONFIRM_AFTER_REVIEW:
                self._input("Press Enter to continue to next guess...")
                state = RoundState.WORD_ENTRY

            elif state == RoundState.DISPLAY:
                self.Display()
                return

    def Score(self) -> None:
        self.attempts.append(self._current_guess)
        self.attempt_count += 1

    def IsWinner(self) -> bool:
        return self._current_guess == self.secret_word

    def Display(self) -> None:
        self._output("\nRound Complete")
        self._output("Attempts:")
        for index, attempt in enumerate(self.attempts, start=1):
            self._output(f"{index}. {attempt}")

        self._output(f"Total attempts: {self.attempt_count}")
        if self.has_won:
            self._output("You Won.")
        else:
            self._output("You Lost.")

        self._input("Press Enter to return to menu...")


def run() -> None:
    while True:
        print("\nWordle Main Menu")
        print("1) Play a round of Wordle")
        print("2) Leave")
        selection = input("Choose an option: ").strip()

        if selection == "2":
            print("Thanks for Playing and come back another time!")
            break

        if selection == "1":
            game = Wordle(secret_word="crane")
            game.PlayRound()
        else:
            print("Invalid selection. Please choose 1 or 2.")


if __name__ == "__main__":
    run()
