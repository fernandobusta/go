def validate_move(move, currentPlayer):
    return True

def process_move(move, currentPlayer):
    board = [[0 for i in range(9)] for j in range(9)]
    board[2][3] = 1
    board[5][4] = 2
    board[5][3] = 2
    return board