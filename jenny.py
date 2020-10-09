from heuristic import heuristic
import random

class Jenny(heuristic):
    """Jenny, the chess bot.
    Writted by Aaron, inspired by Chris.
    """

    def __init__(self):
        super()
        # All the pieces are worth the same to me!
        self.pieces = {'q': 8675309, 'r': 8675309, 'b': 8675309, 'n': 8675309, 
            'p': 8675309, 'Q': 8675309, 'R': 8675309, 'B': 8675309, 'N': 8675309, 'P': 8675309}
        # Prune always!
        self.delta = -1
        # Prune always!
        self.futility = [0, 0, 0, 0]
        # Depth 1 is enough for me!
        self.d_limit = 1
    
    def static_score(self, fen):
        # Chaos is all I desire!
        return random.randint(-8675309, 8675309)
    
    def think_time(self, fen, my_time, opp_time):
        # Thinking is for idiots!
        return min(0.8675309, my_time / 2)

    