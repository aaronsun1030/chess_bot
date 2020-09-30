import sys
import time
"""
This file runs an AI that does alpha-beta pruning with the 
inputted heuristic. This is not intended to be changed for the 
purposes of the competition.
"""


class AI:
    
    def __init__(self, board, color, heuristic):
        """Create a new AI."""
        # A value which is better than winning.
        self.INFTY = sys.maxsize - 1
        # A value to indicate a player will win in the next move. Use this for faster wins.
        self.WINNING_VALUE = sys.maxsize - 10
        # A value to indicate a player will win in the coming moves.
        self.WILL_WIN_VALUE = sys.maxsize - 20


        # The best move in the current position.
        self.last_found_move = None
        self.board = board
        # 1 for white, -1 for black.
        self.color = color 
        self.heuristic = heuristic
        self.current_depth = 0
        pass
 
    def best_move(self):
        """Find and return the best move for the given position."""  
        self.last_found_move = None
        self.iterative_deepening(self.heuristic.think_time(self.board.fen(), 0, 0))
        return self.last_found_move
    
    def iterative_deepening(self, limit):
        """Run iterative deepening, stopping on the last depth once time runs out"""
        t1 = time.time()
        d = 2
        while time.time() - t1 < limit:
            self.current_depth = d
            print(d)
            print(time.time() - t1)
            self.find_move(self.board, d, True,
                self.color, -1 * self.INFTY, self.INFTY)
            d += 2

            

    def find_move(self, board, depth, saveMove, turn, alpha, beta):
        """Does alpha-beta pruning to find the best move for the given position."""
        if board.is_checkmate():
            if depth >= self.current_depth - 2:
                return -turn * self.WINNING_VALUE
            else:
                return -turn * self.WILL_WIN_VALUE

        if board.is_game_over():
            return 0

        if depth == 0:
            return self.heuristic.static_score(board.fen())

        possible_moves = board.legal_moves
        best_value = -turn * self.INFTY
        current_value = 0

        for move in possible_moves:
            board.push(move)
            current_value = self.find_move(board, depth - 1, False, turn * -1, alpha, beta)
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

        return best_value