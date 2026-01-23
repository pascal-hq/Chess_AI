from typing import Optional, Tuple
from game.piece import Piece, PieceType

Position = Tuple[int, int]


class Move:
    def __init__(
        self,
        start: Position,
        end: Position,
        piece: Piece,
        captured: Optional[Piece] = None,
        promotion: Optional[str] = None,
        is_castling: bool = False,
        is_en_passant: bool = False,
    ):
        self.start = start
        self.end = end
        self.piece = piece
        self.captured = captured

        # Special move flags
        self.promotion = promotion        # 'q', 'r', 'b', 'n'
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant

        # Stored for undo
        self.previous_en_passant = None
        self.previous_castling_rights = None
        self.previous_has_moved = False

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------
    def is_capture(self) -> bool:
        return self.captured is not None

    def is_promotion(self) -> bool:
        return self.promotion is not None

    # --------------------------------------------------
    # Debug / Display
    # --------------------------------------------------
    def __repr__(self):
        return (
            f"Move({self.start} -> {self.end}, "
            f"{self.piece.type.name}, "
            f"capture={self.captured is not None}, "
            f"promotion={self.promotion}, "
            f"castling={self.is_castling}, "
            f"en_passant={self.is_en_passant})"
        )
