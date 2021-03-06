# chess_bot
Minimax Chess AI.

Skeleton code for the chess heuristic competition. 

The competiton involves making the best chess heuristic for a chess AI. Everyone's will use the same AI, which uses some basic alpha beta pruning, but with a different heuristic (the part that tells how good or bad the position is).  
If you are interested in competing, please fill out this form: https://forms.gle/kRakX19n7KJwKdmx9

## Setup:

1. Clone the repo
2. Open terminal, cd to the file
3. Run "python -m venv ./venv"
4. Activate the virtual environment (look up, depends on OS). You will have to do this step every time you restart.
5. Run "pip install chess"

## File descriptions:

### CODING  
heuristic.py is an "interface" which your class should inherit from and should overwrite some of the functions of.  

### TESTING  
game.py lets you play against the AI or have the AI play against itself.  
testing.py runs your bot on a given set of tactics. The initial heuristic can already do most of them easily, so don't get your hopes up.  

### OTHER  
rules.txt has more details on the rules of the competition (allowed practices and expectations for submission).  
jenny.py is a sample submission (but not a very good one).  
AI.py has the pruning logic and stuff which you don't need to worry about.
