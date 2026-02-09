from game.piece import PieceType, Color
from game.game_state import GameState


class Evaluator:
    # Basic material values
    PIECE_VALUES = {
        PieceType.PAWN: 1,
        PieceType.KNIGHT: 3,
        PieceType.BISHOP: 3,
        PieceType.ROOK: 5,
        PieceType.QUEEN: 9,
        PieceType.KING: 0,  # king value handled via checkmate
    }

    @staticmethod
    def evaluate(state: GameState) -> float:
        """
        Positive score = White advantage
        Negative score = Black advantage
        """

        # Checkmate
        legal_moves = state.get_legal_moves()
        if not legal_moves:
            if state.is_in_check(state.turn):
                # Current player is checkmated
                return -9999 if state.turn == Color.WHITE else 9999
            else:
                # Stalemate
                return 0

        score = 0.0

        # Material evaluation
        for row in range(8):
            for col in range(8):
                piece = state.board.get_piece((row, col))
                if piece:
                    value = Evaluator.PIECE_VALUES[piece.type]
                    if piece.color == Color.WHITE:
                        score += value
                    else:
                        score -= value

        return score
