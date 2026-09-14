"""Regression coverage for legacy bugs identified during Ruff linting."""

import contextlib
import io
import runpy
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]


class LegacyScriptTests(unittest.TestCase):
    def run_player_win(self):
        """Play a deterministic fork without changing the interactive script."""
        output = io.StringIO()
        with (
            mock.patch("builtins.input", side_effect=["X", "1", "7", "9", "8", "n"]) as prompt,
            mock.patch("random.randint", return_value=1),
            mock.patch("random.choice", side_effect=lambda choices: choices[0]),
            contextlib.redirect_stdout(output),
        ):
            namespace = runpy.run_path(str(ROOT / "python/games/tic-tac-toe/main.py"))
        return namespace, output.getvalue(), prompt

    def test_player_win_ends_round_and_prompts_for_replay(self):
        _, output, prompt = self.run_player_win()
        self.assertIn("Congratulations! You won the game!", output)
        self.assertEqual(prompt.call_args.args, ("Do you want to play again (y/n): ",))

    def test_computer_blocks_the_opponent_for_either_letter(self):
        namespace, _, _ = self.run_player_win()
        for computer, player in [("X", "O"), ("O", "X")]:
            with self.subTest(computer=computer):
                board = [" "] * 10
                board[1] = board[2] = player
                original = board.copy()
                self.assertEqual(namespace["computerMove"](board, computer), 3)
                self.assertEqual(board, original)

    def test_flames_recovers_from_an_out_of_range_elimination_index(self):
        with (
            mock.patch("builtins.input", return_value="n"),
            mock.patch("sys.exit"),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            namespace = runpy.run_path(str(ROOT / "python/games/flames/main.py"))
        flames_type = namespace["Flames"]
        game = flames_type.__new__(flames_type)
        game.text = list("FLAMES")
        snapshots = []

        def stop_recursion(_count):
            snapshots.append(game.text.copy())
            game.text = ["F"]

        game.flgame = stop_recursion
        game.flcalc(7, 8)
        self.assertEqual(snapshots, [list("AMESF")])

    def test_statistics_script_loads_and_prints_grades_on_python3(self):
        namespace = runpy.run_path(str(ROOT / "python/exercises/statistics/exam_statistics.py"))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            namespace["print_grades"]([80, 90])
        self.assertEqual(output.getvalue(), "80\n90\n")


if __name__ == "__main__":
    unittest.main()
