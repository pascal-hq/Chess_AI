from typing import List, Optional
import copy

from game.board import Board, Position
from game.piece import Piece, Color, PieceType
from game.move import Move
from game.rules import Rules


class GameState:
    def __init__(self):
        self.board = Board()
        self.rules = Rules(self.board)
        self.turn = Color.WHITE
        self.move_history: List[Move] = []

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------
    def opponent(self, color: Color) -> Color:
        return Color.BLACK if color == Color.WHITE else Color.WHITE

    # --------------------------------------------------
    # Check Detection
    # --------------------------------------------------
    def is_in_check(self, color: Color) -> bool:
        king_pos = (
            self.board.white_king_pos
            if color == Color.WHITE
            else self.board.black_king_pos
        )

        for move in self.rules.generate_pseudo_legal_moves(self.opponent(color)):
            if move.end == king_pos:
                return True
        return False

    # --------------------------------------------------
    # Legal Move Generation
    # --------------------------------------------------
    def get_legal_moves(self) -> List[Move]:
        legal_moves = []

        for move in self.rules.generate_pseudo_legal_moves(self.turn):
            self.make_move(move)
            if not self.is_in_check(self.turn):
                legal_moves.append(move)
            self.undo_move()

        return legal_moves

    # --------------------------------------------------
    # Make Move
    # --------------------------------------------------
    def make_move(self, move: Move):
        # Save state for undo
        move.previous_en_passant = self.board.en_passant_target
        move.previous_has_moved = move.piece.has_moved

        self.board.en_passant_target = None

        # ---------------- En Passant Capture ----------------
        if move.is_en_passant:
            captured_pos = (move.start[0], move.end[1])
            move.captured = self.board.get_piece(captured_pos)
            self.board.set_piece(captured_pos, None)

        # ---------------- Move Main Piece ----------------
        self.board.move_piece(move.start, move.end)
        move.piece.has_moved = True

        # ---------------- Castling ----------------
        if move.is_castling:
            row = move.start[0]
            if move.end[1] > move.start[1]:  # kingside
                rook_start, rook_end = (row, 7), (row, 5)
            else:  # queenside
                rook_start, rook_end = (row, 0), (row, 3)

            rook = self.board.get_piece(rook_start)
            self.board.move_piece(rook_start, rook_end)
            rook.has_moved = True

        # ---------------- Promotion ----------------
        if move.promotion:
            move.captured = None  # promotions never capture on the end square
            promoted_piece = Piece(
                {
                    'q': PieceType.QUEEN,
                    'r': PieceType.ROOK,
                    'b': PieceType.BISHOP,
                    'n': PieceType.KNIGHT,
                }[move.promotion],
                move.piece.color,
            )
            promoted_piece.has_moved = True
            self.board.set_piece(move.end, promoted_piece)

        # ---------------- En Passant Target ----------------
        if (
            move.piece.type == PieceType.PAWN
            and abs(move.start[0] - move.end[0]) == 2
        ):
            self.board.en_passant_target = (
                (move.start[0] + move.end[0]) // 2,
                move.start[1],
            )

        # ---------------- Finish ----------------
        self.move_history.append(move)
        self.turn = self.opponent(self.turn)

    # --------------------------------------------------
    # Undo Move
    # --------------------------------------------------
    def undo_move(self):
        if not self.move_history:
            return

        move = self.move_history.pop()
        self.turn = self.opponent(self.turn)

        # Restore state
        self.board.en_passant_target = move.previous_en_passant

        # ---------------- Undo Promotion ----------------
        if move.promotion:
            self.board.set_piece(move.end, move.piece)

        # ---------------- Undo Castling ----------------
        if move.is_castling:
            row = move.start[0]
            if move.end[1] > move.start[1]:
                rook_start, rook_end = (row, 7), (row, 5)
            else:
                rook_start, rook_end = (row, 0), (row, 3)

            rook = self.board.get_piece(rook_end)
            self.board.move_piece(rook_end, rook_start)
            rook.has_moved = False

        # ---------------- Restore Main Piece ----------------
        self.board.set_piece(move.start, move.piece)
        self.board.set_piece(move.end, move.captured)

        move.piece.has_moved = move.previous_has_moved

        # ---------------- Restore En Passant Pawn ----------------
        if move.is_en_passant and move.captured:
            captured_pos = (move.start[0], move.end[1])
            self.board.set_piece(captured_pos, move.captured)

        # ---------------- Restore King Position ----------------
        if move.piece.type == PieceType.KING:
            if move.piece.color == Color.WHITE:
                self.board.white_king_pos = move.start
            else:
                self.board.black_king_pos = move.start
