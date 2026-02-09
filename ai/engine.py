from game.state import GameState
from game.piece import Color
from ai.minimax import MinimaxAI


class ChessAI:
    def __init__(self, color: Color, depth: int = 3):
        self.color = color
        self.depth = depth
        self.ai = MinimaxAI(depth=self.depth)

    def choose_move(self, state: GameState):
        """
        Returns the best move for this AI's color given the current GameState.
        """
        # Ensure the AI only chooses moves for its own color
        if state.turn != self.color:
            return None

        return self.ai.choose_move(state)
