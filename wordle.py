from __future__ import annotations

import random
from enum import Enum, auto
from typing import Callable, Sequence


WORD_BANK: tuple[str, ...] = (
    "abide", "adore", "agent", "aisle", "amber", "angel", "apple", "arena", "argue", "armor",
    "badge", "baker", "basic", "beach", "beard", "began", "belly", "bench", "berry", "bingo",
    "black", "blade", "blame", "blank", "blast", "blend", "bless", "blind", "blink", "block",
    "bloom", "blown", "board", "boast", "boost", "bound", "brain", "brake", "brand", "brave",
    "bread", "break", "brick", "bride", "brief", "bring", "broad", "broke", "brown", "brush",
    "cabin", "cable", "camel", "candy", "caper", "cargo", "carve", "catch", "cause", "chain",
    "chair", "charm", "chase", "cheap", "check", "chest", "chief", "child", "chime", "choir",
    "claim", "class", "clean", "clear", "clerk", "click", "cliff", "climb", "clock", "close",
    "cloud", "coast", "color", "comic", "couch", "could", "count", "court", "cover", "craft",
    "crane", "crash", "cream", "crime", "crisp", "cross", "crowd", "crown", "curve", "cycle",
    "dance", "dealt", "delay", "depth", "diary", "digit", "diner", "doubt", "dozen", "draft",
    "drain", "drama", "dream", "dress", "drift", "drink", "drive", "drove", "eager", "eagle",
    "early", "earth", "elite", "enjoy", "entry", "equal", "error", "event", "exact", "exist",
    "faith", "fancy", "favor", "feast", "fence", "field", "final", "flame", "flash", "fleet",
    "floor", "focus", "force", "frame", "fresh", "front", "frost", "fruit", "ghost", "giant",
    "glade", "globe", "grace", "grade", "grain", "grand", "grant", "grape", "graph", "grasp",
    "great", "green", "grief", "gross", "group", "guard", "guest", "guide", "habit", "happy",
    "heart", "heavy", "honey", "horse", "hotel", "house", "human", "humor", "ideal", "image",
    "index", "inner", "input", "issue", "ivory", "jelly", "joint", "judge", "juice", "knock",
    "known", "label", "labor", "laser", "later", "laugh", "layer", "learn", "least", "leave",
    "legal", "lemon", "level", "light", "limit", "local", "logic", "loose", "lucky", "lunch",
    "magic", "major", "maker", "march", "match", "maybe", "medal", "mercy", "metal", "might",
    "minor", "model", "money", "month", "moral", "motor", "mount", "mouse", "mouth", "movie",
    "music", "naive", "nerve", "never", "night", "noble", "noise", "north", "novel", "nurse",
    "ocean", "offer", "olive", "orbit", "order", "organ", "other", "ought", "outer", "owner",
    "panel", "party", "peace", "phone", "photo", "piece", "pilot", "pitch", "plain", "plane",
    "plant", "plate", "point", "pound", "power", "press", "price", "pride", "prime", "print",
    "prize", "proof", "proud", "queen", "quick", "quiet", "quite", "radio", "raise", "range",
    "rapid", "ratio", "reach", "react", "ready", "refer", "reply", "right", "rival", "river",
    "robot", "rough", "round", "route", "royal", "rural", "saint", "scale", "scene", "scope",
    "score", "sense", "serve", "shade", "shake", "shall", "shape", "share", "sharp", "sheep",
    "sheet", "shelf", "shell", "shift", "shine", "shirt", "shock", "shoot", "shore", "short",
    "shown", "sight", "since", "skill", "sleep", "slice", "slide", "slope", "small", "smart",
    "smile", "smoke", "solid", "solve", "sound", "south", "space", "spare", "speak", "speed",
    "spend", "spice", "spike", "spite", "split", "sport", "spray", "staff", "stage", "stair",
    "stake", "stand", "stare", "start", "state", "steam", "steel", "stick", "still", "stock",
    "stone", "store", "storm", "story", "strip", "stuck", "study", "stuff", "style", "sugar",
    "table", "taste", "teach", "tease", "thank", "their", "theme", "there", "thick", "thing",
    "think", "third", "those", "three", "throw", "tight", "tired", "title", "today", "token",
    "topic", "total", "touch", "tough", "tower", "track", "trade", "train", "treat", "trend",
    "trial", "tribe", "trick", "truck", "truly", "trust", "truth", "twice", "under", "union",
    "unity", "until", "upper", "urban", "usage", "usual", "valid", "value", "video", "visit",
    "vital", "voice", "waste", "watch", "water", "wheel", "where", "which", "while", "white",
    "whole", "whose", "woman", "world", "worry", "worth", "would", "write", "wrong", "young",
    "youth", "zebra",
)


class RoundState(Enum):
    WORD_ENTRY = auto()
    CONFIRM = auto()
    SCORE = auto()
    IS_WINNER = auto()
    REVIEW = auto()
    CONFIRM_AFTER_REVIEW = auto()
    DISPLAY = auto()


def choose_secret_word(
    word_bank: Sequence[str] = WORD_BANK,
    chooser: Callable[[Sequence[str]], str] = random.choice,
) -> str:
    if not word_bank:
        raise ValueError("word_bank must contain at least one word")
    return chooser(word_bank)


