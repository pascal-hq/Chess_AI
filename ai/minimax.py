from typing import Optional, Tuple
import math

from game.game_state import GameState
from game.move import Move
from game.piece import Color
from game.ai.evaluator import Evaluator


class MinimaxAI:
    def __init__(self, depth: int = 3):
        self.depth = depth

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------
    def choose_move(self, state: GameState) -> Optional[Move]:
        best_move = None

        if state.turn == Color.WHITE:
            best_score = -math.inf
        else:
            best_score = math.inf

        for move in state.get_legal_moves():
            state.make_move(move)
            score = self._minimax(
                state,
                depth=self.depth - 1,
                alpha=-math.inf,
                beta=math.inf,
                maximizing=(state.turn == Color.WHITE),
            )
            state.undo_move()

            if state.turn == Color.WHITE and score > best_score:
                best_score = score
                best_move = move

            elif state.turn == Color.BLACK and score < best_score:
                best_score = score
                best_move = move

        return best_move

    # --------------------------------------------------
    # Minimax Core
    # --------------------------------------------------
    def _minimax(
        self,
        state: GameState,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> float:

        if depth == 0:
            return Evaluator.evaluate(state)

        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return Evaluator.evaluate(state)

        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                state.make_move(move)
                eval_score = self._minimax(
                    state, depth - 1, alpha, beta, False
                )
                state.undo_move()

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break  # Alpha-Beta prune

            return max_eval

        else:
            min_eval = math.inf
            for move in legal_moves:
                state.make_move(move)
                eval_score = self._minimax(
                    state, depth - 1, alpha, beta, True
                )
                state.undo_move()

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break  # Alpha-Beta prune

            return min_eval
