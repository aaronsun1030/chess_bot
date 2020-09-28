import sys
import chess
import chess.pgn

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
        pass
 
    def best_move(self):
        """Find and return the best move for the given position."""  
        self.last_found_move = None
        self.find_move(self.board, self.max_depth(self.board), True,
                self.color, -1 * self.INFTY, self.INFTY)
        return self.last_found_move

    def find_move(self, board, depth, saveMove, turn, alpha, beta):
        """Does alpha-beta pruning to find the best move for the given position."""
        if board.is_checkmate():
            if depth >= self.max_depth(board) - 2:
                return -turn * self.WINNING_VALUE
            else:
                return -turn * self.WILL_WIN_VALUE

        if board.is_stalemate() or board.can_claim_draw(): # add more
            return 0

        if depth == 0:
            return self.heuristic.static_score(board)

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
        
    def max_depth(self, board):
        return 3


"""import heuristic
h = heuristic.heuristic()
game = chess.pgn.Game()
b = chess.Board()
white = AI(b, 1, h)
black = AI(b, -1, h)
m = white.best_move()
b.push(m)
node = game.add_variation(m)
while not b.is_game_over():
    m = black.best_move()
    b.push(m)
    node = node.add_variation(m)
    if b.is_game_over():
        break
    m = white.best_move()
    b.push(m)
    node = node.add_variation(m)
print(game)"""