from heuristic import heuristic
import random

class Jenny(heuristic):
    """Jenny, the chess bot.
    Writted by Aaron, inspired by Chris.
    """

    def __init__(self):
        super()
    
    def static_score(self, fen):
        return random.randint(-8675309, 8675309)
    
    def think_time(self, fen, my_time, opp_time):
        return min(0.8675309, my_time / 2)

    