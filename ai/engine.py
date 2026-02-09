from game.state import GameState
from game.piece import Color
from ai.minimax import find_best_move

class ChessAI:
    def __init__(self, color: Color, depth: int = 3):
        self.color = color
        self.depth = depth

    def choose_move(self, state: GameState):
        return find_best_move(state, self.color, self.depth)
