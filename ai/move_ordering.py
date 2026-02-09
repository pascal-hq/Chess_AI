from game.move import Move

def order_moves(moves: list[Move]) -> list[Move]:
    """
    Sort moves to try captures and promotions first.
    """
    return sorted(moves, key=lambda m: (
        m.is_promotion, m.is_capture()
    ), reverse=True)
