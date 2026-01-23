from typing import Optional, Tuple, List
from game.piece import Piece, PieceType, Color

Position = Tuple[int, int]


class Board:
    def __init__(self):
        # 8x8 board
        self.grid: List[List[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

        self.white_king_pos: Position = (7, 4)
        self.black_king_pos: Position = (0, 4)

        self.en_passant_target: Optional[Position] = None

        self._setup_board()

    # --------------------------------------------------
    # Initial Setup
    # --------------------------------------------------
    def _setup_board(self):
        # Pawns
        for col in range(8):
            self.grid[6][col] = Piece(PieceType.PAWN, Color.WHITE)
            self.grid[1][col] = Piece(PieceType.PAWN, Color.BLACK)

        # Rooks
        self.grid[7][0] = self.grid[7][7] = Piece(PieceType.ROOK, Color.WHITE)
        self.grid[0][0] = self.grid[0][7] = Piece(PieceType.ROOK, Color.BLACK)

        # Knights
        self.grid[7][1] = self.grid[7][6] = Piece(PieceType.KNIGHT, Color.WHITE)
        self.grid[0][1] = self.grid[0][6] = Piece(PieceType.KNIGHT, Color.BLACK)

        # Bishops
        self.grid[7][2] = self.grid[7][5] = Piece(PieceType.BISHOP, Color.WHITE)
        self.grid[0][2] = self.grid[0][5] = Piece(PieceType.BISHOP, Color.BLACK)

        # Queens
        self.grid[7][3] = Piece(PieceType.QUEEN, Color.WHITE)
        self.grid[0][3] = Piece(PieceType.QUEEN, Color.BLACK)

        # Kings
        self.grid[7][4] = Piece(PieceType.KING, Color.WHITE)
        self.grid[0][4] = Piece(PieceType.KING, Color.BLACK)

    # --------------------------------------------------
    # Board Helpers
    # --------------------------------------------------
    def in_bounds(self, pos: Position) -> bool:
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, pos: Position) -> Optional[Piece]:
        row, col = pos
        return self.grid[row][col]

    def set_piece(self, pos: Position, piece: Optional[Piece]):
        row, col = pos
        self.grid[row][col] = piece

    def is_empty(self, pos: Position) -> bool:
        return self.get_piece(pos) is None

    # --------------------------------------------------
    # Move Piece
    # --------------------------------------------------
    def move_piece(self, start: Position, end: Position):
        piece = self.get_piece(start)
        self.set_piece(end, piece)
        self.set_piece(start, None)

        # Track king position
        if piece and piece.type == PieceType.KING:
            if piece.color == Color.WHITE:
                self.white_king_pos = end
            else:
                self.black_king_pos = end
