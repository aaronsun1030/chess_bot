import sys

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
        self.color = color
        pass

    # Find and return the best move for the given position.    
    def find_move():
        best_move = None
        findMove(self.board, self.max_depth(self.board), True,
                self.color, -1 * self.INFTY, self.INFTY)
        return last_found_move

    # 
    def findMove(board, depth, saveMove, turn, alpha, beta):
        if depth == 0:
            return static_score(board)
        
        
        
    def max_depth(board):
        return 7

    # Give a hueristic score for BOARD.
    def static_score(board):
        # YOUR CODE HERE
        return 0




    