class Wordle:
    def __init__(
        self,
        secret_word: str,
        input_func: Callable[[str], str] = input,
        output_func: Callable[[str], None] = print,
    ):
        if len(secret_word) != 5 or not secret_word.isalpha():
            raise ValueError("secret_word must be exactly 5 alphabetic letters")

        self.secret_word = secret_word.lower()
        self.attempt_count = 0
        self.has_won = False
        self.has_quit = False
        self.attempts: list[str] = []
        self._current_guess = ""
        self._input = input_func
        self._output = output_func

    def PlayRound(self) -> None:
        state = RoundState.WORD_ENTRY

        while True:
            if state == RoundState.WORD_ENTRY:
                guess = self._input(
                    "Enter a 5-letter guess (or type 'history' / 'quit'): "
                ).strip().lower()

                if self._handle_round_command(guess):
                    if self.has_quit:
                        state = RoundState.DISPLAY
                    continue

                if len(guess) != 5 or not guess.isalpha():
                    self._output("Invalid guess. Please enter exactly five letters.")
                    continue

                self._current_guess = guess
                state = RoundState.CONFIRM

            elif state == RoundState.CONFIRM:
                confirm = self._input(
                    f"Use '{self._current_guess}'? (y/n, or 'quit'): "
                ).strip().lower()

                if confirm in {"q", "quit", "exit"}:
                    self.has_quit = True
                    state = RoundState.DISPLAY
                elif confirm in {"n", "no"}:
                    state = RoundState.WORD_ENTRY
                elif confirm in {"y", "yes"}:
                    state = RoundState.SCORE
                else:
                    self._output("Please answer with y or n (or quit).")

            elif state == RoundState.SCORE:
                self.Score()
                state = RoundState.IS_WINNER

            elif state == RoundState.IS_WINNER:
                self.has_won = self.IsWinner()
                if self.has_won or self.attempt_count >= 6:
                    state = RoundState.DISPLAY
                else:
                    state = RoundState.REVIEW

            elif state == RoundState.REVIEW:
                self._output("\nGuess review:")
                self._display_attempt_history()
                self._output("Legend: [✓]=right letter/right spot  [?]=in word/wrong spot  [x]=not in word")
                state = RoundState.CONFIRM_AFTER_REVIEW

            elif state == RoundState.CONFIRM_AFTER_REVIEW:
                action = self._input(
                    "Next action: (n)ext guess, (h)istory, or (q)uit: "
                ).strip().lower()

                if action in {"n", "next", ""}:
                    state = RoundState.WORD_ENTRY
                elif action in {"h", "history"}:
                    self._output("\nPrevious guesses with letter feedback:")
                    self._display_attempt_history(show_header=False)
                elif action in {"q", "quit", "exit"}:
                    self.has_quit = True
                    state = RoundState.DISPLAY
                else:
                    self._output("Invalid option. Choose n, h, or q.")

            elif state == RoundState.DISPLAY:
                self.Display()
                return

    def _handle_round_command(self, command: str) -> bool:
        if command in {"q", "quit", "exit"}:
            self.has_quit = True
            return True

        if command in {"h", "history"}:
            self._output("\nPrevious guesses with letter feedback:")
            self._display_attempt_history(show_header=False)
            return True

        return False

    def Score(self) -> None:
        self.attempts.append(self._current_guess)
        self.attempt_count += 1

    def IsWinner(self) -> bool:
        return self._current_guess == self.secret_word

    def _evaluate_guess(self, guess: str) -> list[str]:
        statuses = ["absent"] * 5
        secret_remaining: dict[str, int] = {}

        for idx, letter in enumerate(self.secret_word):
            if guess[idx] == letter:
                statuses[idx] = "correct"
            else:
                secret_remaining[letter] = secret_remaining.get(letter, 0) + 1

        for idx, letter in enumerate(guess):
            if statuses[idx] == "correct":
                continue

            remaining = secret_remaining.get(letter, 0)
            if remaining > 0:
                statuses[idx] = "present"
                secret_remaining[letter] = remaining - 1

        return statuses

    def _format_guess_feedback(self, guess: str) -> str:
        markers = {
            "correct": "✓",
            "present": "?",
            "absent": "x",
        }

        statuses = self._evaluate_guess(guess)
        pieces = [f"{letter.upper()}[{markers[state]}]" for letter, state in zip(guess, statuses)]
        return " ".join(pieces)

    def _display_attempt_history(self, show_header: bool = True) -> None:
        if show_header:
            self._output("Previous guesses with letter feedback:")

        if not self.attempts:
            self._output("No guesses yet.")
            return

        for index, attempt in enumerate(self.attempts, start=1):
            self._output(f"{index}. {self._format_guess_feedback(attempt)}")

    def Display(self) -> None:
        self._output("\nRound Complete")
        self._display_attempt_history()
        self._output(f"Total attempts: {self.attempt_count}")

        if self.has_won:
            self._output("You Won.")
        elif self.has_quit:
            self._output("Round ended early. You quit.")
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
            game = Wordle(secret_word=choose_secret_word())
            game.PlayRound()
        else:
            print("Invalid selection. Please choose 1 or 2.")


if __name__ == "__main__":
    run()
