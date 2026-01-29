from typing import List, Tuple
from game.piece import Piece, PieceType, Color
from game.board import Board, Position
from game.move import Move

class Rules:
    def __init__(self, board: Board):
        self.board = board

    # ---------------- Helpers ----------------
    def in_bounds(self, pos: Position) -> bool:
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    def is_opponent(self, piece: Piece, other: Piece) -> bool:
        return other is not None and piece.color != other.color

    def square_under_attack(self, pos: Position, by_color: Color) -> bool:
        for move in self.generate_pseudo_legal_moves(by_color):
            if move.end == pos:
                return True
        return False

    # ---------------- Move Generation ----------------
    def generate_pseudo_legal_moves(self, color: Color) -> List[Move]:
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece and piece.color == color:
                    moves.extend(self.get_piece_moves(piece, (row, col)))
        return moves

    def get_piece_moves(self, piece: Piece, pos: Position) -> List[Move]:
        if piece.type == PieceType.PAWN:
            return self.pawn_moves(piece, pos)
        elif piece.type == PieceType.ROOK:
            return self.straight_line_moves(piece, pos, [(-1,0),(1,0),(0,-1),(0,1)])
        elif piece.type == PieceType.BISHOP:
            return self.straight_line_moves(piece, pos, [(-1,-1),(-1,1),(1,-1),(1,1)])
        elif piece.type == PieceType.QUEEN:
            return self.straight_line_moves(piece, pos, [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)])
        elif piece.type == PieceType.KNIGHT:
            return self.knight_moves(piece, pos)
        elif piece.type == PieceType.KING:
            return self.king_moves(piece, pos)
        return []

    # ---------------- Pawn Moves ----------------
    def pawn_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos
        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        # Forward 1
        forward1 = (row + direction, col)
        if self.in_bounds(forward1) and self.board.is_empty(forward1):
            if forward1[0] in [0, 7]:
                for promo in ['q','r','b','n']:
                    moves.append(Move(pos, forward1, piece, promotion=promo))
            else:
                moves.append(Move(pos, forward1, piece))

            # Forward 2
            forward2 = (row + 2*direction, col)
            if row == start_row and self.board.is_empty(forward2):
                moves.append(Move(pos, forward2, piece))

        # Captures
        for dc in [-1,1]:
            capture_pos = (row + direction, col + dc)
            if self.in_bounds(capture_pos):
                target = self.board.get_piece(capture_pos)
                if self.is_opponent(piece, target):
                    if capture_pos[0] in [0,7]:
                        for promo in ['q','r','b','n']:
                            moves.append(Move(pos, capture_pos, piece, target, promo))
                    else:
                        moves.append(Move(pos, capture_pos, piece, target))

        # En passant
        if self.board.en_passant_target:
            ep_row, ep_col = self.board.en_passant_target
            if ep_row == row + direction and abs(ep_col - col) == 1:
                captured = self.board.get_piece((row, ep_col))
                if captured and captured.type == PieceType.PAWN:
                    moves.append(Move(pos, (ep_row, ep_col), piece, captured, is_en_passant=True))

        return moves

    # ---------------- Sliding Pieces ----------------
    def straight_line_moves(self, piece: Piece, pos: Position, directions: List[Tuple[int,int]]) -> List[Move]:
        moves = []
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not self.in_bounds((r,c)):
                    break
                target = self.board.get_piece((r,c))
                if target is None:
                    moves.append(Move(pos, (r,c), piece))
                elif self.is_opponent(piece, target):
                    moves.append(Move(pos, (r,c), piece, target))
                    break
                else:
                    break
        return moves

    # ---------------- Knight ----------------
    def knight_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            r, c = row + dr, col + dc
            if self.in_bounds((r,c)):
                target = self.board.get_piece((r,c))
                if target is None or self.is_opponent(piece, target):
                    moves.append(Move(pos, (r,c), piece, target))
        return moves

    # ---------------- King ----------------
    def king_moves(self, piece: Piece, pos: Position) -> List[Move]:
        moves = []
        row, col = pos

        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            r, c = row + dr, col + dc
            if self.in_bounds((r,c)):
                target = self.board.get_piece((r,c))
                if target is None or self.is_opponent(piece, target):
                    moves.append(Move(pos, (r,c), piece, target))

        # Castling (with safety)
        opponent = piece.color.opposite()
        if not piece.has_moved and not self.square_under_attack(pos, opponent):
            if self.can_castle_kingside(piece.color):
                if not self.square_under_attack((row, col+1), opponent) and not self.square_under_attack((row, col+2), opponent):
                    moves.append(Move(pos, (row, col+2), piece, is_castling=True))

            if self.can_castle_queenside(piece.color):
                if not self.square_under_attack((row, col-1), opponent) and not self.square_under_attack((row, col-2), opponent):
                    moves.append(Move(pos, (row, col-2), piece, is_castling=True))

        return moves

    # ---------------- Castling Helpers ----------------
    def can_castle_kingside(self, color: Color) -> bool:
        row = 7 if color == Color.WHITE else 0
        rook = self.board.get_piece((row,7))
        return (
            rook
            and rook.type == PieceType.ROOK
            and not rook.has_moved
            and all(self.board.is_empty((row,c)) for c in [5,6])
        )

    def can_castle_queenside(self, color: Color) -> bool:
        row = 7 if color == Color.WHITE else 0
        rook = self.board.get_piece((row,0))
        return (
            rook
            and rook.type == PieceType.ROOK
            and not rook.has_moved
            and all(self.board.is_empty((row,c)) for c in [1,2,3])
        )
