from typing import Optional
import math

from game.state import GameState
from game.move import Move
from game.piece import Color
from ai.evaluator import Evaluator  # Use your evaluation module


class MinimaxAI:
    def __init__(self, depth: int = 3):
        self.depth = depth

    # ---------------- Public API ----------------
    def choose_move(self, state: GameState) -> Optional[Move]:
        """
        Chooses the best move for the current turn using minimax with alpha-beta pruning.
        """
        best_move: Optional[Move] = None
        maximizing = state.turn == Color.WHITE
        best_score = -math.inf if maximizing else math.inf

        for move in state.get_legal_moves():
            state.make_move(move)
            score = self._minimax(
                state,
                depth=self.depth - 1,
                alpha=-math.inf,
                beta=math.inf,
                maximizing=not maximizing,  # next level
            )
            state.undo_move()

            if maximizing and score > best_score:
                best_score = score
                best_move = move
            elif not maximizing and score < best_score:
                best_score = score
                best_move = move

        return best_move

    # ---------------- Minimax Core ----------------
    def _minimax(
        self,
        state: GameState,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool
    ) -> float:
        """
        Recursively evaluates moves using minimax with alpha-beta pruning.
        """
        # Terminal conditions
        if depth == 0 or state.is_checkmate() or state.is_stalemate():
            return Evaluator.evaluate(state)

        legal_moves = state.get_legal_moves()
        if not legal_moves:
            return Evaluator.evaluate(state)

        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                state.make_move(move)
                eval_score = self._minimax(state, depth - 1, alpha, beta, False)
                state.undo_move()

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            return max_eval
        else:
            min_eval = math.inf
            for move in legal_moves:
                state.make_move(move)
                eval_score = self._minimax(state, depth - 1, alpha, beta, True)
                state.undo_move()

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-Beta pruning
            return min_eval
