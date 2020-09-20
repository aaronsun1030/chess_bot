import sys
import chess

class AI:
    # A value which is better than winning.
    final self.INFTY = sys.maxsize
    # A value to indicate a player will win in the next move. Use this for faster wins.
    final self.WINNING_VALUE = sys.maxsize - 10
    # A value to indicate a player will win in the coming moves.
    final self.WILL_WIN_VALUE = sys.maxsize - 20

    # The best move in the current position.
    self.last_found_move = None
    # 1 for WHITE, -1 for BLACK
    self.color = 0
    # The current board state.
    self.board = None


    # Create a new AI.
    def __init__(board, color):
        self.board = board
        self.color = color # 1 for white, -1 for black.
        pass

    # Find and return the best move for the given position.    
    def find_move():
        best_move = None
        findMove(self.board, self.max_depth(self.board), True,
                self.color, -1 * self.INFTY, self.INFTY)
        return last_found_move

    # 
    def find_move(board, depth, saveMove, turn, alpha, beta):
        if board.is_checkmate():
            if depth >= max_depth(board) - 2:
                return -turn * self.WINNING_VALUE
            else:
                return -turn * self.WILL_WIN_VALUE

        if board.is_stalemate or board.can_claim_draw(): # add more
            return 0

        if depth == 0:
            return static_score(board)

        possible_moves = board.legal_moves
        best_value = -turn * self.INFTY
        current_value = 0

        for move in possible_moves:
            board.push(move)
            current_value = find_move(board, depth - 1, False, turn * -1, alpha, beta)
            board.pop()
            if turn == 1:
                if current_value > best_value:
                    best_value = current_value
                    if saveMove:
                        self.last_found_move = move
                alpha = max(alpha, best_value)
            else:
                if current_value < best_value:
                    best_value = current_value
                    if saveMove:
                        self.last_found_move = move
                beta = min(beta, best_value)
            
           
            if beta <= alpha:
                break
            



        
        
        
    def max_depth(board):
        return 7

    # Give a hueristic score for BOARD.
    def static_score(board):
        # YOUR CODE HERE
        return 0




    



