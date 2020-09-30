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
            print("evaluating at depth")
            print(d)
            print(time.time() - t1)
            self.find_move(self.board, d, True,
                self.color, -1 * self.INFTY, self.INFTY, t1, limit)
            d += 2

            

    def find_move(self, board, depth, saveMove, turn, alpha, beta, startTime, limit):
        """Does alpha-beta pruning to find the best move for the given position."""
        if time.time()-startTime > limit:
            print("timelimit reached")
            print(time.time() - startTime)
            return False, 0

        if board.is_checkmate():
            if depth >= self.current_depth - 2:
                return True, -turn * self.WINNING_VALUE
            else:
                return True, -turn * self.WILL_WIN_VALUE

        if board.is_game_over():
            return True, 0

        if depth == 0:
            return True, self.heuristic.static_score(board.fen())

        possible_moves = board.legal_moves
        best_value = -turn * self.INFTY
        current_value = 0

        found_move = None

        for move in possible_moves:
            board.push(move)
            time_remaining, current_value = self.find_move(board, depth - 1, False, turn * -1, alpha, beta, startTime, limit)
            if not time_remaining:
                board.pop()
                return False, 0

            board.pop() 
            if turn == 1:
                if current_value > best_value:
                    best_value = current_value
                    if saveMove:
                        found_move = move
                alpha = max(alpha, best_value)
            else:
                if current_value < best_value:
                    best_value = current_value
                    if saveMove:
                        found_move = move
                beta = min(beta, best_value)
            
           
            if beta <= alpha:
                break

        if saveMove:
            print("updated move")
            print(found_move)
            self.last_found_move = found_move

        return True, best_value