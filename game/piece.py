from enum import Enum, auto


class Color(Enum):
    WHITE = auto()
    BLACK = auto()

    def opposite(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class PieceType(Enum):
    PAWN = auto()
    ROOK = auto()
    KNIGHT = auto()
    BISHOP = auto()
    QUEEN = auto()
    KING = auto()


class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.type = piece_type
        self.color = color
        self.has_moved = False  # Needed for castling, pawn first move

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------
    def copy(self):
        p = Piece(self.type, self.color)
        p.has_moved = self.has_moved
        return p

    # --------------------------------------------------
    # Debug / Display
    # --------------------------------------------------
    def __repr__(self):
        color = "W" if self.color == Color.WHITE else "B"
        return f"{color}{self.type.name[0]}"
