
from pacman_module.game import Agent
from pacman_module.pacman import Directions
import random

class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

    def get_action(self, state, belief_state):
        """
        Given a pacman game state and a belief state,
                returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - `belief_state`: a list of probability matrices.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        legal_moves = state.getLegalPacmanActions()
        if Directions.STOP in legal_moves:
            legal_moves.remove(Directions.STOP)
        
        if not legal_moves:
            return Directions.STOP
            
        return random.choice(legal_moves)
